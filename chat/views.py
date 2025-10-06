from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


@csrf_exempt
@require_http_methods(["GET", "POST"])
def chat_view(request):
    if request.method == "GET":
        return render(request, "chat/index.html")

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            user_question = data.get("question", "").strip()

            if not user_question:
                return JsonResponse({"error": "Please provide a question"}, status=400)

            # Get OpenAI API key
            openai_api_key = os.getenv("OPENAI_API_KEY")

            if not openai_api_key or openai_api_key == "your_openai_api_key_here":
                return JsonResponse({"error": "OpenAI API key not configured"}, status=500)

            # Initialize OpenAI client
            client = OpenAI(api_key=openai_api_key)

            # Create messages for the chat completion
            messages = [{"role": "user", "content": user_question}]

            # Get response from OpenAI
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            ai_response = response.choices[0].message.content

            return JsonResponse({"question": user_question, "answer": ai_response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error processing request: {str(e)}"}, status=500)
