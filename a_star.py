import osmnx as ox
import heapq
import imageio.v3 as imageio

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


def plot_state(step, state, alg):
    filename = f"frame_{step:05d}.png"
    filepath = f"frames/{alg}/{filename}"
    ox.plot_graph(
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
        bgcolor="#18080e",
    )


def distance(node1, node2):
    x1, y1 = G.nodes[node1]["x"], G.nodes[node1]["y"]
    x2, y2 = G.nodes[node2]["x"], G.nodes[node2]["y"]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def a_star(orig, dest, plot=False):
    alg = "build-a-star"
    for node in G.nodes:
        G.nodes[node]["previous"] = None
        G.nodes[node]["size"] = 0
        G.nodes[node]["g_score"] = float("inf")
        G.nodes[node]["f_score"] = float("inf")
    for edge in G.edges:
        style_unvisited_edge(edge)
    G.nodes[orig]["size"] = 50
    G.nodes[dest]["size"] = 50
    G.nodes[orig]["g_score"] = 0
    G.nodes[orig]["f_score"] = distance(orig, dest)
    pq = [(G.nodes[orig]["f_score"], orig)]
    step = 0
    while pq:
        _, node = heapq.heappop(pq)
        if node == dest:
            if plot:
                print("Iteraciones:", step)
                plot_state(step, G, alg)
                create_gif(alg)
            return
        for edge in G.out_edges(node):
            style_visited_edge((edge[0], edge[1], 0))
            neighbor = edge[1]
            tentative_g_score = G.nodes[node]["g_score"] + distance(node, neighbor)
            if tentative_g_score < G.nodes[neighbor]["g_score"]:
                G.nodes[neighbor]["previous"] = node
                G.nodes[neighbor]["g_score"] = tentative_g_score
                G.nodes[neighbor]["f_score"] = tentative_g_score + distance(
                    neighbor, dest
                )
                heapq.heappush(pq, (G.nodes[neighbor]["f_score"], neighbor))
                for edge2 in G.out_edges(neighbor):
                    style_active_edge((edge2[0], edge2[1], 0))
        if step % 100 == 0:
            plot_state(step, G, alg)
        step += 1


def reconstruct_path(orig, dest, plot=False, algorithm=None):
    alg = "reconstruct-a-star"
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
    imageio.imwrite(f"{filename}.gif", frames, duration=250, loop=0)
    states.clear()


def init_a_star(start_node, end_node, G_data):
    global G
    G = G_data
    a_star(start_node, end_node, plot=True)
    reconstruct_path(start_node, end_node, plot=True)
