from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

import json
from .models import Note


@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'notes/list.html', {'notes': notes})


@login_required
def note_detail(request, note_id=None):
    note = None
    if note_id:
        note = get_object_or_404(Note, id=note_id, user=request.user)
    return render(request, 'notes/detail.html', {'note': note})


@require_POST
@login_required
def note_save(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        title = (data.get('title') or '').strip() or 'Untitled'
        content_html = data.get('content_html') or ''
        note_id = data.get('note_id')

        # convert empty string → None
        if not note_id:
            note_id = None

        if note_id:
            note = get_object_or_404(Note, id=int(note_id), user=request.user)
            note.title = title
            note.content_html = content_html
            note.save()
        else:
            note = Note.objects.create(
                user=request.user,
                title=title,
                content_html=content_html
            )

        return JsonResponse({
            'success': True,
            'note_id': note.id
        })

    except Exception as e:
        print("SAVE ERROR:", str(e))
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_POST
@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return JsonResponse({'success': True})