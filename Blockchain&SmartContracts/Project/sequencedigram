import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

fig, ax = plt.subplots(figsize=(14, 7))
G = nx.DiGraph()

# Aktörler ve use case'ler
actors = {
    "Developer": (1, 1),
    "Project Manager": (5, 1),
    "Auditor": (9, 1)
}

use_cases = {
    "Submit Contributions": (2, 2),
    "Receive Tokens": (4, 2),
    "Access Training": (6, 2),
    "Participate in Decision Making": (8, 2),
    "Trade Tokens": (10, 2)
}

# Aktörleri diagrama ekle
for actor, pos in actors.items():
    G.add_node(actor, pos=pos)

# Use case'leri diagrama ekle
for use_case, pos in use_cases.items():
    G.add_node(use_case, pos=pos)

# Bağlantıları ekle
edges = [
    ("Developer", "Submit Contributions"),
    ("Submit Contributions", "Receive Tokens"),
    ("Receive Tokens", "Developer"),
    ("Developer", "Access Training"),
    ("Developer", "Participate in Decision Making"),
    ("Developer", "Trade Tokens"),
    ("Project Manager", "Receive Tokens"),
    ("Auditor", "Trade Tokens")
]

G.add_edges_from(edges)

# Düğümlerin pozisyonlarını çiz
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=9, font_weight='bold', node_shape="s")

# Bağlantı okları
nx.draw_networkx_edges(G, pos, edgelist=edges, arrowstyle='-|>', arrowsize=15, edge_color='blue')

plt.title('Tokenomics Use Case Diagram')
plt.grid('on')
plt.show()
