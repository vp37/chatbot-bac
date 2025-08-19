from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDsTCRC32wwAEhKjFoE5RHQlJ53X570-cY")

# Finance Role Prompt
BOT_PROMPT = """

- Speak in a friendly, helpful tone.
- Keep responses short unless asked for details.
- If the user asks about **real-time information** (like stock prices, currency rates, weather, news, etc.):
    - Clearly explain that you cannot fetch live data directly.
    - Suggest reliable external sources (Google Finance, Yahoo Finance, Weather apps, News portals).
- You can still provide **general explanations, trends, and financial concepts**.
- If you don’t know something, admit it instead of making up.
"""

@method_decorator(csrf_exempt, name='dispatch')
class FinanceChatBotView(View):

    def post(self, request):
        try:
            body = json.loads(request.body)
            user_message = body.get("message")

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([
                BOT_PROMPT,
                f"User: {user_message}"
            ])

            return JsonResponse({"reply": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
