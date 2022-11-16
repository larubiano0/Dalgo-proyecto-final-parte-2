import sys


class Grafo:

    def __init__(self):
        self.V = set()
        # Diccionario de adyacencia nodo_de_origen:[nodos_destino]
        self.A = dict()
        self.marcados_temporal = set()
        self.marcados_permantente = set()
        self.contiene_ciclo = False

    def anadir_vertice(self, v):
        self.V.add(v)
        if v not in self.A:
            self.A[v] = []

    def anadir_eje(self, v1, v2):
        if v2 not in self.A[v1]:
            self.A[v1].append(v2)

    def __str__(self):
        return f"V: {self.V}, A: {self.A}"

    def __repr__(self):
        return f"V: {self.V}, A: {self.A}"

    def dfs_topological_sort_util(self, i, stack):
        if i in self.marcados_permantente:
            return
        if i in self.marcados_temporal:
            self.contiene_ciclo = True
            return

        self.marcados_temporal.add(i)

        for j in self.A[i]:
            self.dfs_topological_sort_util(j, stack)

        self.marcados_temporal.remove(i)
        self.marcados_permantente.add(i)
        stack.insert(0, i)

    def dfs_topological_sort(self):
        stack = []
        for i in self.V:
            if self.contiene_ciclo:
                return stack
            elif i not in self.marcados_permantente:
                self.dfs_topological_sort_util(i, stack)

        return stack


def encontrar_orden(diccionario):
    # Grafo de implicación entre letras, el vertice (a,b) implica que a < b
    grafo_de_implicacion = Grafo()
    palabra_anterior = diccionario[0]
    i = 1
    while i < len(diccionario):
        palabra_actual = diccionario[i]

        for x, y in zip(palabra_anterior, palabra_actual):
            if x != y:
                grafo_de_implicacion.anadir_vertice(x)
                grafo_de_implicacion.anadir_vertice(y)
                grafo_de_implicacion.anadir_eje(x, y)
                break

        palabra_anterior = palabra_actual
        i += 1

    orden = grafo_de_implicacion.dfs_topological_sort()

    if grafo_de_implicacion.contiene_ciclo:
        return "ERROR"
    else:
        return "".join(orden)


def main():
    casos = int(sys.stdin.readline())  # Lee el número de casos
    for _ in range(casos):
        n, m = tuple(sys.stdin.readline().split())
        n, m = int(n), int(m)
        # Guarda en cada pagina las palabras que se encuentran en ella
        paginas = [[] for _ in range(m)]
        for _ in range(n):
            pagina = list(sys.stdin.readline().split())
            n_pagina = int(pagina[0])
            palabras_pagina = pagina[1:]
            paginas[n_pagina] = palabras_pagina

        # Lista ordenada con todas las palabras en el "diccionario" (flatten)
        palabras = [j for sub in paginas for j in sub]

        orden = encontrar_orden(palabras)  # Encuentra el orden como un string
        sys.stdout.write(orden + "\n")


if __name__ == '__main__':
    main()

# python3 solucion.py < P0.in > archivo2.out
