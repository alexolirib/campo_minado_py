import math

from django.shortcuts import render, redirect
from django.utils import timezone

from app.forms import JogadaForm
from app.models import Jogada, Game


def start_game(request):
    if request.method == 'GET':
        return render(request, 'init_game.html')
    if request.method == 'POST':
        game = Game.criar_novo_game()

        return redirect('play_game', pk=game.id)

def play_game(request, pk=None):
    try:
        game = Game.objects.get(id=pk)
    except:
        return redirect('init_game')

    if request.method == "GET":
        form = JogadaForm()

    if request.method == "POST":
        form = JogadaForm(request.POST)
        if form.is_valid():
            jogada = form.save(commit=False)
            jogada.created_date = timezone.now()
            jogada.save()
    else:
        form = JogadaForm()

    jogadas = Jogada.objects.all()

    loop_time = range(1,int(math.pow(game.tamanho,1/2)+1))

    context = {
        'form': form,
        'jogadas': jogadas,
        'loop_time': loop_time
    }

    return render(request, 'game.html', context)