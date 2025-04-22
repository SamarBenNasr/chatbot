from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.http import JsonResponse
from django.shortcuts import render
# Initialize the chatbot
# views.py
from django.http import JsonResponse
from django.shortcuts import render
# chatbot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from langchain.schema import HumanMessage
from .chat_logic import get_answer, select_llm

llm = select_llm()  # Instancier une fois au chargement

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            response = get_answer(llm, user_message)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == "GET":
        return JsonResponse({"message": "Welcome to the chatbot API. Please send a POST request with your message."})
    return JsonResponse({"error": "Invalid request"}, status=400)




def main(request):
  template = loader.get_template('chatbot.html')
  return HttpResponse(template.render())

