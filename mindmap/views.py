from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

import json
import base64
import os
import uuid

import requests
import graphviz

from .models import MindMap


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

@login_required
def generator(request):
    return render(request, "mindmap/generator.html")


@require_POST
@login_required
def generate(request):

    try:
        data = json.loads(request.body)
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return JsonResponse({
                "success": False,
                "error": "Prompt cannot be empty"
            })

        # ------------------------
        # OPENROUTER REQUEST
        # ------------------------

        ai_prompt = f"""
You are an AI that generates ONLY valid JSON.

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.

Topic:
{prompt}

Format:

{{
    "central_concept":"topic",
    "branches":[
        {{
            "title":"branch",
            "points":["p1","p2","p3"]
        }}
    ]
}}
"""

        text = ask_openrouter(ai_prompt)

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        structure = json.loads(text)
        central = structure["central_concept"]

        # ------------------------
        # GRAPHVIZ GENERATION
        # ------------------------

        dot = graphviz.Digraph(
            format="svg",
            graph_attr={
                "rankdir": "LR",
                "bgcolor": "#0f172a"
            },
            node_attr={
                "fontcolor": "white",
                "color": "#38bdf8",
                "fontname": "Arial"
            },
            edge_attr={
                "color": "#38bdf8"
            }
        )

        dot.node("central",
                 shape="ellipse",
                 style="filled",
                 fillcolor="#06b6d4",
                fontcolor="black")

        for i, branch in enumerate(structure["branches"]):

            branch_id = f"branch{i}"

            dot.node(branch_id,
                branch["title"],
                shape="box",
                style="filled,rounded",
                fillcolor="#1e293b",
                fontcolor="white")

            dot.edge("central", branch_id)

            for j, point in enumerate(branch["points"]):

                point_id = f"{branch_id}_{j}"

                dot.node(point_id,
                        point,
                        shape="box",
                        fontcolor="white")

                dot.edge(branch_id, point_id)

        filename = f"mindmap_{uuid.uuid4().hex}"

        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        dot.render(filepath, cleanup=True)

        svg_path = filepath + ".svg"

        with open(svg_path, "rb") as f:
            svg_data = f.read()

        encoded_svg = base64.b64encode(svg_data).decode()

        # ------------------------
        # SAVE TO DATABASE
        # ------------------------

        MindMap.objects.create(
            user=request.user,
            title=prompt[:100],
            central=central,
            structure_json=structure,
            svg_content=encoded_svg
        )

        return JsonResponse({
            "success": True,
            "svg": encoded_svg
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })