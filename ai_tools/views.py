import json
import urllib.parse
import base64

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import google.generativeai as genai


# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


# DASHBOARD
def dashboard(request):
    return render(request, "ai_tools/dashboard.html")


# ---------------- SUMMARIZATION ----------------

@csrf_exempt
def summarize(request):

    if request.method == "POST":

        data = json.loads(request.body)
        text = data.get("text")

        prompt = f"Summarize the following text:\n{text}"

        response = model.generate_content(prompt)

        return JsonResponse({
            "result": response.text
        })


# ---------------- TRANSLATION ----------------

@csrf_exempt
def translate(request):

    if request.method == "POST":

        data = json.loads(request.body)

        text = data.get("text")
        target = data.get("target")

        prompt = f"Translate the following text to {target}:\n{text}"

        response = model.generate_content(prompt)

        return JsonResponse({
            "result": response.text
        })


# ---------------- CONTENT GENERATION ----------------

@csrf_exempt
def generate_content(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            response = model.generate_content(
                prompt,
                request_options={"timeout": 30}
            )

            return JsonResponse({
                "result": response.text
            })

        except Exception as e:
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

        response = model.generate_content(prompt)

        return JsonResponse({
            "result": response.text
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

        response = model.generate_content([
            prompt,
            {
                "mime_type": file.content_type,
                "data": image_bytes
            }
        ])

        return JsonResponse({
            "result": response.text
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