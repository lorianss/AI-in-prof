import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# Шаг 1: Создание списка населённых пунктов и расстояний между ними
places = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Омск", "Самара", "Ростов-на-Дону",
    "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград", "Краснодар",
    "Саратов", "Тюмень", "Тольятти", "Ижевск", "Барнаул"
]

# Матрица расстояний (добавляем недостающие рёбра)
distances = {
    ("Москва", "Санкт-Петербург"): 650,
    ("Москва", "Казань"): 800,
    ("Москва", "Нижний Новгород"): 450,
    ("Санкт-Петербург", "Новосибирск"): 3200,
    ("Санкт-Петербург", "Казань"): 1000,
    ("Новосибирск", "Екатеринбург"): 1700,
    ("Екатеринбург", "Казань"): 1200,
    ("Екатеринбург", "Челябинск"): 300,
    ("Екатеринбург", "Омск"): 900,
    ("Казань", "Нижний Новгород"): 200,
    ("Казань", "Самара"): 600,
    ("Нижний Новгород", "Челябинск"): 1500,
    ("Челябинск", "Омск"): 800,
    ("Омск", "Красноярск"): 1200,
    ("Самара", "Ростов-на-Дону"): 1100,
    ("Самара", "Уфа"): 400,
    ("Ростов-на-Дону", "Краснодар"): 400,
    ("Уфа", "Красноярск"): 2000,
    ("Уфа", "Пермь"): 500,
    ("Уфа", "Екатеринбург"): 500,  # Добавлено новое ребро
    ("Казань", "Екатеринбург"): 1200,  # Добавлено новое ребро
    ("Красноярск", "Воронеж"): 3000,
    ("Пермь", "Волгоград"): 1000,
    ("Волгоград", "Краснодар"): 500,
    ("Краснодар", "Саратов"): 700,
    ("Саратов", "Тюмень"): 1200,
    ("Тюмень", "Тольятти"): 1300,
    ("Тольятти", "Ижевск"): 400,
    ("Ижевск", "Барнаул"): 2000,
}

# Шаг 2: Создание графа
G = nx.Graph()

# Добавление узлов (населённых пунктов)
G.add_nodes_from(places)

# Добавление рёбер с весами (расстояниями)
for (place1, place2), distance in distances.items():
    G.add_edge(place1, place2, weight=distance)

# Шаг 3: Определение начального и конечного пунктов
start_place = "Москва"
end_place = "Красноярск"

# Промежуточные пункты
intermediate_places = ["Казань", "Екатеринбург", "Уфа"]

# Шаг 4: Поиск минимального маршрута через промежуточные пункты
def find_min_path_with_intermediates(graph, start, intermediates, end):
    from itertools import permutations
    min_distance = float('inf')
    best_path = None

    for perm in permutations(intermediates):
        current_path = [start] + list(perm) + [end]
        try:
            total_distance = sum(
                graph[current_path[i]][current_path[i + 1]]['weight']
                for i in range(len(current_path) - 1)
            )
            if total_distance < min_distance:
                min_distance = total_distance
                best_path = current_path
        except KeyError:
            continue  # Пропускаем, если путь не существует

    return best_path, min_distance

# Вызов функции
path, distance = find_min_path_with_intermediates(G, start_place, intermediate_places, end_place)

# Проверка, найден ли путь
if path is None:
    print("Маршрут не найден. Проверьте соединения между городами.")
else:
    print(f"Минимальный маршрут: {path}")
    print(f"Общая длина маршрута: {distance} км")

    # Визуализация графа и маршрута
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=6, font_weight="bold")

    # Выделение маршрута
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title("Граф дорог между населёнными пунктами")
    plt.show()