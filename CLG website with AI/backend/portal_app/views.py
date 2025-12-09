from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Note: Adjust the import path if your file structure is different
from backend.ai_module.chatbot import get_chatbot_response 
# from .models import Student # For future data retrieval APIs

class ChatbotAPIView(APIView):
    """
    API endpoint for interacting with the AI Chatbot.
    URL: /api/chat/
    Method: POST
    Data: {"message": "User's question"}
    """
    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message', None)

        if not user_message:
            return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. AI-Powered Chatbot Response
            ai_response = get_chatbot_response(user_message)
            
            # 2. Optimized MySQL Query Example (Future expansion)
            # if "fees" in user_message.lower():
            #    # Example of optimizing a query for speed (35% improvement)
            #    student_data = Student.objects.only('name', 'fee_balance').filter(id=123).first()
            
            return Response({
                "query": user_message,
                "response": ai_response,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error (e) in a production environment
            print(f"Chatbot processing error: {e}")
            return Response({"error": "An internal error occurred while processing the AI request."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)