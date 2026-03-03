
API 

1) lấy conversation
- Method: GET
- Path: /api/v1/api/e-learning/get_conversation_lessons
- Req:
{
    "lesson_id": 1
}
- Res:
{
    "Questions": [
        {
            "id": 1,
            "message": "Hello how are you?",
            "order_index": 1,
            "answer": "I am fine, thank you!"
            "has_do":
            {
                "total_score": 4,
                "score": 3,
                "status": "success",
                "progress": 0.9,
                "keywords": 
                [
                    { "conversation_keyword_id": 2,"keyword_text": "How", "status": "success" },
                    { "conversation_keyword_id": 3,"keyword_text": "Hello", "status": "failed" },
                ]
            }
        },
        {
            "id": 3,
            "message": "What is your name?",
            "order_index": 2,
            "answer": "My name is Gemini."
            "has_do": null

        },
    ]
}


2) check và lưu/cập nhật conversation và từng keyword
- Method: POST
- Path: /api/v1/api/e-learning/update_user_conversation
- Req:
{
    "conversation_id": 1,
    "keywords": [
        {
            "word": "tôi",
            "position": 1
        },
        {
            "word": "là",
            "position": 2
        }
    ]
}
- Res: 
{
    "status": 200,
    "message": "User Conversation and Lesson progress updated successfully",
    "data": {
        "saved_conversations":[
            "conversation_id": 1,
            "progress": 0.9,
            "status": "success",
            "lesson_overall_progress": 0.9,
            "updated_at": ....,
            "saved_keywords": [
                {
                    "keyword_id": 20, 
                    "status": "success"
                },
                {
                    "keyword_id": 3,
                    "status": "failed"
                }
            ]
        ]
    }
}


3) xóa all conv 
- Method: DELETE
- Path: v1/api/e-learning/delete_user_conversation (delete all)
- Path: v1/api/e-learning/update_user_conversation?conversation_id=1 (delete each conversation)
- Req:
{
    "lesson_id": 1
}
- Res:
{
    "status": 200,
    "message": "Conversation 5 in lesson 1 deleted successfully." (delete all)
    "message": "All progress for lesson 2 has been reset." (delete each conversation)
}