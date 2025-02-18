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
    ("Уфа", "Екатеринбург"): 500,
    ("Казань", "Екатеринбург"): 1200,
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

# Шаг 3: Ограничение количества городов
limited_places = places[:10]  # Берём первые 10 городов
G_limited = G.subgraph(limited_places).copy()  # Создаём изменяемую копию подграфа

# Автоматическое добавление недостающих рёбер
for u in limited_places:
    for v in limited_places:
        if u != v and not G_limited.has_edge(u, v):
            # Добавляем ребро с большим весом (например, 10000)
            G_limited.add_edge(u, v, weight=10000)

# Проверка связности графа
if not nx.is_connected(G_limited):
    print("Граф несвязный. Добавьте недостающие рёбра.")
    exit()

# Шаг 4: Решение задачи коммивояжёра методом полного перебора
def tsp_brute_force(graph, start):
    # Список всех городов, кроме начального
    cities = list(graph.nodes)
    cities.remove(start)

    # Инициализация минимального расстояния и маршрута
    min_distance = float('inf')
    best_path = None

    # Перебор всех перестановок городов
    for perm in permutations(cities):
        current_path = [start] + list(perm) + [start]  # Замыкаем путь обратно в стартовый город
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
start_city = "Москва"
best_route, min_total_distance = tsp_brute_force(G_limited, start_city)

# Проверка, найден ли маршрут
if best_route is None:
    print("Маршрут не найден. Проверьте соединения между городами.")
else:
    print(f"Оптимальный маршрут: {best_route}")
    print(f"Общая длина маршрута: {min_total_distance} км")

    # Визуализация графа и маршрута
    pos = nx.spring_layout(G_limited, seed=42)
    nx.draw(G_limited, pos, with_labels=True, node_size=200, node_color="lightblue", font_size=5, font_weight="bold")

    # Выделение маршрута
    route_edges = [(best_route[i], best_route[i + 1]) for i in range(len(best_route) - 1)]
    nx.draw_networkx_edges(G_limited, pos, edgelist=route_edges, edge_color='red', width=2)

    plt.title("Граф дорог между населёнными пунктами")
    plt.show()