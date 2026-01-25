from email.mime import message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.shortcuts import get_object_or_404

from api.services.minIo_service import MinIOService
from api.services.google_genai import GoogleGenAIService
from api.services.user_lesson_service import search_lessons_for_user
from .models import RequestModel
from pydantic import ValidationError
from .serializers import *
from .models import UserInfo, User, FriendRequest
from rest_framework.exceptions import AuthenticationFailed
from .messages import ErrorMessages, SuccessMessages
from .services.text_to_sign_service import text_to_sign_process_smoothing
from src.utils.util import convert_none_to_nan
from .services.grpc_ai_client import recognize_sign_grpc, health_check_grpc
from .services.llm_services import LLMService
from .services.video_processing_service import VideoProcessingService
from api.const import *
from .exceptions import handle_validation_error
from django.db.models import Q
import json
from django.db import IntegrityError, transaction
import requests
import traceback
from django.http import FileResponse, StreamingHttpResponse
from datetime import timedelta, datetime
from api.services.vn_chunker_service import chunk_text_strings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import os, json, uuid, tempfile
from django.core.cache import cache
from .models import Lesson, Section, UserLessons, UserSections
from django.db.models import Sum
from api.services.user_lesson_service import mark_word_completed

googleGenAIService = GoogleGenAIService()

@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request):
    return Response({"message": SuccessMessages.SERVER_AVAILABLE}, status=200)

# region User Feature
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    try:
        keyword = request.GET.get('keyword', '').strip()

        users = UserInfo.objects.select_related('user').filter(user_id__is_deleted=False).exclude(user = request.user)

        if keyword:
            users = users.filter(
                Q(full_name__icontains=keyword) |
                Q(user__username__icontains=keyword) |
                Q(email__icontains=keyword)
            )
            users = users.order_by('full_name')[:20]

        else:
            users = users.order_by('full_name')

        serializer = GetUserInfoSerializer(users, many=True)
        
        return standard_response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )
    
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e),
        )

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny]) 
def user_profile(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=user_id, is_deleted=False)
            serializer = UserProfileSerializer(user)
            return standard_response(
                status= status.HTTP_200_OK,
                data= serializer.data
            )
            
        except User.DoesNotExist:
            return standard_response(
                status= status.HTTP_404_NOT_FOUND,
                message= ErrorMessages.USER_NOT_FOUND
            )
            
        except Exception as e:
            return standard_response(
                status= status.HTTP_500_INTERNAL_SERVER_ERROR,
                message= str(e)
            )    
    elif request.method == 'PUT':
        try:
                user = User.objects.get(pk=user_id, is_deleted=False)
                serializer = UserUpdateSerializer(user, data=request.data)
                if not serializer.is_valid():
                    error_data = handle_validation_error(serializer)
                    return standard_response(
                        status=error_data['status'],
                        message=error_data['message']
                    )
                
                serializer.save()
                return standard_response(status=status.HTTP_200_OK, data=serializer.data)
            
        except User.DoesNotExist:
            return standard_response(
                status= status.HTTP_404_NOT_FOUND,
                message= ErrorMessages.USER_NOT_FOUND
            )
        except Exception as e:
            return standard_response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_image(request):
    try:
        minio_service = MinIOService()
        data, status_code = minio_service.upload_base64_image(request.data.get('base64'))
        return standard_response(status=status_code, data=data)
    
    except Exception as e:
        return standard_response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=str(e)
            )       
# endregion
        
def standard_response(status, message="Success", data=None):
    return Response({
        "status": status,
        "message": message,
        "data": data
    }, status=status)    

# region Sign Feature
@api_view(['POST'])
@permission_classes([AllowAny])
def llm_invoke(request):
    try:
        llm = LLMService()
        data, status_code = llm.gemini_api(request.data)
        return Response(data, status=status_code)
    except requests.exceptions.RequestException as e:
        error_details = {
            "error_message": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()  # Lấy full traceback
        }
        return Response(error_details, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def adapt_frames_to_xyz(frames):
    adapted = []
    for f in frames:
        kps = f.get("keypoints", [])
        # assume keypoints is a list of [x, y, z]
        xs = [pt[0] for pt in kps]
        ys = [pt[1] for pt in kps]
        zs = [pt[2] for pt in kps]
        adapted.append({"x": xs, "y": ys, "z": zs})
    return adapted

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_to_text(request):
    platform = request.GET.get('platform', PLATFORM_MOBILE)
    language_code = request.GET.get('language_code', LANGUAGE_AU)

    payload = request.data or {}
    frames = payload.get("frames") or payload.get("data") or []
    adapted = adapt_frames_to_xyz(frames)

    try:
        validated_data = RequestModel(data=adapted)
    except ValidationError as e:
        return Response({"error": e.errors()}, status=status.HTTP_400_BAD_REQUEST)

    predicted_class, confidence, error, status_code = recognize_sign_grpc(
        validated_data.data,
        platform=platform,
        language_code=language_code,
    )

    response_data = {"Class": predicted_class, "Confidence": confidence}
    if error:
        response_data["error"] = error

    if platform == PLATFORM_MOBILE:
        return Response(response_data, status=status_code)
    return standard_response(
        status=status_code,
        data=[response_data] if status_code == 200 else response_data,
    )
    
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_to_text_combine(request):
    try:
        platform = request.GET.get('platform', PLATFORM_MOBILE) 
        language_code = request.GET.get('language_code', LANGUAGE_AU)  

        json_data = json.loads(request.body)
        
        # Parse JSON data similar to original process_prediction_combine_api
        from .services.json_compare_service import rearrange_landmark_data_concatenated_padded
        json_data_processed = rearrange_landmark_data_concatenated_padded(json_data)
        json_data_processed["data"] = convert_none_to_nan(json_data_processed.get("data"))
        
        try:
            validated_data = RequestModel(data=json_data_processed["data"])
        except ValidationError as e:
            return standard_response(
                status=status.HTTP_400_BAD_REQUEST,
                message=str(e.errors())
            )
        
        # Call gRPC AI service
        predicted_class, confidence, error, status_code = recognize_sign_grpc(
            validated_data.data,
            platform=platform or PLATFORM_MOBILE,
            language_code=language_code or LANGUAGE_AU
        )
        
        response_data = [{
            "Class": predicted_class,
            "Confidence": confidence
        }] if status_code == 200 else {"error": error}

        return standard_response(
            status=status_code,
            data=response_data,
        )

    except ValidationError as e:
        return standard_response(
            status=status.HTTP_400_BAD_REQUEST,
            message=str(e.errors())
        )
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Error connecting to AI service: {str(e)}"
        )    

@api_view(['GET'])
@permission_classes([AllowAny])
def text_to_sign_smooth(request):
    try:
        request_text = request.query_params.get("text")
        language_code = request.GET.get('language_code', LANGUAGE_AU)
        result, status_code = text_to_sign_process_smoothing(request_text, language_code)

        if status_code == status.HTTP_200_OK:
            
            # Return file response
            return FileResponse(
                result["pose_file"],
                content_type='application/octet-stream',
                headers={
                    'Content-Disposition': 'attachment; filename="output.pose"'
                }
            )

        return standard_response(
                status=status_code,
                data=result
            ) 

    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e))

@api_view(['GET'])
@permission_classes([AllowAny])
def check_device(request):
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        return Response(device, status=200)

    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e))
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def json_to_text(request):
    try:
        json_data = json.loads(request.body)
        result = test_manual_file_similarity(json_data=json_data)
            
        return standard_response(
                status=status.HTTP_200_OK,
                data=result
            ) 

    except ValidationError as e:
        return Response({"error": e.errors()}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
@permission_classes([AllowAny])
def recognize_sign_from_minio_video(request):
    """
    Lấy video từ MinIO, extract frames, extract landmarks, gửi tới AI gRPC.
    
    Request body:
    {
        "minio_path": "videos/my_sign.mp4",
        "platform": "web",  (optional, default "web")
        "language_code": "au",  (optional, default "au")
        "sample_rate": 5  (optional, lấy 1 frame cứ mỗi N frame)
    }
    """
    try:
        data = request.data
        minio_path = data.get("minio_path")
        platform = data.get("platform", "web")
        language_code = data.get("language_code", "au")
        sample_rate = int(data.get("sample_rate", 5))
        
        if not minio_path:
            return standard_response(
                status=status.HTTP_400_BAD_REQUEST,
                message="minio_path is required"
            )
        
        # Import MediaPipe detector
        try:
            import mediapipe as mp
            mp_holistic = mp.solutions.holistic
            detector = mp_holistic.Holistic()
        except ImportError:
            return standard_response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="MediaPipe not installed"
            )
        
        # Process video
        video_service = VideoProcessingService()
        predicted_class, confidence, error, response_status = (
            video_service.process_video_from_minio_and_recognize(
                minio_path=minio_path,
                detector=detector,
                platform=platform,
                language_code=language_code,
                sample_rate=sample_rate
            )
        )
        
        if response_status != 200:
            return standard_response(
                status=response_status,
                message=error or "Error processing video"
            )
        
        return standard_response(
            status=status.HTTP_200_OK,
            data={
                "Class": predicted_class,
                "Confidence": confidence
            }
        )
    
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )

# endregion

# region Authen Feature
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    # Retrieve the username and password from the request
    username = request.data.get('Username')
    password = request.data.get('Password')

    # Check if username and password are provided
    if not username or not password:
        return Response({"error": ErrorMessages.USERNAME_PASS_REQUIRED}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user = authenticate(username=username, password=password)

    if user is not None:
        try:
            user_info = UserInfo.objects.get(user_id=user.id)

            refresh = RefreshToken.for_user(user)
            return standard_response(
            status=status.HTTP_200_OK,
            data={
                "UserId": user.id,
                "Username": user.username,
                "UserType": user.user_type,
                "FullName": user_info.full_name,
                "Phone": user_info.phone,
                "Email": user_info.email,
                "Avatar": user_info.avatar,
                "Gender": user_info.gender,
                "DateOfBirth": user_info.date_of_birth,
                "Address": user_info.address,
                "IsActive": user.is_active,
                "Access": str(refresh.access_token),  # access token
                "Refresh": str(refresh),  # refresh token
            })
        except Exception as e:
            return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    else:
        return standard_response(
            status=status.HTTP_401_UNAUTHORIZED,
            message=ErrorMessages.USERNAME_PASS_INCORRECT)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    user_data = request.data
    user = None

    # Create User
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        try:
            user = user_serializer.save()  # Create a new user

            if user:
                # Create UserInfo
                user_info_data = {
                    'user': user.id,
                    'full_name': user_data.get('FullName'),
                    'phone': user_data.get('PhoneNumber', None),
                    'email': user_data.get('Email'),
                    'address': user_data.get('Address', None),
                    'date_of_birth': user_data.get('DateOfBirth'),
                    'avatar': user_data.get('Avatar', None),
                    'gender': user_data.get('Gender')
                }
                user_info_serializer = UserInfoSerializer(data=user_info_data)
                if user_info_serializer.is_valid():
                    user_info_serializer.save()
                else:
                    # Delete User if UserInfo creation fails
                    user.delete()
                    error_data = handle_validation_error(user_info_serializer)
                    return standard_response(
                        status=error_data['status'],
                        message=error_data['message']
                    )

            return standard_response(
                status=status.HTTP_200_OK,
                data={
                    'user': user_serializer.data
            })

        except Exception as e:
            # Delete User if an error occurs
            if user is not None:
                user.delete()
            return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e))

    else:
        error_data = handle_validation_error(user_serializer)
        return standard_response(
            status=error_data['status'],
            message=error_data['message']
        )

@api_view(['POST'])
def logout_user(request):
    try:
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return standard_response(
            status=status.HTTP_400_BAD_REQUEST,
            message=ErrorMessages.AUTH_HEADER_MISSING
        )

        # Ensure the header format is 'Bearer <token>'
        if not auth_header.startswith('Bearer '):
            return standard_response(
            status=status.HTTP_400_BAD_REQUEST,
            message=ErrorMessages.INVALID_AUTH_HEADER_FORMAT)

        # Extract the access token from the header
        access_token = auth_header.split(' ')[1]

        # Decode the access token
        access = AccessToken(access_token)

        return standard_response(
            status= status.HTTP_200_OK,
            message= SuccessMessages.LOGOUT_SUCCESSFUL)
    
    except AuthenticationFailed as e:
        return standard_response(
            status=status.HTTP_401_UNAUTHORIZED,
            message=str(e),
        )
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e),
        )

@api_view(['POST'])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return standard_response(
                status=status.HTTP_400_BAD_REQUEST,
                message= ErrorMessages.REFRESH_TOKEN_VALIDATE,
            ) 

        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)

        return standard_response(
            data= {
                    "Access": new_access_token
            }
        ) 

    except Exception as e:
        return standard_response(
            status=status.HTTP_401_UNAUTHORIZED,
            message=ErrorMessages.REFRESH_TOKEN_INVALID,
        )    
# endregion

# region Friend Feature
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, receiver_id):
    try:
        sender = request.user
        receiver = User.objects.get(pk=receiver_id, is_deleted=False)
        
        if sender == receiver:
            return standard_response(
                status = status.HTTP_400_BAD_REQUEST,
                message = ErrorMessages.FRIEND_REQUEST_YOURSELF
            )
        
        existing_request = FriendRequest.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | 
            (Q(sender=receiver) & Q(receiver=sender))
        ).first()
        
        if existing_request:
            if existing_request.status == FRIEND_REQUEST_PENDING:
                return standard_response(
                    status= status.HTTP_400_BAD_REQUEST,
                    message= ErrorMessages.FRIEND_REQUEST_EXIST
                )
            elif existing_request.status == FRIEND_REQUEST_ACCEPT:
                return standard_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=ErrorMessages.FRIEND_REQUEST_ACCEPTED
                )
            elif existing_request.status == FRIEND_REQUEST_REJECT:
                if existing_request.sender == sender:
                # Nếu user hiện tại là người gửi request ban đầu
                    existing_request.status = FRIEND_REQUEST_PENDING
                    existing_request.save()
                else:
                    print("VAO DAY HONG")
                    # Trường hợp 2: User hiện tại là người nhận request ban đầu
                    # Đảo ngược sender và receiver
                    with transaction.atomic():
                        existing_request.delete()  # Xóa request cũ
                        new_request = FriendRequest.objects.create(
                            sender=sender,
                            receiver=receiver,
                            status=FRIEND_REQUEST_PENDING
                        )
                        existing_request = new_request

                serializer = FriendRequestSerializer(existing_request)
                return standard_response(
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
        
        friend_request = FriendRequest.objects.create(
            sender=sender,
            receiver=receiver,
            status=FRIEND_REQUEST_PENDING
        )
        
        serializer = FriendRequestSerializer(friend_request)
        
        return standard_response(
            status=status.HTTP_200_OK,
            data=serializer.data,
            message=SuccessMessages.FRIEND_REQUEST_SENT
        )
    
    except User.DoesNotExist:
        return standard_response(
            status=status.HTTP_404_NOT_FOUND,
            message=ErrorMessages.USER_NOT_FOUND
        )
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def respond_friend_request(request, request_id, action):
    try:
        action = action.lower()
        if action not in [FRIEND_REQUEST_ACTION_ACCEPT, FRIEND_REQUEST_ACTION_REJECT]:
            return standard_response(
                status=status.HTTP_400_BAD_REQUEST,
                message=ErrorMessages.FRIEND_REQUEST_ACTION_VALIDATE
            )
        
        friend_request = FriendRequest.objects.get(
            pk=request_id,
            receiver=request.user,
            status='pending'
        )
        
        sender_user = friend_request.sender
        receiver_user = request.user

        conversation_id = None

        if action == FRIEND_REQUEST_ACTION_ACCEPT:
            friend_request.status = FRIEND_REQUEST_ACCEPT
            friend_request.save()

            # Create conversation
            user1_id = min(sender_user.id, receiver_user.id)
            user2_id = max(sender_user.id, receiver_user.id)

            conversation, created = Conversation.objects.get_or_create(
                user1_id=user1_id,
                user2_id=user2_id
            )

            conversation_id = conversation.id

            message = "Friend request accepted."
        else:
            friend_request.status = FRIEND_REQUEST_REJECT
            friend_request.save()
            message = "Friend request rejected."
        
        serializer = FriendRequestSerializer(friend_request)
        response_data = {
            'friend_request': serializer.data,
            'conversation_id': conversation_id,
        }
        
        return standard_response(
            status=status.HTTP_200_OK,
            data=response_data,
            message=message
        )
    
    except FriendRequest.DoesNotExist:
        return standard_response(
            status=status.HTTP_404_NOT_FOUND,
            message=ErrorMessages.FRIEND_REQUEST_NOT_FOUND
        )
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_requests(request):
    try:
        user = request.user
        
        friend_requests = FriendRequest.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver', 'sender__userinfo', 'receiver__userinfo')
        
        serializer = FriendRequestDetailSerializer(
            friend_requests, 
            many=True,
            context={'request': request}
        )
        
        return standard_response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )
    
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_friend_request(request, request_id):
    try:
        with transaction.atomic():

            friend_request = FriendRequest.objects.select_for_update().get(
                pk=request_id,
                sender=request.user,
                status=FRIEND_REQUEST_PENDING
            )
            
            friend_request.delete()
            
            return standard_response(
                status=status.HTTP_200_OK,
                message=SuccessMessages.FRIEND_REQUEST_CANCELED
            )
    
    except FriendRequest.DoesNotExist:
        return standard_response(
            status=status.HTTP_404_NOT_FOUND,
            message=ErrorMessages.FRIEND_REQUEST_NOT_FOUND
        )
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_relationships(request):
    try:
        current_user = request.user

        # Step 1: Get all ACCEPTED friend requests involving the current user
        friend_requests = FriendRequest.objects.filter(
            Q(sender=current_user) | Q(receiver=current_user),
            status=FRIEND_REQUEST_ACCEPT
        ).select_related('sender__userinfo', 'receiver__userinfo')

        friends = []
        friend_ids = []

        for fr in friend_requests:
            # Determine if the current user is sender or receiver, then get the other user (friend)
            friend = fr.sender if fr.sender != current_user else fr.receiver
            if friend.id not in friend_ids:
                friends.append(friend)
                friend_ids.append(friend.id)

        # Step 2: Get all conversations between current user and each friend
        user_pairs = [(min(current_user.id, fid), max(current_user.id, fid)) for fid in friend_ids]
        conversations = Conversation.objects.filter(
            user1_id__in=[u1 for u1, u2 in user_pairs],
            user2_id__in=[u2 for u1, u2 in user_pairs]
        )
        conversation_map = {}
        user_conv_map = {}

        for conv in conversations:
            # Identify the other user in the conversation
            other_user_id = conv.user2_id if conv.user1_id == current_user.id else conv.user1_id
            conversation_map[conv.id] = conv
            user_conv_map[other_user_id] = conv

        # Step 3: Get list of pinned conversations for the current user
        my_pinned_conv_ids = set()
        if friend_ids:
            my_pinned_conv_ids = set(PinnedConversation.objects.filter(
                user=current_user,
                conversation_id__in=conversation_map.keys()
            ).values_list('conversation_id', flat=True))

        # Step 4: Get last message for each conversation
        last_messages = {}
        if conversation_map:
            messages = Message.objects.filter(
                conversation_id__in=conversation_map.keys(),
                id__in=[c.last_message_id for c in conversation_map.values() if c.last_message_id]
            ).values('conversation_id', 'content', 'sent_at')

            for msg in messages:
                last_messages[msg['conversation_id']] = {
                    'content': msg['content'],
                    'sent_at': msg['sent_at']
                }

        # Step 5: Count unread messages from friends
        unread_counts = {}
        if conversation_map and friend_ids:
            unread_list = Message.objects.filter(
                conversation_id__in=conversation_map.keys(),
                sender__in=friend_ids,
                is_read=False
            ).values_list('sender', 'conversation_id').annotate(count=models.Count('id'))

            for sender_id, conv_id, count in unread_list:
                unread_counts[(sender_id, conv_id)] = count

        # Step 6: Attach additional properties to each user
        for user in friends:
            conv = user_conv_map.get(user.id)
            user.conversation_id = conv.id if conv else None
            if conv and conv.id in last_messages:
                user.last_message_content = last_messages[conv.id]['content']
                user.last_message_sent_at = last_messages[conv.id]['sent_at']
            else:
                user.last_message_content = None
                user.last_message_sent_at = None
            user.unread_count = unread_counts.get((user.id, conv.id), 0) if conv else 0
            user.is_pinned = conv.id in my_pinned_conv_ids if conv else False

        # Step 7: Get pending friend requests
        requested = FriendRequest.objects.filter(
            sender=current_user,
            status='pending'
        ).select_related('receiver', 'receiver__userinfo')

        received = FriendRequest.objects.filter(
            receiver=current_user,
            status='pending'
        ).select_related('sender', 'sender__userinfo')

        # Step 8: Serialize data
        friend_serializer = FriendUserSerializer(friends, many=True, context={'request': request})
        requested_serializer = FriendRequestSerializer(requested, many=True)
        received_serializer = ReceivedRequestSerializer(received, many=True)

        response = {
            "friends": friend_serializer.data,
            "requested": requested_serializer.data,
            "received": received_serializer.data
        }

        return standard_response(status=200, data=response)

    except Exception as e:
        return standard_response(status=500, message=str(e))
# endregion

# region Chat Feature
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    receiver_id = request.data.get('receiver_id')
    content = request.data.get('content')

    if not receiver_id or not content:
        return standard_response(
            status=status.HTTP_400_BAD_REQUEST,
            message="Missing receiver_id or content"
        )

    try:
        sender = request.user
        receiver = User.objects.get(id=receiver_id)

        user1_id = min(sender.id, receiver.id)
        user2_id = max(sender.id, receiver.id)

        conversation = Conversation.objects.filter(user1=user1_id, user2=user2_id).first()

        if not conversation:
            return standard_response(
                status=status.HTTP_400_BAD_REQUEST,
                message="Conversation does not exist."
            )
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content,
        )

        serializer = MessageSerializer(message)

        return standard_response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    except User.DoesNotExist:
        return standard_response(
            status=status.HTTP_404_NOT_FOUND,
            message="Receiver not found"
        )
    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, conversation_id):
    try:
        user = request.user

        conversation = Conversation.objects.filter(id=conversation_id).first()
        if not conversation:
            return standard_response(
                status=status.HTTP_404_NOT_FOUND,
                message="Conversation not found"
            )

        if user.id not in [conversation.user1_id, conversation.user2_id]:
            return standard_response(
                status=status.HTTP_403_FORBIDDEN,
                message="You are not part of this conversation"
            )

        thirty_days_ago = timezone.now() - timedelta(days=30)
        messages = Message.objects.filter(
            conversation=conversation,
            sent_at__gte=thirty_days_ago
        ).order_by('sent_at')

        Message.objects.filter(
            ~Q(sender=user),
            is_read=False,
            conversation=conversation
        ).update(is_read=True)

        serializer = MessageSerializer(messages, many=True)

        return standard_response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    except Exception as e:
        return standard_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_pin_conversation(request, conversation_id):
    try:
        user = request.user
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if user.id not in [conversation.user1_id, conversation.user2_id]:
            return standard_response(
                status=403,
                message=ErrorMessages.NOT_IN_CONVERSATION
            )

        pinned_conv, created = PinnedConversation.objects.get_or_create(
            user=user,
            conversation=conversation
        )

        if not created:
            pinned_conv.delete()
            message=SuccessMessages.UNPINED_MESSAGE
        else:
            message=SuccessMessages.PINED_MESSAGE
        
        return standard_response(status=status.HTTP_200_OK, message=message)

    except Exception as e:
        return standard_response(status=500, message=str(e))    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def text_chunking(request):
    text = request.data.get('text', '')
    words_chunking = chunk_text_strings(text, score_dict={}, score_threshold=0.7, keep_threshold=0.5)
    print(words_chunking)
    return standard_response(status=status.HTTP_200_OK, data=words_chunking)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_training_words(request):
    training_words = TrainingWord.objects.filter(disabled=False).order_by("-created_at")
    serializer = TrainingWordSerializer(training_words, many=True)
    return standard_response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_training_word(request):
    try:
        training_word = request.data.get('word', '')
        url = request.data.get('url', '')
        key = request.data.get('key', '')
        word = TrainingWord.objects.create(
            word=training_word,
            disabled=False,
            url=url,
            key=key
        )
        serializer = TrainingWordSerializer(word)
    except:
        return standard_response(status=status.HTTP_400_BAD_REQUEST, message="Can not add training word")
    return standard_response(status=status.HTTP_201_CREATED, data=serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def update_training_word(request):
    training_word = request.data.get('word', '')
    url = request.data.get('url', '')
    disabled = request.data.get('disabled', False)
    key = request.data.get('key', '')
    try:
        word = TrainingWord.objects.get(word=training_word)
        word.url = url
        word.disabled = disabled
        word.key = key
        word.save()
    except TrainingWord.DoesNotExist:
        return standard_response(status=status.HTTP_404_NOT_FOUND, message="Training word not found")
    return standard_response(status=status.HTTP_200_OK, data={"message": f"{word} updated successfully"})


TMP_ROOT = os.path.join(tempfile.gettempdir(), "django_generic_uploads")
os.makedirs(TMP_ROOT, exist_ok=True)

def _meta_path(upload_id: str) -> str:
    return os.path.join(TMP_ROOT, f"{upload_id}.json")

def _file_path(upload_id: str) -> str:
    return os.path.join(TMP_ROOT, f"{upload_id}.part")

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_video(request):
    try:
        # Check for video file
        if 'video' not in request.FILES:
            return Response({'message': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        video = request.FILES['video']

        # Create upload folder if not exist
        upload_folder = os.path.join(tempfile.gettempdir(), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        # Generate unique filename
        file_path = os.path.join(upload_folder, video.name)

        # Save video file
        with open(file_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)
                
        date_save_video = cache.get("date_save_video")
        today_folder = date_save_video if date_save_video else datetime.now().strftime("%Y-%m-%d")
        mime = "application/octet-stream"
        minio_service = MinIOService()
        result = minio_service.upload_to_minio(file_path, f"video/{today_folder}/{video.name}", content_type=mime)
        if not result.get("success"):
            return standard_response(message=f"Upload failed: {result.get('error')}",
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message': 'Video uploaded successfully', 'file_path': file_path}, status=status.HTTP_200_OK)

    except Exception as e:
        return standard_response(message=f"Upload failed: {e}",
                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_video(request):
    """
    Delete a video by its name.
    Example request body: { "name": "my_video.webm" }
    """
    try:
        # Get filename from request
        video_name = request.data.get("object_name")
        if not video_name:
            return Response({'message': 'Missing "object_name" in request'}, status=status.HTTP_400_BAD_REQUEST)

        video_object = f"{video_name}.webm"
        mediapipe_object = f"{video_name}.json"

        # Local path
        upload_folder_video = os.path.join(tempfile.gettempdir(), 'uploads')
        upload_folder_json = os.path.join(tempfile.gettempdir(), 'mediapipe')

        file_path_video = os.path.join(upload_folder_video, video_object)
        file_path_json = os.path.join(upload_folder_json, mediapipe_object)

        # Delete from local temp video if exists
        if os.path.exists(file_path_video):
            os.remove(file_path_video)
            print(f"Deleted local file: {file_path_video}")
        else:
            print(f"Local file not found: {file_path_video}")

        # Delete from local temp json if exists
        if os.path.exists(file_path_json):
            os.remove(file_path_json)
            print(f"Deleted local file: {file_path_json}")
        else:
            print(f"Local file not found: {file_path_json}")

        try:
            date_save_video = cache.get("date_save_video")
            today_folder = date_save_video if date_save_video else datetime.now().strftime("%Y-%m-%d")
            # Also delete from MinIO
            minio_service = MinIOService()
            video_result = minio_service.delete_from_minio(f"video/{today_folder}/{video_object}")
            mediapipe_result = minio_service.delete_from_minio(f"mediapipe/{today_folder}/{mediapipe_object}")
        except Exception as e:
            print(f"⚠️ MinIO deletion failed: {e}")
            video_result = {"success": False, "error": str(e)}
            mediapipe_result = {"success": False, "error": str(e)}

        # Always return a proper Response
        return Response({
            "message": "Deletion completed (local + MinIO attempted)",
            "results": {
                "video": video_result,
                "mediapipe": mediapipe_result
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"message": f"Unexpected error: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def start_upload(request):
    try:
        raw = request.body.decode('utf-8') if request.body else ''
        data = json.loads(raw) if raw else {}
        if not isinstance(data, dict):
            data = json.loads(data)
    except Exception:
        return standard_response(message="Invalid JSON payload",
                                 status=status.HTTP_400_BAD_REQUEST)

    object_name = data.get("objectName")
    mime = data.get("mime") or "application/octet-stream"
    if not object_name:
        return standard_response(message="Missing objectName",
                                 status=status.HTTP_400_BAD_REQUEST)

    upload_id = str(uuid.uuid4())
    print(f"Starting    __________  {_file_path(upload_id)}")
    open(_file_path(upload_id), "wb").close()
    meta = {"objectName": object_name, "mime": mime, "nextIndex": 0}
    with open(_meta_path(upload_id), "w", encoding="utf-8") as f:
        json.dump(meta, f)

    return standard_response(
        data={"upload_id": upload_id},
        message="Session created",
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_chunk(request):
    print("Starting upload chunk...")
    upload_id = request.headers.get("X-Upload-Id")
    if not upload_id:
        return standard_response(message="Missing X-Upload-Id",
                                 status=status.HTTP_400_BAD_REQUEST)

    meta_file = _meta_path(upload_id)
    if not os.path.exists(meta_file):
        object_name = request.headers.get("X-Object-Name") or request.GET.get("objectName")
        mime_type = request.headers.get("X-Mime-Type") or request.GET.get("mime", "application/octet-stream")
        if object_name:
            # initialize session metadata and temp file
            print(f"uploading chunk {upload_id}")
            meta = {"objectName": object_name, "mime": mime_type, "nextIndex": 0}
            with open(meta_file, "w", encoding="utf-8") as f:
                print(f"Processing: uploading chunk {upload_id}")
                json.dump(meta, f)
            open(_file_path(upload_id), "wb").close()
        else:
            return standard_response(message="Upload session not found",
                                     status=status.HTTP_404_NOT_FOUND)

    print(f"uploading chunk {upload_id}")
    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)

    idx_hdr = request.headers.get("X-Chunk-Index")
    if idx_hdr is None:
        return standard_response(message="Missing X-Chunk-Index",
                                 status=status.HTTP_400_BAD_REQUEST)
    try:
        idx = int(idx_hdr)
    except ValueError:
        return standard_response(message="Invalid X-Chunk-Index",
                                 status=status.HTTP_400_BAD_REQUEST)

    expected = meta.get("nextIndex", 0)
    if idx != expected:
        return standard_response(
            message=f"Unexpected chunk index {idx}, expected {expected}",
            status=status.HTTP_409_CONFLICT,
        )
    print(f"Start Writing body .................")
    with open(_file_path(upload_id), "ab") as out:
        out.write(request.body)
    print(f"End Writing body .................")

    meta["nextIndex"] = expected + 1
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f)

    return standard_response(
        data={"upload_id": upload_id, "next_index": meta["nextIndex"]},
        message="Chunk accepted",
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def finish_upload(request):
    print("Finish upload ...")
    print(request)
    # Parse JSON payload
    try:
        raw = request.body.decode('utf-8') if request.body else ''
        data = json.loads(raw) if raw else {}
        if not isinstance(data, dict):
            data = json.loads(data)
    except Exception:
        return standard_response(message="Invalid JSON payload",
                                 status=status.HTTP_400_BAD_REQUEST)

    upload_id = data.get("uploadId")
    object_name = data.get("objectName")
    if not upload_id or not object_name:
        return standard_response(message="Missing uploadId or objectName",
                                 status=status.HTTP_400_BAD_REQUEST)

    meta_file = _meta_path(upload_id)
    if not os.path.exists(meta_file):
        return standard_response(message="Session not found",
                                 status=status.HTTP_404_NOT_FOUND)

    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)

    print(f"[FINISH] upload_id={upload_id} objectName(client)={object_name} objectName(meta)={meta.get('objectName')}")

    if object_name != meta.get("objectName"):
        return standard_response(
            message=f"Object name mismatch (got '{object_name}', expected '{meta.get('objectName')}')",
            status=status.HTTP_400_BAD_REQUEST
        )

    file_path = _file_path(upload_id)
    if not os.path.exists(file_path):
        return standard_response(message="Temp file not found",
                                 status=status.HTTP_404_NOT_FOUND)
    

    mime = meta.get("mime") or "application/octet-stream"
    minio_service = MinIOService()
    try:
        print("=======================")
        result = minio_service.upload_to_minio(file_path, f"video/{meta.get('objectName')}", content_type=mime)
        if not result.get("success"):
            return standard_response(message=f"Upload failed: {result.get('error')}",
                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Upload successful")
    except Exception as e:
        return standard_response(message=f"Upload failed: {e}",
                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Cleanup
    # try:
    #     os.remove(file_path)
    # except OSError:
    #     pass
    # try:
    #     os.remove(meta_file)
    # except OSError:
    #     pass
    return standard_response(
        data={"object_name": object_name, "upload_id": upload_id},
        message="Upload finished",
        status=status.HTTP_200_OK,
    )


CAPTURE_DATA_ROOT = os.path.join(tempfile.gettempdir(), 'mediapipe')
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_capture_mediapine(request):
    os.makedirs(CAPTURE_DATA_ROOT, exist_ok=True)
    # print(request.data)
    object_name = request.data.get("objectName")
    filename = f"{object_name}.json"
    path = os.path.join(CAPTURE_DATA_ROOT, filename)
    mime = "application/octet-stream"
    today_folder = datetime.now().strftime("%Y-%m-%d")
    cache.set("date_save_video", today_folder, timeout=0)

    # Remove object name for saving format
    data_to_save = dict(request.data)
    data_to_save.pop("objectName", None)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False)    

    minio_service = MinIOService()
    try:
        print("=======================")
        print(path)
        result = minio_service.upload_to_minio(path, f"mediapipe/{today_folder}/{filename}", mime)
        if not result.get("success"):
            return standard_response(message=f"Upload failed: {result.get('error')}",
                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Upload successful")
    except Exception as e:
        return standard_response(message=f"Upload failed: {e}",
                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return standard_response(
        data={"capture_id": request.data.get("objectName"), "filename": filename, "path": path},
        message="capture saved",
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def text_to_speech(request):
    try:
        text = request.GET.get("text", None)
        data, status_code = googleGenAIService.tts_stream(text)

        if (status_code == status.HTTP_200_OK):
            response = StreamingHttpResponse(data, content_type="audio/mpeg")
            response["Cache-Control"] = "no-cache"
            return response

        return Response(data, status_code)
    except requests.exceptions.RequestException as e:
        error_details = {
            "error_message": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        return Response(error_details, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_training_word_feedback(request):
    serializer = TrainingWordFeedbackSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        with transaction.atomic():
            obj = serializer.save()
    except IntegrityError:
        # hit unique constraint (word or word,key)
        return Response(
            {"detail": "Feedback for this word already exists."},
            status=status.HTTP_409_CONFLICT
        )
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_learning_status(request):
    try:
        user = request.user

        total_lessons = Lesson.objects.filter(is_deleted=False).count()
        
        completed_lessons = UserLessons.objects.filter(
            user=user,
            status='completed'
        ).count()

        completed_sections = UserLessons.objects.filter(user=user).aggregate(
            total=Sum('completed_signs')
        )['total'] or 0

        elementary_total = Lesson.objects.filter(level="elementary", is_deleted=False).count()
        intermediate_total = Lesson.objects.filter(level="intermediate", is_deleted=False).count()

        elementary_done = UserLessons.objects.filter(
            user=user,
            lesson__level="elementary",
            status="completed"
        ).count()

        intermediate_done = UserLessons.objects.filter(
            user=user,
            lesson__level="intermediate",
            status="completed"
        ).count()

        if elementary_done < elementary_total:
            level = "elementary"
        else:
            if intermediate_total == 0:
                level = "intermediate"
            else:
                intermediate_ratio = intermediate_done / intermediate_total

                if intermediate_ratio < 0.67:
                    level = "intermediate"
                else:
                    level = "advanced"

        return Response({
            "learnedWords": completed_sections,
            "totalLessons": total_lessons,
            "completedLessons": completed_lessons,
            "level": level
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print("Exception in get_learning_status:")
        return Response({"detail": "Internal server error"}, status=500)
# endregion

# region search and filter lessons for user
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def lessons_search_view(request):
#     # user = request.user
#     user = User.objects.get(id=16)
#     query_params = request.query_params  
#     print("Query Params:", query_params)
#     lessons_list = search_lessons_for_user(query_params, user)
#     print("Lessons List:", lessons_list)
#     serializer = LessonListItemSerializer(lessons_list, many=True)
#     return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def lessons_search_view(request):
    user = request.user
    query_params = request.query_params  

    lessons_list = search_lessons_for_user(query_params, user)

    serializer = LessonListItemSerializer(lessons_list, many=True)

    return Response(serializer.data)
# endregion

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def mark_word(request):
    user = request.user
    
    # Merge query params và body data
    data = {**request.query_params.dict(), **request.data}
    
    result = mark_word_completed(data, user)
    if result.get("error"):
        return Response(result, status=result.get("status", 400))
    return Response(result, status=200)


# region API endpoint for notebook feature
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_notebook(request):
    """
    GET: Return all noted sections of current user.
    Response: {"sections": [...]}
    """
    try:
        user = request.user

        # GET: Return all noted sections
        user_sections = UserSections.objects.filter(
            user=user,
            is_user_noted=True,
            is_deleted=False
        ).select_related('section', 'lesson')

        sections_data = []
        for us in user_sections:
            s = us.section
            if s and not s.is_deleted:
                try:
                    score = int(us.score) if us.score is not None else 0
                except:
                    score = 0

                sections_data.append({
                    "id": s.id,
                    "content": s.sign or s.content or "",
                    "description": s.content or "",
                    "tip": s.tips or "",
                    "is_user_noted": bool(us.is_user_noted),
                    "video_url": s.video_url or "",
                })

        return Response({"sections": sections_data}, status=status.HTTP_200_OK)

    except Exception as e:
        return standard_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def manage_user_notebook(request):
    """
    POST/PUT: Create or update notebook entry
    - section_id (required): Used to filter if record exists
    - score, is_user_noted, status: Fields to update or set
    """
    try:
        user = request.user
        section_id = request.data.get('section_id')

        if not section_id:
            return standard_response(status=status.HTTP_400_BAD_REQUEST, message="Missing section_id")

        # Validate section exists
        try:
            section = Section.objects.get(pk=section_id, is_deleted=False)
        except Section.DoesNotExist:
            return standard_response(status=status.HTTP_404_NOT_FOUND, message="Section not found")

        # Filter by section_id AND current user_id to check if record exists
        existing_us = UserSections.objects.filter(
            user=user,  # Current authenticated user
            section=section,  # Section from section_id
            is_deleted=False
        ).first()

        if existing_us:
            # UPDATE existing record with any fields provided
            if 'score' in request.data:
                existing_us.score = request.data.get('score')
            
            if 'is_user_noted' in request.data:
                existing_us.is_user_noted = request.data.get('is_user_noted')
            
            if 'status' in request.data:
                existing_us.status = request.data.get('status')
            
            existing_us.update_by = user
            existing_us.save()

            data = {
                'id': existing_us.id,
                'user_id': existing_us.user_id,
                'section_id': existing_us.section_id,
                'lesson_id': existing_us.lesson_id,
                'score': float(existing_us.score),
                'status': existing_us.status,
                'is_user_noted': bool(existing_us.is_user_noted)
            }

            return standard_response(status=status.HTTP_200_OK, message="Updated successfully", data=data)
        
        else:
            # CREATE new record with provided fields or defaults
            us = UserSections.objects.create(
                user=user,
                section=section,
                lesson=section.lesson,
                score=request.data.get('score', 0.0),
                status=request.data.get('status', 'inprogress'),
                is_user_noted=request.data.get('is_user_noted', True),
                create_by=user,
                update_by=user
            )

            data = {
                'id': us.id,
                'user_id': us.user_id,
                'section_id': us.section_id,
                'lesson_id': us.lesson_id,
                'score': float(us.score),
                'status': us.status,
                'is_user_noted': bool(us.is_user_noted)
            }

            return standard_response(status=status.HTTP_201_CREATED, message="Created", data=data)

    except Exception as e:
        return standard_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
# endregion