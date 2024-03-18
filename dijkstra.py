import osmnx as ox
import heapq
import imageio.v3 as imageio

from colors import *

## Si se desea probar el código por separado descomentar las siguientes líneas 

# import shutil
# import os

# if os.path.isdir('frames'):
#     shutil.rmtree('frames')

# place_name = "La Paz, Bolivia"
# G = ox.graph_from_place(place_name, network_type="drive")
G = None
states = []

def style_unvisited_edge(edge):
    G.edges[edge]["color"] = UNVISITED_EDGE_COLOR
    G.edges[edge]["alpha"] = 0.2
    G.edges[edge]["linewidth"] = 0.5

def style_visited_edge(edge):
    G.edges[edge]["color"] = VISITED_EDGE_COLOR
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_active_edge(edge):
    G.edges[edge]["color"] = ACTIVE_EDGE_COLOR
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_path_edge(edge):
    G.edges[edge]["color"] = PATH_EDGE_COLOR
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def plot_state(step, state, alg):
    filename = f"frame_{step:05d}.png"        
    filepath=f"frames/{alg}/{filename}"
    ox.plot_graph(
        state,
        node_size=[state.nodes[node]["size"] for node in state.nodes],
        edge_color=[state.edges[edge]["color"] for edge in state.edges],
        edge_alpha=[state.edges[edge]["alpha"] for edge in state.edges],
        edge_linewidth=[state.edges[edge]["linewidth"] for edge in state.edges],
        node_color=PATH_EDGE_COLOR ,
        bgcolor=BG_COLOR,
        figsize=(20, 20),
        show=False,
        save=True,
        close=True,
        filepath=filepath,
    )
    states.append(filepath)

def plot_heatmap(algorithm):
    edge_colors = ox.plot.get_edge_colors_by_attr(G, f"{algorithm}_uses", cmap="hot")
    fig, _ = ox.plot_graph(
        G,
        node_size=0,
        edge_color=edge_colors,
        # bgcolor="#9a9745"
        bgcolor=BG_COLOR,
    )


def dijkstra(orig, dest, plot=False):
    alg = "build-dijkstra"
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
                plot_state(step, G, alg)
                create_gif(alg)
                return
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
        if step % 300 == 0:
            plot_state(step, G, alg)
        step += 1


def reconstruct_path(orig, dest, plot=False, algorithm=None):
    alg = "reconstruct-dijkstra"
    for edge in G.edges:
        style_unvisited_edge(edge)
    dist = step = 0
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
        if step % 5 == 0:
           plot_state(step, G, alg)
        step += 1
    plot_state(step, G, alg)
    dist /= 1000
    if plot:
        print(f"Distance: {dist}")
        print(f"Avg. speed: {sum(speeds)/len(speeds)}")
        print(f"Total time: {dist/(sum(speeds)/len(speeds)) * 60}")
        create_gif(alg)

def create_gif(filename):
    frames = []
    for image in states:
        frames.append(imageio.imread(image))
    imageio.imwrite(f"{filename}.gif", frames, duration = 250, loop = 0)
    states.clear()  

def init_dijkstra(start_node, end_node, G_data):
    global G
    G = G_data
    dijkstra(start_node, end_node, plot=True)
    reconstruct_path(start_node, end_node, plot=True)
