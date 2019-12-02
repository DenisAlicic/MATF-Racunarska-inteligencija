# Primer resavanja problema pakovanja ranca maksimalne vrednosti, ogranicenog kapaciteta
# Koriscenjem algoritma branch and bound
# Ideja ja resenja predstaviti u obliku stabla
# Cvor stabla predstavlja svaki predmet koji se potencijalno stavlja u ranac
# Zatim leva grana predstavlja ubacivanje predmeta, desna da predmet ne ulazi u resenje
# Do resenja se dolazi bektrekingom uz dodatnu informaciju koje je najbolje resenje podstabla 
# trenutnog cvora. Leva i desna podstabla su identicna za svaki cvor u smislu predmeta i izgleda.
#                1
#       2                2
#    3     3          3     3
#  4   4  4  4      4   4  4  4

import queue

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

class Node:
    def __init__(self, level, weight, value):
        self.level = level
        self.weight = weight
        self.value = value
        self.bound = 0.0

def bound(u, knapsackWeight, items):
    if (u.weight > knapsackWeight):
        return 0
    totalValue = u.value
    totalWeight = u.weight
    l = u.level + 1
    while l < len(items) and totalWeight + items[l].weight <= knapsackWeight:
        totalWeight += items[l].weight
        totalValue += items[l].value
        l += 1
    return totalValue


def knapsack(W, arr):
    Q = queue.Queue()
    u = Node(-1, 0, 0)
    Q.put(u)
    maxValue = 0.0
    while(not Q.empty()):
        u = Q.get()
        if u.level == len(items)-1:
            continue
        v = Node(u.level+1, u.weight + items[u.level + 1].weight, u.value + items[u.level+1].value)
        if v.weight <= W and v.value > maxValue:
            maxValue = v.value
        v.bound = bound(v, W, items)
        if v.bound > maxValue:
            Q.put(v)
        v = Node(u.level + 1, u.weight, u.value)
        v.bound = bound(v, W, items)
        if v.bound > maxValue:
            Q.put(v)
    return maxValue


knapsackWeight = 10.0
items = [Item(2, 10), Item(3.14, 50), Item(1.98, 100), Item(5, 95), Item(3,30)]
print(knapsack(knapsackWeight, items))
