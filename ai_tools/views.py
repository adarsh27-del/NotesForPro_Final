import json
import urllib.parse
import base64
import traceback
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY

def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek/deepseek-chat-v3-0324",
        "messages": [
            {
                "role": "user",
                "content": str(prompt)
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=120
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
# ---------------- DASHBOARD ----------------

def dashboard(request):
    return render(request, "ai_tools/dashboard.html")


# ---------------- SUMMARIZATION ----------------

@csrf_exempt
def summarize(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text")

        prompt = f"Summarize the following text:\n{text}"

        result = ask_openrouter(prompt)

        return JsonResponse({
            "result": result
        })


# ---------------- TRANSLATION ----------------

@csrf_exempt
def translate(request):
    if request.method == "POST":
        data = json.loads(request.body)

        text = data.get("text")
        target = data.get("target")

        prompt = f"Translate the following text to {target}:\n{text}"

        result = ask_openrouter(prompt)

        return JsonResponse({
            "result": result
        })


#--------------- CONTENT GENERATION ----------------

@csrf_exempt
def generate_content(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            prompt = data.get("prompt")

            result = ask_openrouter(prompt)

            return JsonResponse({
                "result": result
            })

        except Exception as e:
            traceback.print_exc()

            return JsonResponse({
                "error": str(e)
            }, status=500)
# ---------------- MEETING NOTES ----------------

@csrf_exempt
def meeting_notes(request):

    if request.method == "POST":

        data = json.loads(request.body)

        transcript = data.get("text")

        prompt = f"""
        Convert the following meeting transcript into structured meeting notes
        with bullet points and action items:

        {transcript}
        """

        result = ask_openrouter(prompt)

        return JsonResponse({
            "result": result
        })


# ---------------- OCR ----------------

@csrf_exempt
def ocr(request):

    if request.method == "POST":

        file = request.FILES.get("file")

        if not file:
            return JsonResponse({"result": "No file uploaded"}, status=400)

        image_bytes = file.read()

        prompt = "Extract all text from this image."

        result = ask_openrouter([
            prompt,
            {
                "mime_type": file.content_type,
                "data": image_bytes
            }
        ])

        return JsonResponse({
            "result": result
        })


# ---------------- IMAGE GENERATION (Pollinations) ----------------

@csrf_exempt
def generate_image(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            prompt = data.get("prompt")
            model_name = data.get("model", "turbo")
            style = data.get("style", "realistic")

            final_prompt = f"{prompt}, {style}"

            encoded_prompt = urllib.parse.quote(final_prompt)

            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model={model_name}"

            return JsonResponse({
                "success": True,
                "image_url": image_url
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }) 