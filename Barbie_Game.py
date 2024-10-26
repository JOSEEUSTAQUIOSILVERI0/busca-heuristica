import tkinter as tk
import heapq
import time
import random

class JogoBarbie(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Barbie - Algoritmo A*")

        # Configuração do mapa com diferentes custos de terreno
        self.mapa = [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 1, 1, 1, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 1, 11, 11, 11, 11, 11, 1, 11, 11, 11, 11, 11, 11, 1, 5, 5, 5, 5, 1, 11, 11, 11, 5, 10, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5],
    [5, 5, 1, 11, 11, 11, 11, 11, 1, 11, 11, 11, 11, 11, 11, 1, 1, 1, 1, 1, 1, 11, 11, 10, 10, 10, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 11, 11, 1, 11, 11, 1, 11, 11, 11, 10, 11, 11, 1, 11, 11, 11, 11, 5, 11, 11, 10, 10, 10, 5, 5, 5, 1, 5, 5, 5, 3, 3, 3, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 11, 11, 5, 11, 11, 11, 5, 10, 5, 5, 5, 1, 5, 5, 5, 3, 3, 3, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 11, 11, 11, 5, 5, 5, 5, 5, 10, 5, 5, 5, 1, 5, 5, 5, 3, 3, 3, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 11, 11, 11, 11, 5, 11, 11, 11, 5, 10, 5, 5, 5, 1, 5, 5, 5, 3, 3, 3, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 3, 3, 3, 3, 5, 5, 5, 5, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 11, 11, 11, 5, 10, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5],
    [5, 5, 1, 3, 3, 3, 3, 5, 3, 5, 5, 3, 3, 3, 3, 1, 5, 5, 5, 5, 1, 11, 11, 10, 10, 10, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5],
    [5, 5, 1, 3, 3, 3, 3, 5, 5, 5, 5, 3, 3, 3, 3, 1, 5, 5, 5, 5, 1, 11, 11, 11, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 5, 5, 5, 5, 1, 11, 11, 11, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 5, 5, 5, 5, 1, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 10, 5, 11, 11, 11, 5, 5, 11, 11, 11, 11, 5, 5, 10, 5, 11, 11, 11, 11, 11, 11, 11, 5, 10, 5, 11, 11, 11, 11, 11, 11, 11, 5, 11, 11, 11, 11, 11, 5, 5],
    [5, 5, 10, 1, 1, 11, 11, 5, 5, 11, 11, 11, 10, 10, 10, 10, 5, 11, 11, 11, 11, 11, 11, 11, 5, 10, 5, 11, 11, 11, 11, 11, 11, 11, 5, 11, 11, 11, 11, 11, 5, 5],
    [5, 5, 10, 5, 11, 11, 11, 5, 5, 11, 11, 11, 11, 5, 5, 10, 5, 11, 10, 11, 11, 11, 10, 11, 5, 10, 5, 11, 11, 11, 11, 10, 11, 11, 5, 11, 11, 10, 11, 11, 5, 5],
    [5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 10, 5, 5, 5, 10, 5, 5, 10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5],
    [5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5],
    [5, 5, 10, 1, 1, 1, 1, 1, 1, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 10, 5, 5, 5, 5, 5, 10, 5, 5, 10, 5, 1, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 1, 11, 11, 11, 11, 1, 10, 5, 11, 11, 11, 5, 5, 11, 11, 11, 5, 10, 5, 11, 11, 10, 11, 5, 11, 11, 5, 10, 5, 11, 10, 11, 1, 11, 11, 5, 10, 5, 5],
    [5, 5, 10, 1, 11, 11, 11, 11, 1, 10, 5, 11, 11, 11, 5, 5, 11, 11, 3, 10, 10, 5, 11, 11, 11, 11, 5, 11, 11, 5, 10, 5, 11, 11, 11, 1, 11, 11, 5, 10, 5, 5],
    [5, 5, 10, 1, 11, 11, 11, 1, 1, 10, 10, 10, 11, 11, 5, 5, 11, 11, 11, 5, 10, 5, 5, 5, 5, 5, 5, 11, 10, 10, 10, 5, 5, 5, 5, 1, 11, 3, 10, 10, 5, 5],
    [5, 5, 10, 1, 11, 11, 11, 11, 1, 10, 5, 11, 11, 11, 5, 5, 11, 11, 11, 5, 10, 5, 11, 11, 11, 11, 5, 11, 11, 5, 10, 5, 11, 11, 11, 1, 11, 11, 5, 10, 5, 5],
    [5, 5, 10, 1, 11, 11, 11, 11, 1, 10, 5, 11, 11, 11, 5, 5, 11, 11, 11, 5, 10, 5, 11, 11, 10, 11, 5, 11, 11, 5, 10, 5, 11, 10, 11, 1, 11, 11, 5, 10, 5, 5],
    [5, 5, 10, 1, 1, 1, 1, 1, 1, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 10, 5, 5, 5, 5, 5, 10, 5, 5, 10, 5, 1, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5],
    [5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 1, 5, 10, 5, 1, 5, 5, 5, 1, 5, 10, 5, 5, 5, 10, 5, 5, 5, 5, 1, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 5, 11, 11, 11, 11, 11, 11, 5, 10, 5, 11, 11, 11, 1, 11, 10, 11, 1, 11, 11, 11, 1, 11, 10, 11, 5, 5, 10, 5, 11, 11, 11, 1, 11, 11, 5, 10, 5, 5],
    [5, 5, 10, 5, 11, 11, 10, 10, 11, 11, 5, 10, 5, 11, 10, 11, 1, 11, 11, 11, 1, 11, 10, 11, 1, 11, 11, 11, 5, 5, 10, 5, 11, 11, 11, 11, 11, 11, 5, 10, 5, 5],
    [5, 5, 10, 5, 5, 5, 10, 10, 5, 5, 5, 10, 5, 5, 10, 5, 1, 5, 5, 5, 1, 5, 10, 5, 1, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5],
    [5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5],
    [5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 10, 1, 1, 1, 1, 10, 5, 5],
    [5, 5, 10, 5, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 10, 1, 11, 11, 1, 10, 5, 5],
    [5, 5, 10, 5, 11, 10, 10, 10, 10, 10, 10, 10, 11, 11, 10, 10, 10, 11, 11, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 10, 1, 11, 11, 1, 10, 5, 5],
    [5, 5, 10, 5, 11, 10, 11, 11, 11, 11, 11, 10, 11, 11, 11, 11, 10, 11, 11, 5, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 1, 3, 11, 1, 10, 5, 5],
    [5, 5, 10, 5, 11, 10, 10, 10, 10, 11, 11, 10, 10, 10, 10, 10, 10, 11, 11, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 10, 1, 11, 11, 1, 10, 5, 5],
    [5, 5, 10, 5, 11, 11, 11, 11, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 10, 1, 11, 11, 1, 10, 5, 5],
    [5, 5, 10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5, 5, 10, 1, 1, 1, 1, 10, 5, 5],
    [5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],

           
        ]

               
        # Posição inicial e metas
        self.jogador = (18, 22)
        self.metas = [(12, 4), (8, 9), (34, 5), (37, 23), (14, 35), (36, 36)]
        
        # Seleciona 3 amigos aleatórios como metas
        # Verifique se existem pelo menos 3 metas
        if len(self.metas) >= 3:
            # Seleciona três metas aleatórias
            self.metas_mensagem = random.sample(self.metas, 3)
        else:
            # Tratamento de exceção caso não haja metas suficientes
            raise ValueError("A lista de metas deve conter pelo menos 3 itens.")
        
        print("Metas selecionadas:", self.metas_mensagem)
        
        # Configurações de interface e controle
        self.caminho_percorrido = []
        self.block_size = 15
        self.canvas = tk.Canvas(self, width=len(self.mapa[0]) * self.block_size, height=len(self.mapa) * self.block_size)
        self.canvas.pack()
        
        # Desenhar mapa e iniciar movimento automático
        self.desenhar_mapa()
        self.movimento_automatico()

    def desenhar_mapa(self):
        """Desenha o mapa e a posição inicial do jogador e das metas"""
        for y, linha in enumerate(self.mapa):
            for x, custo in enumerate(linha):
                cor = self.obter_cor_celula(custo)
                self.canvas.create_rectangle(x * self.block_size, y * self.block_size, (x + 1) * self.block_size, (y + 1) * self.block_size, fill=cor)

        # Desenhar jogador
        self.desenhar_jogador(self.jogador)

        # Desenhar metas
        for meta in self.metas:
            x, y = meta
            self.canvas.create_rectangle(x * self.block_size + 3, y * self.block_size + 3, (x + 1) * self.block_size - 3, (y + 1) * self.block_size - 3, fill="blue")

    def desenhar_jogador(self, posicao):
        """Desenha o jogador na posição especificada"""
        x, y = posicao
        self.canvas.create_oval(x * self.block_size + 2, y * self.block_size + 2, (x + 1) * self.block_size - 2, (y + 1) * self.block_size - 2, fill="red", tags="jogador")

    def obter_cor_celula(self, custo):
        """Retorna a cor da célula com base no custo do terreno"""
        if custo == 1:
            return "white"     # Asfalto
        elif custo == 3:
            return "#964B00"     # Terra
        elif custo == 5:
            return "green"     # Grama
        elif custo == 10:
            return "silver"    # Paralelepípedo
        elif custo == 11:
            return "#ff8c00"    # Edifício

    def movimento_automatico(self):
        """Controla o movimento do jogador até todas as metas e de volta à posição inicial"""
        inicio_tempo = time.time()
        custo_total = 0
        
        for meta in self.metas_mensagem:
            caminho = self.a_estrela(self.jogador, meta)
            if caminho:
                custo_total += self.movimento_ate_meta(meta, caminho)

        # Retorno à posição inicial
        caminho_de_volta = self.a_estrela(self.jogador, (18, 22))
        custo_total += self.movimento_ate_meta((18, 22), caminho_de_volta)
        
        # Exibir o custo total e tempo gasto
        fim_tempo = time.time()
        print(f"Custo total do caminho percorrido: {custo_total}")
        print(f"Tempo total: {fim_tempo - inicio_tempo:.2f} segundos")

    def movimento_ate_meta(self, meta, caminho):
        """Move o jogador ao longo do caminho até a meta, retornando o custo do percurso"""
        custo_caminho = sum(self.mapa[y][x] for x, y in caminho)
        
        for posicao in caminho:
            self.jogador = posicao
            self.desenhar_jogador(posicao)
            self.canvas.update()
            time.sleep(0.05)
        
        if meta in self.metas_mensagem:
            self.exibir_mensagem("Convite aceito para o concurso!", meta)
        
        return custo_caminho

    def a_estrela(self, inicio, fim):
        """Implementação do algoritmo A* para encontrar o menor caminho até a meta"""
        fronteira = [(0, inicio)]
        heapq.heapify(fronteira)
        custo_so_far = {inicio: 0}
        came_from = {inicio: None}

        while fronteira:
            _, atual = heapq.heappop(fronteira)
            if atual == fim:
                caminho = []
                while atual:
                    caminho.append(atual)
                    atual = came_from[atual]
                return caminho[::-1]

            for vizinho in self.vizinhos_validos(atual):
                novo_custo = custo_so_far[atual] + self.mapa[vizinho[1]][vizinho[0]]
                if vizinho not in custo_so_far or novo_custo < custo_so_far[vizinho]:
                    custo_so_far[vizinho] = novo_custo
                    prioridade = novo_custo + self.distancia(vizinho, fim)
                    heapq.heappush(fronteira, (prioridade, vizinho))
                    came_from[vizinho] = atual

    def vizinhos_validos(self, posicao):
        """Retorna os vizinhos válidos para o movimento"""
        x, y = posicao
        vizinhos = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [vizinho for vizinho in vizinhos if self.validar_posicao(vizinho)]

    def validar_posicao(self, posicao):
        """Verifica se uma posição é válida (dentro dos limites e não é edifício)"""
        x, y = posicao
        return 0 <= x < len(self.mapa[0]) and 0 <= y < len(self.mapa) and self.mapa[y][x] < 11

    def distancia(self, a, b):
        """Calcula a distância de Manhattan entre duas posições"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def exibir_mensagem(self, mensagem, meta):
        """Exibe uma mensagem no centro da tela quando uma meta é alcançada"""
        self.canvas.delete("mensagem")
        pos_x = (len(self.mapa[0]) * self.block_size) // 2
        pos_y = (len(self.mapa) * self.block_size) // 2
        self.canvas.create_text(pos_x, pos_y, text=mensagem, fill="black", font=("Helvetica", 12), tags="mensagem")
        self.canvas.update()
        self.after(3000, lambda: self.canvas.delete("mensagem"))

if __name__ == "__main__":
    app = JogoBarbie()
    app.mainloop()
