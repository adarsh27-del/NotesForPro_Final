# games/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
from .models import GameScore

TYPING_QUOTES = [
    "The quick brown fox jumps over the lazy dog.",
    "Practice makes perfect in everything you do.",
    "Success is the sum of small efforts repeated day in and day out.",
    "Code is like humor. When you have to explain it, it's bad.",
    "Keep calm and keep typing faster every day."
]

@login_required
def typing_game(request):
    # Pick a random quote to start
    quote = random.choice(TYPING_QUOTES)
    request.session['current_quote'] = quote
    return render(request, 'games/typing.html', {'quote': quote})

@login_required
def typing_game_check(request):
    if request.method == 'POST':
        typed = request.POST.get('typed', '').strip()
        time_taken = float(request.POST.get('time', 20))  # seconds
        current_quote = request.session.get('current_quote', '')
        
        words_typed = len(typed.split())
        wpm = round(words_typed / (time_taken / 60)) if time_taken > 0 else 0

        correct_chars = sum(1 for i in range(min(len(typed), len(current_quote))) if typed[i] == current_quote[i])
        accuracy = round((correct_chars / len(current_quote)) * 100) if current_quote else 100

        # Save score
        score = wpm
        GameScore.objects.create(
            user=request.user,
            game_type='typing',
            score=score,
            details={'wpm': wpm, 'accuracy': accuracy, 'time': time_taken, 'typed': typed, 'quote': current_quote}
        )

        # Pick next quote
        new_quote = random.choice(TYPING_QUOTES)
        request.session['current_quote'] = new_quote

        return JsonResponse({'wpm': wpm, 'accuracy': accuracy, 'new_quote': new_quote})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def chess_game(request):
    return render(request,'games/chess.html')