import osmnx as ox
import networkx as nx
import random
import heapq
import imageio
import os

## Libraries to animate the analysis
import matplotlib.pyplot as plt

place_name = "La Paz, Bolivia"
G = ox.graph_from_place(place_name, network_type="drive")

states = []

for edge in G.edges:
    # Cleaning the "maxspeed" attribute, some values are lists, some are strings, some are None
    maxspeed = 40
    if "maxspeed" in G.edges[edge]:
        maxspeed = G.edges[edge]["maxspeed"]
        if type(maxspeed) == list:
            speeds = [int(speed) for speed in maxspeed]
            maxspeed = min(speeds)
        elif type(maxspeed) == str:
            maxspeed = maxspeed.split(" ")
            maxspeed = int(maxspeed[0])
    G.edges[edge]["maxspeed"] = maxspeed
    # Adding the "weight" attribute (time = distance / speed)
    G.edges[edge]["weight"] = G.edges[edge]["length"] / maxspeed


def style_unvisited_edge(edge):
    G.edges[edge]["color"] = "#d36206"
    G.edges[edge]["alpha"] = 0.2
    G.edges[edge]["linewidth"] = 0.5


def style_visited_edge(edge):
    G.edges[edge]["color"] = "#d36206"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1


def style_active_edge(edge):
    G.edges[edge]["color"] = "#e8a900"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1


def style_path_edge(edge):
    G.edges[edge]["color"] = "white"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1


def plot_graph():
    ox.plot_graph(
        G,
        node_size=[G.nodes[node]["size"] for node in G.nodes],
        edge_color=[G.edges[edge]["color"] for edge in G.edges],
        edge_alpha=[G.edges[edge]["alpha"] for edge in G.edges],
        edge_linewidth=[G.edges[edge]["linewidth"] for edge in G.edges],
        node_color="white",
        bgcolor="#18080e",
        figsize=(20, 20),
    )


def plot_state(step, state):
    filename = f"frame_{step:05d}.png"
    fig, ax = ox.plot_graph(
        state,
        node_size=[state.nodes[node]["size"] for node in state.nodes],
        edge_color=[state.edges[edge]["color"] for edge in state.edges],
        edge_alpha=[state.edges[edge]["alpha"] for edge in state.edges],
        edge_linewidth=[state.edges[edge]["linewidth"] for edge in state.edges],
        node_color="white",
        bgcolor="#18080e",
        figsize=(20, 20),
        show=False,
        save=True,
        filepath=f"frames/{filename}",
    )
    states.append(f"frames/{filename}")
    return f"frames/{filename}"


def plot_heatmap(algorithm):
    edge_colors = ox.plot.get_edge_colors_by_attr(G, f"{algorithm}_uses", cmap="hot")
    fig, _ = ox.plot_graph(
        G,
        node_size=0,
        edge_color=edge_colors,
        # bgcolor="#9a9745"
        bgcolor="#18080e",
    )


def dijkstra(orig, dest, plot=False):
    for node in G.nodes:
        G.nodes[node]["visited"] = False
        G.nodes[node]["distance"] = float("inf")
        G.nodes[node]["previous"] = None
        G.nodes[node]["size"] = 0
    for edge in G.edges:
        style_unvisited_edge(edge)
    G.nodes[orig]["distance"] = 0
    G.nodes[orig]["size"] = 50
    G.nodes[dest]["size"] = 50
    pq = [(0, orig)]
    step = 0
    while pq:
        _, node = heapq.heappop(pq)
        if node == dest:
            if plot:
                print("Iteraciones:", step)
                plot_graph()
        if G.nodes[node]["visited"]:
            continue
        G.nodes[node]["visited"] = True
        for edge in G.out_edges(node):
            style_visited_edge((edge[0], edge[1], 0))
            neighbor = edge[1]
            weight = G.edges[(edge[0], edge[1], 0)]["weight"]
            if G.nodes[neighbor]["distance"] > G.nodes[node]["distance"] + weight:
                G.nodes[neighbor]["distance"] = G.nodes[node]["distance"] + weight
                G.nodes[neighbor]["previous"] = node
                heapq.heappush(pq, (G.nodes[neighbor]["distance"], neighbor))
                for edge2 in G.out_edges(neighbor):
                    style_active_edge((edge2[0], edge2[1], 0))
        if step % 500 == 0:
            plot_state(step, G)
        step += 1


def reconstruct_path(orig, dest, plot=False, algorithm=None):
    for edge in G.edges:
        style_unvisited_edge(edge)
    dist = 0
    speeds = []
    curr = dest
    while curr != orig:
        prev = G.nodes[curr]["previous"]
        dist += G.edges[(prev, curr, 0)]["length"]
        speeds.append(G.edges[(prev, curr, 0)]["maxspeed"])
        style_path_edge((prev, curr, 0))
        if algorithm:
            G.edges[(prev, curr, 0)][f"{algorithm}_uses"] = (
                G.edges[(prev, curr, 0)].get(f"{algorithm}_uses", 0) + 1
            )
        curr = prev
    dist /= 1000
    if plot:
        print(f"Distance: {dist}")
        print(f"Avg. speed: {sum(speeds)/len(speeds)}")
        print(f"Total time: {dist/(sum(speeds)/len(speeds)) * 60}")
        plot_graph()


start = random.choice(list(G.nodes))
end = random.choice(list(G.nodes))

dijkstra(start, end, plot=True)
with imageio.get_writer("path_animation.gif", mode="I") as writer:
    for i, state in enumerate(states):
        filename = plot_state(i, state)
        image = imageio.imread(filename)
        writer.append_data(image)
        # os.remove(filename)  # Optionally, remove the frame files
