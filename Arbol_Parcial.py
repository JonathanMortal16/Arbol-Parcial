# prim_simulador.py
# Simulador del Árbol Parcial Mínimo de Prim
# - Muestra paso a paso por consola
# - Tiene opción de mostrar el grafo y el APM gráficamente (si tienes networkx y matplotlib)

import math

# ===========================
# Algoritmo de Prim (con pasos)
# ===========================
def prim_mst(num_vertices, edges, start=0):
    """
    num_vertices: número de vértices (0..n-1)
    edges: lista de aristas (u, v, w) con u,v vértices y w el peso
    start: vértice inicial
    """
    INF = math.inf

    # Matriz de adyacencia
    adj = [[INF] * num_vertices for _ in range(num_vertices)]
    for u, v, w in edges:
        # Por si se repite arista, nos quedamos con el menor peso
        if w < adj[u][v]:
            adj[u][v] = w
            adj[v][u] = w

    selected = [False] * num_vertices  # Conjunto de vértices ya incluidos en el APM
    key = [INF] * num_vertices         # Coste mínimo para conectar cada vértice
    parent = [-1] * num_vertices       # Padre de cada vértice en el APM

    key[start] = 0  # Empezamos desde "start"

    print("=== Simulador del Árbol Parcial Mínimo de Prim ===")
    print(f"Número de vértices: {num_vertices}")
    print("Vértices numerados de 0 a", num_vertices - 1)
    print(f"Comenzando desde el vértice {start}\n")

    for step in range(num_vertices):
        # 1) Elegir el vértice no seleccionado con menor 'key'
        u = -1
        min_key = INF
        for v in range(num_vertices):
            if not selected[v] and key[v] < min_key:
                min_key = key[v]
                u = v

        if u == -1:
            print("El grafo NO es conexo, el algoritmo se detiene.")
            break

        selected[u] = True

        print(f"Paso {step + 1}:")
        print(f"  -> Se agrega el vértice {u} al árbol (costo incremental = {min_key})")

        # 2) Mostrar aristas candidatas desde el conjunto visitado al no visitado
        print("  Candidatos (aristas desde vértices ya en el árbol hacia los que faltan):")
        for v in range(num_vertices):
            if selected[v]:
                for w in range(num_vertices):
                    if not selected[w] and adj[v][w] != INF:
                        print(f"    ({v} --{adj[v][w]}--> {w})")

        # 3) Actualizar keys y padres usando el nuevo vértice u
        for v in range(num_vertices):
            if not selected[v] and adj[u][v] < key[v]:
                key[v] = adj[u][v]
                parent[v] = u

        # 4) Mostrar el árbol parcial mínimo acumulado hasta ahora
        total = 0
        print("  Aristas actuales del Árbol Parcial Mínimo:")
        for v in range(num_vertices):
            if parent[v] != -1:
                print(f"    {parent[v]} --{adj[parent[v]][v]}--> {v}")
                total += adj[parent[v]][v]
        print(f"  Costo total acumulado: {total}\n")

    # Resultado final
    print("=== Resultado final ===")
    total = 0
    print("Aristas del Árbol Parcial Mínimo:")
    for v in range(num_vertices):
        if parent[v] != -1:
            print(f"  {parent[v]} --{adj[parent[v]][v]}--> {v}")
            total += adj[parent[v]][v]
    print("Costo total del árbol:", total)

    return parent  # Lo usamos para la parte gráfica


# ===========================
# Lectura del grafo por consola
# ===========================
def leer_grafo_desde_consola():
    print("Introduce los datos del grafo NO dirigido y conexo.\n")
    n = int(input("Número de vértices: "))
    m = int(input("Número de aristas: "))

    edges = []
    print("\nIntroduce cada arista en el formato:  u v peso")
    print("Ejemplo:  0 1 4   significa una arista entre 0 y 1 de peso 4\n")
    for i in range(m):
        while True:
            try:
                linea = input(f"Arista {i+1}: ")
                u_str, v_str, w_str = linea.split()
                u, v, w = int(u_str), int(v_str), float(w_str)
                if not (0 <= u < n and 0 <= v < n):
                    print("  Error: los vértices deben estar entre 0 y", n-1)
                    continue
                edges.append((u, v, w))
                break
            except ValueError:
                print("  Formato inválido, inténtalo de nuevo (ejemplo: 0 1 4)")
    return n, edges


# ===========================
# Parte gráfica (opcional)
# ===========================
def dibujar_grafo_y_mst(num_vertices, edges, parent):
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n[AVISO] No se pudo importar 'networkx' o 'matplotlib'.")
        print("       Para ver la parte gráfica, instala las librerías con:")
        print("       pip install networkx matplotlib")
        return

    G = nx.Graph()
    for i in range(num_vertices):
        G.add_node(i)

    # Aristas del grafo original
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    # Aristas del APM según 'parent'
    mst_edges = []
    for v in range(num_vertices):
        if parent[v] != -1:
            mst_edges.append((parent[v], v))

    pos = nx.spring_layout(G, seed=42)  # distribución de los nodos

    # Grafo original
    plt.figure()
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Grafo original")

    # Árbol Parcial Mínimo
    plt.figure()
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Árbol Parcial Mínimo (Prim)")

    plt.show()


# ===========================
# Programa principal
# ===========================
if __name__ == "__main__":
    # 1) Leer grafo
    n, edges = leer_grafo_desde_consola()

    # 2) Elegir vértice inicial (opcional)
    try:
        s = input("Vértice inicial para Prim (default 0): ")
        start = int(s) if s.strip() != "" else 0
    except ValueError:
        start = 0

    # 3) Ejecutar Prim (con pasos)
    parent = prim_mst(n, edges, start=start)

    # 4) Preguntar si se quiere parte gráfica
    ver_grafica = input("\n¿Deseas ver el grafo y el APM gráficamente? (s/n): ").strip().lower()
    if ver_grafica == "s":
        dibujar_grafo_y_mst(n, edges, parent)
