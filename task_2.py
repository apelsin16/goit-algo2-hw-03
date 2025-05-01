import csv
import timeit
from BTrees.OOBTree import OOBTree

# Читання CSV
def load_data(file_path):
    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        items = []
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"])
            }
            items.append(item)
        return items

# Структури
tree_by_price = OOBTree()  # ключ — ціна, значення — список товарів
items_dict = {}

# Додавання у дерево: ключ — ціна
def add_item_to_tree(tree, item):
    price = item["Price"]
    if price not in tree:
        tree[price] = []
    tree[price].append(item)

# Додавання у dict: ключ — ID
def add_item_to_dict(d, item):
    d[item["ID"]] = item

# Діапазонний запит для дерева (ефективно!)
def range_query_tree(tree, min_price, max_price):
    result = []
    for _, items in tree.items(min_price, max_price):
        result.extend(items)
    return result

# Діапазонний запит для словника (лінійний пошук)
def range_query_dict(d, min_price, max_price):
    return [item for item in d.values() if min_price <= item["Price"] <= max_price]

# Завантаження
items = load_data("generated_items_data.csv")
for item in items:
    add_item_to_tree(tree_by_price, item)
    add_item_to_dict(items_dict, item)

# Параметри для запиту
MIN_PRICE = 10.0
MAX_PRICE = 100.0

# Функції-обгортки для timeit
def time_tree():
    range_query_tree(tree_by_price, MIN_PRICE, MAX_PRICE)

def time_dict():
    range_query_dict(items_dict, MIN_PRICE, MAX_PRICE)

# Вимірювання часу
tree_time = timeit.timeit(time_tree, number=100)
dict_time = timeit.timeit(time_dict, number=100)

# Вивід
print(f"Час виконання 100 запитів для OOBTree: {tree_time:.4f} секунд")
print(f"Час виконання 100 запитів для dict:    {dict_time:.4f} секунд")
