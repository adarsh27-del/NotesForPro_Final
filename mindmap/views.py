from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

import json
import base64
import os
import uuid

import google.generativeai as genai
import graphviz

from .models import MindMap


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


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
        # GEMINI REQUEST
        # ------------------------

        model = genai.GenerativeModel("gemini-2.5-flash")

        gemini_prompt = f"""
        You are a JSON generator.

        Return ONLY valid JSON.

        Topic: {prompt}

        Format:

        {{
        "central_concept": "topic",
        "branches":[
            {{
            "title":"branch",
            "points":["p1","p2","p3"]
            }}
        ]
        }}

        DO NOT include explanation or markdown.
        """

        response = model.generate_content(gemini_prompt)

        text = response.text.strip()

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