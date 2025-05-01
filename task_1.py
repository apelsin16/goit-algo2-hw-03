import networkx as nx
# import matplotlib.pyplot as plt
from collections import deque
import pandas as pd

# Створюємо граф
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),

    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),

    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),

    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),

    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Додаємо ребра до графа з атрибутом "capacity"
for u, v, capacity in edges:
    G.add_edge(u, v, capacity=capacity)

# pos = {
#     # Термінали (верхній рівень)
#     "Термінал 1": (0, 3),
#     "Термінал 2": (4, 3),
#
#     # Склади (середній рівень)
#     "Склад 1": (0, 2),
#     "Склад 2": (2, 2),
#     "Склад 3": (1, 2),
#     "Склад 4": (4, 2),
#
#     # Магазини (нижній рівень)
#     "Магазин 1": (-1, 1),
#     "Магазин 2": (0, 1),
#     "Магазин 3": (1, 1),
#     "Магазин 4": (1.5, 1),
#     "Магазин 5": (2, 1),
#     "Магазин 6": (2.5, 1),
#     "Магазин 7": (0.5, 1),
#     "Магазин 8": (1, 0.8),
#     "Магазин 9": (1.5, 0.8),
#     "Магазин 10": (3.5, 1),
#     "Магазин 11": (4, 1),
#     "Магазин 12": (4.5, 1),
#     "Магазин 13": (5, 1),
#     "Магазин 14": (5.5, 1),
# }
#
# nx.draw(
#     G, pos, with_labels=True, node_size=2000, node_color='lightblue',
#     font_size=9, font_weight='bold', arrows=True
# )
# labels = nx.get_edge_attributes(G, 'capacity')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
# plt.title("Схема логістики: Термінали → Склади → Магазини")
# plt.tight_layout()
# plt.savefig("graph.png")

# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][
                neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow,
                            capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node

        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow


# Створюємо матрицю пропускних здатностей
nodes = list(G.nodes)
node_index = {node: idx for idx, node in enumerate(nodes)}
capacity_matrix = [[0] * len(nodes) for _ in range(len(nodes))]

# Заповнюємо матрицю пропускних здатностей
for u, v, data in G.edges(data=True):
    capacity_matrix[node_index[u]][node_index[v]] = data['capacity']

# Викликаємо алгоритм Едмондса-Карпа для кожного термінала (source) та магазину (sink)
results = []
for terminal in ["Термінал 1", "Термінал 2"]:
    for i in range(1, 15):
        store = f"Магазин {i}"
        source = node_index[terminal]
        sink = node_index[store]

        max_flow = edmonds_karp(capacity_matrix, source, sink)
        results.append([terminal, store, max_flow])

# Створюємо таблицю

df = pd.DataFrame(results, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"])
print(df)

# max_capacity_edge = max(edges, key=lambda x: x[2])
# print(f"Маршрут з найбільшою пропускною здатністю: {max_capacity_edge}")
#
# min_capacity_edge = min(edges, key=lambda x: x[2])
# print(f"Маршрут з найменшою пропускною здатністю: {min_capacity_edge}")


