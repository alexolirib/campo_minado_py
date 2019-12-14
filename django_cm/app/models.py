from random import randint

from django.db import models
from django.utils import timezone

class Game(models.Model):
    tamanho = models.IntegerField()
    bombas = models.CharField(max_length=100)
    created_date = models.DateField(default=timezone.now)
    ended_date = models.DateField(null=True)

    @staticmethod
    def criar_novo_game(tamanho=8):
        game = Game()
        game.tamanho = tamanho ** 2
        game.bombas = game.criar_bombas()
        game.save()
        return game

    def criar_bombas(self, area_bomba=20):

        porc_bomba = area_bomba / 100
        qtd_bomba = int(self.tamanho * porc_bomba)

        list_bombas = []

        while qtd_bomba > 0:
            self.verificar_posicao_bomba(posicao=randint(1, self.tamanho), list_bombas=list_bombas)
            qtd_bomba -= 1
        return list_bombas

    def verificar_posicao_bomba(self, posicao, list_bombas):
        if posicao in list_bombas:
            if posicao == self.tamanho:
                posicao = 0
            posicao += 1

            self.verificar_posicao_bomba(posicao, list_bombas)
            return
        list_bombas.append(posicao)

class Jogada(models.Model):
    linha = models.CharField(max_length=2)
    coluna = models.CharField(max_length=2)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)