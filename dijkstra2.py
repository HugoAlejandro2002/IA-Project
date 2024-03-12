import os
import osmnx as ox
import networkx as nx
import random
import heapq
import imageio.v3 as imageio
import matplotlib.pyplot as plt

place_name = "La Paz, Bolivia"
G = ox.graph_from_place(place_name, network_type="drive")

for edge in G.edges:
    maxspeed = 40
    if "maxspeed" in G.edges[edge]:
        maxspeed = G.edges[edge]["maxspeed"]
        if isinstance(maxspeed, list):
            maxspeed = min(int(speed) for speed in maxspeed)
        elif isinstance(maxspeed, str):
            maxspeed = int(maxspeed.split()[0])
    G.edges[edge]["maxspeed"] = maxspeed
    G.edges[edge]["weight"] = G.edges[edge]["length"] / maxspeed

style_changes = []


def add_edge_style_change(edge, status):
    if status == "unvisited":
        style_changes.append(
            ("edge", edge, {"color": "#d36206", "alpha": 0.2, "linewidth": 0.5})
        )
    elif status == "visited":
        style_changes.append(
            ("edge", edge, {"color": "#d36206", "alpha": 1, "linewidth": 1})
        )
    elif status == "active":
        style_changes.append(
            ("edge", edge, {"color": "#e8a900", "alpha": 1, "linewidth": 1})
        )
    elif status == "path":
        style_changes.append(
            ("edge", edge, {"color": "white", "alpha": 1, "linewidth": 1})
        )


def add_node_style_change(node, size, color="white"):
    style_changes.append(("node", node, {"size": size, "color": color}))


def apply_changes_and_plot(step):
    for change_type, id, attributes in style_changes:
        if change_type == "edge":
            for attr, value in attributes.items():
                G.edges[id][attr] = value
        elif change_type == "node":
            for attr, value in attributes.items():
                G.nodes[id][attr] = value
    fig, ax = ox.plot_graph(
        G,
        node_size=[G.nodes[node]["size"] for node in G.nodes],
        edge_color=[G.edges[edge]["color"] for edge in G.edges],
        edge_alpha=[G.edges[edge]["alpha"] for edge in G.edges],
        edge_linewidth=[G.edges[edge]["linewidth"] for edge in G.edges],
        node_color="white",
        bgcolor="#18080e",
        figsize=(20, 20),
        show=False,
        close=True,
    )
    filepath = f"frame_{step}.png"
    fig.savefig(filepath)
    plt.close(fig)
    return filepath


def generate_animation(start, end):
    frames = []
    dijkstra(start, end)
    for step in range(len(style_changes)):
        filepath = apply_changes_and_plot(step)
        frames.append(imageio.imread(filepath))
        #os.remove(filepath)
    imageio.mimsave("animation.gif", frames, fps=10)


def dijkstra(orig, dest):
    for node in G.nodes:
        G.nodes[node]["visited"] = False
        G.nodes[node]["distance"] = float("inf")
        G.nodes[node]["previous"] = None
        G.nodes[node]["size"] = 0
    for edge in G.edges:
        add_edge_style_change(edge, "unvisited")
    G.nodes[orig]["distance"] = 0
    G.nodes[orig]["size"] = 50
    G.nodes[dest]["size"] = 50
    pq = [(0, orig)]
    step = 0
    pq = [(0, orig, None)]
    while pq:
        current_distance, node, prev_node = heapq.heappop(pq)
        if "visited" in G.nodes[node]:
            continue
        G.nodes[node]["visited"] = True
        if prev_node is not None:
            add_edge_style_change((prev_node, node, 0), "visited")
        if node == dest:
            break
        for neighbor in G.neighbors(node):
            if "visited" not in G.nodes[neighbor]:
                distance = G.edges[node, neighbor, 0]["weight"]
                heapq.heappush(pq, (current_distance + distance, neighbor, node))


start = random.choice(list(G.nodes))
end = random.choice(list(G.nodes))

generate_animation(start, end)
