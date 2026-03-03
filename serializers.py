from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from .messages import *

class PredictionResultSerializer(serializers.Serializer):
    Class = serializers.CharField()
    Accuracy = serializers.FloatField()

class InputLLMSerializer(serializers.Serializer):
    inputs = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

class UserSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='username')
    password = serializers.CharField(write_only=True)
    userType = serializers.CharField(source='user_type')
    
    class Meta:
        model = User
        fields = ['id', 'userName', 'password', 'userType']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def to_internal_value(self, data):
        data = {
            'userName': data.get('Username'),
            'password': data.get('Password'),
            'userType': data.get('UserType')
        }
        return super().to_internal_value(data)    
    
    def validate(self, data):
        allowed_types = ['doctor', 'deaf', 'normal']
        if data.get('user_type') not in allowed_types:
            raise serializers.ValidationError(ErrorMessages.VALIDATE_USER_TYPE)
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            user_type=validated_data['user_type'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GetUserInfoSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source='user.user_type', read_only=True)
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'full_name', 'email', 'avatar', 'user_type']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'       

class SignPoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignPose
        fields = '__all__' 

class UserProfileSerializer(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type', 'date_joined', 'userinfo']     

    def get_userinfo(self, obj):
        serializer = UserInfoSerializer(obj.userinfo)
        return {
            'full_name': serializer.data['full_name'],
            'phone': serializer.data['phone'],
            'email': serializer.data['email'],
            'avatar': serializer.data['avatar'],
            'address': serializer.data['address'],
            'date_of_birth': serializer.data['date_of_birth'],
            'gender': serializer.data['gender']
        }       
class UserUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='userinfo.full_name', required=True)
    phone = serializers.CharField(source='userinfo.phone',required=False, allow_null = True, allow_blank = True)
    email = serializers.EmailField(source='userinfo.email', required=True)
    avatar = serializers.CharField(source='userinfo.avatar', required=True, allow_null=True)
    address = serializers.CharField(source='userinfo.address', required=False, allow_null = True, allow_blank = True)
    date_of_birth = serializers.DateField(source='userinfo.date_of_birth', required=True, allow_null=True)
    gender = serializers.CharField(source='userinfo.gender', required=True)
    
    class Meta:
        model = User
        fields = ['user_type', 'full_name', 'phone', 'email', 'avatar', 
                'address', 'date_of_birth', 'gender']

    def update(self, instance, validated_data):
        # Tách dữ liệu UserInfo từ validated_data
        userinfo_data = {
            'full_name': validated_data.get('userinfo', {}).get('full_name'),
            'phone': validated_data.get('userinfo', {}).get('phone'),
            'email': validated_data.get('userinfo', {}).get('email'),
            'avatar': validated_data.get('userinfo', {}).get('avatar'),
            'address': validated_data.get('userinfo', {}).get('address'),
            'date_of_birth': validated_data.get('userinfo', {}).get('date_of_birth'),
            'gender': validated_data.get('userinfo', {}).get('gender')
        }

        # Cập nhật User
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.save()

        # Cập nhật UserInfo
        userinfo = instance.userinfo
        for attr, value in userinfo_data.items():
            if isinstance(value, str) and value.strip() == "":
                value = None
            setattr(userinfo, attr, value)
        userinfo.save()

        return instance
    
class FriendRequestSerializer(serializers.ModelSerializer):
    sender_info = serializers.SerializerMethodField()
    receiver_info = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'sender_info', 'receiver', 'receiver_info', 'status', 'created_at']
        read_only_fields = ['sender', 'receiver', 'created_at']

    def get_sender_info(self, obj):
        user_info = UserInfo.objects.get(user=obj.sender)
        return {
            'id': obj.sender.id,
            'username': obj.sender.username,
            'full_name': user_info.full_name,
            'avatar': user_info.avatar
        }

    def get_receiver_info(self, obj):
        user_info = UserInfo.objects.get(user=obj.receiver)
        return {
            'id': obj.receiver.id,
            'username': obj.receiver.username,
            'full_name': user_info.full_name,
            'avatar': user_info.avatar
        }

class FriendSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'user_type', 'username', 'user_info']

    def get_user_info(self, obj):
        user_info = UserInfo.objects.get(user=obj)
        return {
            'full_name': user_info.full_name,
            'avatar': user_info.avatar
        }    
    
class FriendRequestDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    is_own_request = serializers.SerializerMethodField()  
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'status', 'created_at', 'user_id', 'user_info', 'is_own_request']
    
    def get_is_own_request(self, obj):
        request = self.context.get('request')
        return obj.sender == request.user  
    
    def get_user_id(self, obj):
        request = self.context.get('request')
        return obj.sender.id if obj.receiver == request.user else obj.receiver.id
    
    def get_user_info(self, obj):
        request = self.context.get('request')
        other_user = obj.sender if obj.receiver == request.user else obj.receiver
        user_info = UserInfo.objects.get(user=other_user)
        return {
            'username': other_user.username,
            'full_name': user_info.full_name,
            'avatar': user_info.avatar,
            'user_type': other_user.user_type
        }    
    
class FriendUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['full_name', 'avatar']    

class FriendUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='userinfo.full_name', read_only=True)
    avatar = serializers.CharField(source='userinfo.avatar', read_only=True, allow_null=True)

    conversation_id = serializers.IntegerField(read_only=True)
    last_message_content = serializers.CharField(read_only=True)
    last_message_sent_at = serializers.DateTimeField(read_only=True)
    unread_count = serializers.IntegerField(read_only=True)
    is_pinned = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'user_type', 'full_name', 'avatar',
            'conversation_id', 'last_message_content', 'last_message_sent_at', 'unread_count', 'is_pinned'
        ]   

class FriendRequestSerializer(serializers.ModelSerializer):
    user = FriendUserSerializer(source='receiver', read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'user', 'status']        

class ReceivedRequestSerializer(serializers.ModelSerializer):
    user = FriendUserSerializer(source='sender', read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'user', 'status']        

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_username', 'sender_avatar', 'content', 'sent_at', 'is_read']

    def get_sender_avatar(self, obj):
        return obj.sender.userinfo.avatar if hasattr(obj.sender, 'userinfo') else None
    
class TrainingWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingWord
        fields = "__all__"


class TrainingWordFeedbackSerializer(serializers.ModelSerializer):
    key = serializers.CharField(write_only=True)
    word_name = serializers.CharField(source='word.key', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TrainingWordFeedback
        fields = ['id', 'key', 'word_name', 'feedback', 'created_at']
        read_only_fields = ['id', 'created_at', 'word_name']

    def create(self, validated_data):
        k = validated_data.pop('key')

        try:
            word_obj = TrainingWord.objects.get(key=k)   # <-- use 'word'
        except TrainingWord.DoesNotExist:
            raise serializers.ValidationError({"key": f"'{k}' does not exist in TrainingWord."})
        
        return TrainingWordFeedback.objects.create(
            word=word_obj,
            feedback=validated_data['feedback']
        )

class ElementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField(allow_blank=True)  # legacy field
    description = serializers.CharField(allow_blank=True, required=False, default="")
    tip = serializers.CharField(allow_blank=True, required=False, default="")
    score = serializers.IntegerField(min_value=0, default=0)
    video_url = serializers.CharField(allow_blank=True, required=False, default="")
    answers = serializers.ListField(child=serializers.CharField(), required=False, default=list)

    def validate_score(self, value):
        """
        Ensure score is non-negative integer.
        """
        if value is None:
            return 0
        return int(value)
class LessonListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False, default="")
    level = serializers.CharField()
    image_url = serializers.CharField(allow_blank=True, required=False, default="")
    # progress stored as float between 0 and 1
    progress = serializers.FloatField(min_value=0.0, max_value=1.0, default=0.0)
    elements = ElementSerializer(many=True, default=list)

    def validate_progress(self, value):
        if value is None:
            return 0.0
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise serializers.ValidationError("Progress must be a number between 0 and 1.")
        if val < 0 or val > 1:
            raise serializers.ValidationError("Progress must be between 0 and 1.")
        # round to 2 decimal places for consistent output
        return round(val, 2)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # make sure 'elements' exists and is a list
        if "elements" not in ret or ret["elements"] is None:
            ret["elements"] = []
        # ensure progress is float
        ret["progress"] = float(ret.get("progress", 0.0))
        return ret


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'company', 'country', 'phone', 'inquiry', 'created_date', 'updated_date']
        read_only_fields = ['id', 'created_date', 'updated_date']


class ConversationElearningSerializer(serializers.ModelSerializer):
    answer_id = serializers.PrimaryKeyRelatedField(
        source='answer',
        queryset=ConversationElearning.objects.all(),
        required=False,
        allow_null=True
    )
    lesson_id = serializers.PrimaryKeyRelatedField(
        source='lesson',
        queryset=Lesson.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = ConversationElearning
        fields = ['id', 'message', 'type', 'answer_id', 'order_index', 'lesson_id']
        read_only_fields = ['id']

    def validate(self, attrs):
        # Get message_type and answer_obj from input data or existing instance
        message_type = attrs.get('type', getattr(self.instance, 'type', None))
        answer_obj = attrs.get('answer', getattr(self.instance, 'answer', None))

        # Rule 1: An ANSWER type record should not point to another answer_id
        if message_type == ConversationElearning.MessageType.ANSWER and answer_obj is not None:
            raise serializers.ValidationError({
                'answer_id': 'Records of type "answer" cannot have an answer_id.'
            })

        # Rule 2: A QUESTION type record must point to a record of type "answer"
        if message_type == ConversationElearning.MessageType.QUESTION and answer_obj is not None:
            if answer_obj.type != ConversationElearning.MessageType.ANSWER:
                raise serializers.ValidationError({
                    'answer_id': 'The answer_id must point to a record with type "answer".'
                })

        return attrs

class ConversationKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationKeyword
        fields = ['id', 'conversation', 'keyword_text', 'position']

    def validate_position(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Position cannot be a negative number.")
        return value

class UserConversationKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConversationKeyword
        fields = ['id', 'user', 'conversation', 'conversation_keyword', 'status', 'last_practiced_at']

    def validate(self, attrs):
        conv = attrs.get('conversation')
        kw = attrs.get('conversation_keyword')

        # Check: The keyword must belong to the selected conversation
        if conv and kw and kw.conversation_id != conv.id:
            raise serializers.ValidationError({
                'conversation_keyword': 'This keyword does not belong to the selected conversation.'
            })
        
        return attrs

class UserConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConversation
        fields = ['id', 'user', 'conversation', 'progress', 'status', 'updated_at']

    def validate_progress(self, value):
        # Valid progress must be between 0 and 100
        if value < 0 or value > 100:
            raise serializers.ValidationError("Progress must be between 0 and 100.")
        return value

    def validate(self, attrs):
        # Auto-update status based on progress value
        progress = attrs.get('progress')
        if progress is not None:
            if progress == 100:
                attrs['status'] = 'completed'
            elif progress > 0:
                attrs['status'] = 'in_progress'
            else:
                attrs['status'] = 'not_started'
        return attrs