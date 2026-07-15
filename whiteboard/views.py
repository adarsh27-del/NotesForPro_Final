from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def whiteboard_canvas(request):
    return render(request, 'whiteboard/canvas.html')   # ← important: with 'whiteboard/'

