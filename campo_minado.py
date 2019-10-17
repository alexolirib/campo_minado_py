from random import randint
import time
import numpy as np


class CampoMinado:

    def __init__(self, tamanho=8):
        self.borda = tamanho
        self.tamanho = tamanho ** 2
        # vai para falso quando for Game Over e True quando for fim de jogo
        self.bombas = self.criar_bombas()
        print(f"posição bombas -> {self.bombas}")
        self.jogada_feitas = []
        self.next_game = True
        self.status = None
        self.message = None
        self.valor_qt_bomba_campo = None
        self.display = self.create_display_game(tamanho)
        self.display_campo_minado()

    def display_campo_minado(self):
        for display in self.display:
            print(display)

    def create_display_game(self, tamanho):
        np_campos = np.chararray((tamanho, tamanho), unicode=True)
        np_campos[:] = 'X'
        return np_campos.tolist()

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

    def obter_posicao_jogada(self, linha, coluna):
        linha = linha - 1
        posicao_jogada = (linha * self.borda) + coluna
        return posicao_jogada

    def update_message(self, message=None, valor_qt_bomba_campo=None, status=None):
        self.message = message
        self.valor_qt_bomba_campo = valor_qt_bomba_campo
        self.status = status
        self.display_campo_minado()
        if isinstance(status, bool):
            self.next_game = False

    def jogada(self, linha, coluna):
        if not self.next_game:
            return
        if (linha < 1 or linha > self.borda) or (coluna < 1 or coluna > self.borda):
            self.update_message(message="Jogada incorreta, tente novamente")
            return

        posicao_jogada = self.obter_posicao_jogada(linha, coluna)
        print(f'posicao - >{posicao_jogada}')
        if posicao_jogada in self.jogada_feitas:
            self.update_message(message="Jogada incorreta, campo já selecionado")
            return
        self.jogada_feitas.append(posicao_jogada)
        if posicao_jogada in self.bombas:
            self.exibir_bombas()
            self.update_message(message="GAME OVER", status=False)
            return

        if len(self.bombas) + len(self.jogada_feitas) == self.tamanho:
            self.update_message(message="PARABENS VOCÊ GANHOU", status=True)
            return

        return self.update_message(
            valor_qt_bomba_campo=self.verificar_qts_bombas_redor(linha, coluna),
            message='Faça sua Próxima jogada!\n\n'
        )

    def exibir_bombas(self):
        for bomba in self.bombas:
            linha_coluna = self.posicao_para_coordenada(bomba)
            self.alterar_display_game(
                linha=linha_coluna['linha'],
                coluna=linha_coluna['coluna'],
                count_bombas='B'
            )

    def posicao_para_coordenada(self, posicao):
        linha = int(posicao/self.borda) + 1
        coluna = posicao - ((linha-1)*self.borda)

        if coluna == 0:
            linha = linha - 1
            coluna = self.borda
        return {'linha':linha, 'coluna': coluna}

    def verificar_qts_bombas_redor(self, linha, coluna):
        list_linha = list(filter(lambda x: (x >= 1 and x <= self.borda), [linha - 1, linha, linha + 1]))
        list_coluna = list(filter(lambda x: (x >= 1 and x <= self.borda), [coluna - 1, coluna, coluna + 1]))
        # obtem todas as combinaçeõs possíveis
        comb_posicao = [[x, y] for x in list_linha for y in list_coluna]
        count_bombas = 0
        for posicao_linha_coluna in comb_posicao:
            posicao = self.obter_posicao_jogada(linha=posicao_linha_coluna[0], coluna=posicao_linha_coluna[1])
            if posicao in self.bombas:
                count_bombas = count_bombas + 1
        self.alterar_display_game(linha, coluna, count_bombas)
        return count_bombas

    def alterar_display_game(self, linha, coluna, count_bombas):
        self.display[linha-1][coluna-1] = str(count_bombas)


def start_game():
    tamanho = input('Insira o tamanho do seu campo minado: ')
    if int(tamanho) < 6:
        print('Tamanha mínimo aceitável é 6')
        return

    cm = CampoMinado(tamanho=int(tamanho))

    while True:
        print('\nFaça sua jogada: \n')
        linha = input('Escolha a linha:')
        coluna = input('Escolha a coluna:')
        cm.jogada(linha=int(linha),coluna=int(coluna))
        if cm.next_game:
            print(cm.message)
            print(cm.valor_qt_bomba_campo)
            continue
        else:
            print(cm.status)
            print(cm.message)

            time_sleep = 0.35
            print('-' * 39)
            time.sleep(time_sleep)
            print('-' * 39)
            time.sleep(time_sleep)
            print('-' * 39)
            time.sleep(time_sleep)
            print('-' * 39)
            time.sleep(time_sleep)
            print('-' * 39)
            break


if __name__ == '__main__':
    time_sleep = 0.35
    print('-' * 39)
    time.sleep(time_sleep)
    print('-' * 39)
    time.sleep(time_sleep)
    print('-' * 15 + 'Bem Vindo' + '-' * 15)
    time.sleep(time_sleep)
    print('-' * 39)
    time.sleep(time_sleep)
    print('-' * 39 + '\n')
    time.sleep(1)
    while True:
        print('Escolha as seguintes opções:\n')
        print('1) INICIAR JOGO\n')
        print('2) Sair')
        opcao = input('Escolha opção 1 ou 2: ')
        if opcao == '1':
            start_game()
            continue
        elif opcao == '2':
            print('Fim de Jogo')

            break
        else:
            print('opção incorreta')
            continue
