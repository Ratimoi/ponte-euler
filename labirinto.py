import heapq
from collections import deque

DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]

labirinto = [
    "I....#.........",
    "##.#.#####.#.##",
    ".#...#.........",
    ".#.###.#.###.#.",
    ".#.....#...#.#.",
    ".#.###.###.###.",
    ".......#.#.....",
    ".###.###.#####.",
    ".#...#.#.....#.",
    ".###.#.#.#.###.",
    ".....#.#.#.....",
    "##.#.#.#.#.####",
    ".........#.....",
    ".###########.#.",
    "..............F",
]

def achar(lab, simbolo):
    for i, linha in enumerate(lab):
        if simbolo in linha:
            return (i, linha.index(simbolo))


def livre(lab, i, j):
    dentro = 0 <= i < len(lab) and 0 <= j < len(lab[0])
    return dentro and lab[i][j] != '#'


def montar_grafo(lab):
    grafo = {}
    for i in range(len(lab)):
        for j in range(len(lab[0])):
            if not livre(lab, i, j):
                continue
            grafo[(i, j)] = []
            for di, dj in DIRECOES:
                if livre(lab, i + di, j + dj):
                    grafo[(i, j)].append((i + di, j + dj))
    return grafo


def desenhar(lab, caminho):
    grade = [list(linha) for linha in lab]
    for i, j in caminho:
        if grade[i][j] == '.':
            grade[i][j] = '*'
    for linha in grade:
        print(''.join(linha))


def reconstruir(pai, saida):
    if saida not in pai:
        return []
    caminho = []
    v = saida
    while v is not None:
        caminho.append(v)
        v = pai[v]
    return caminho[::-1]


def dfs(grafo, inicio, saida):
    pai = {inicio: None}
    visitadas = 0

    def visitar(v):
        nonlocal visitadas
        visitadas += 1
        if v == saida:
            return True
        for w in grafo[v]:
            if w not in pai:
                pai[w] = v
                if visitar(w):
                    return True
        return False

    visitar(inicio)
    return reconstruir(pai, saida), visitadas


def bfs(grafo, inicio, saida):
    pai = {inicio: None}  
    fila = deque([inicio])
    visitadas = 0
    while fila:
        v = fila.popleft()
        visitadas += 1
        if v == saida:
            break
        for w in grafo[v]:
            if w not in pai:
                pai[w] = v
                fila.append(w)
    return reconstruir(pai, saida), visitadas


def h(v, saida): 
    return abs(v[0] - saida[0]) + abs(v[1] - saida[1])


def gulosa(grafo, inicio, saida):
    pai = {inicio: None}
    fronteira = [(h(inicio, saida), inicio)]
    visitadas = 0
    while fronteira:
        _, v = heapq.heappop(fronteira)  # menor h
        visitadas += 1
        if v == saida:
            break
        for w in grafo[v]:
            if w not in pai:
                pai[w] = v
                heapq.heappush(fronteira, (h(w, saida), w))
    return reconstruir(pai, saida), visitadas


if __name__ == "__main__":
    grafo = montar_grafo(labirinto)
    inicio = achar(labirinto, 'I')
    saida = achar(labirinto, 'F')

    resultados = []
    for nome, busca in [("DFS", dfs), ("BFS", bfs), ("Gulosa", gulosa)]:
        caminho, visitadas = busca(grafo, inicio, saida)
        passos = len(caminho) - 1
        resultados.append((nome, passos, visitadas))
        print(f"== {nome} ==")
        desenhar(labirinto, caminho)
        print()

    print(f"casas livres no labirinto: {len(grafo)}\n")
    print(f"{'algoritmo':<10}{'caminho (passos)':>18}{'casas visitadas':>18}")
    for nome, passos, visitadas in resultados:
        print(f"{nome:<10}{passos:>18}{visitadas:>18}")
