# tasks/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.template.loader import render_to_string
from .models import Task
import json
from datetime import date


@login_required
def task_board(request):
    tasks = Task.objects.filter(user=request.user)

    context = {
        'todo': tasks.filter(status='todo').order_by('order', 'created_at'),
        'inprogress': tasks.filter(status='inprogress').order_by('order', 'created_at'),
        'done': tasks.filter(status='done').order_by('order', 'created_at'),
        'today': date.today(),
    }
    return render(request, 'tasks/board.html', context)


@require_POST
@login_required
def task_create(request):
    try:
        data = json.loads(request.body)
        task = Task.objects.create(
            user=request.user,
            title=data.get('title', '').strip() or "Untitled Task",
            description=data.get('description', ''),
            status=data.get('status', 'todo'),
            priority=data.get('priority', 'medium'),
            color=data.get('color', '#00D4FF'),
            deadline=data.get('deadline') or None,
            order=Task.objects.filter(user=request.user, status=data.get('status', 'todo')).count(),
        )
        # in task_create and task_update
        return JsonResponse({
            'success': True,
            'status': task.status,           # ← important!
            'html': render_to_string(
                'tasks/partials/task_card.html',
                {'task': task, 'today': date.today()},
                request=request
            )
         })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    try:
        data = json.loads(request.body)
        for k, v in data.items():
            if k == 'deadline':
                task.deadline = v or None
            elif k in ['title', 'description', 'priority', 'color', 'status']:
                setattr(task, k, v)
        task.save()
        return JsonResponse({
            'success': True,
            'html': render_to_string('tasks/partials/task_card.html', {
                'task': task,
                'today': date.today()
            }, request=request)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["DELETE"])
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.delete()
    return JsonResponse({'success': True})


@require_POST
@login_required
def task_reorder(request):
    try:
        groups = json.loads(request.body)
        for status, task_ids in groups.items():
            for idx, pk_str in enumerate(task_ids):
                task = get_object_or_404(Task, pk=int(pk_str), user=request.user)
                task.status = status
                task.order = idx
                task.save(update_fields=['status', 'order'])
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)