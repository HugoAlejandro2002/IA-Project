import osmnx as ox
import shutil
import os
import random
import numpy as np

from dijkstra import init_dijkstra
from a_star import init_a_star

from haversine import haversine

def get_street_info(G, query):
    lat, lon = ox.geocode(query)
    # print(lat, lon)
    min_dist = np.inf
    nearest_node = None
    
    for node in list(G.nodes):
        node_lat = G.nodes[node]['y']
        node_lon = G.nodes[node]['x']
        
        dist = haversine((lat, lon), (node_lat, node_lon))
        
        if dist < min_dist:
            min_dist = dist
            nearest_node = node
    
    return nearest_node


if __name__ == "__main__":
    if os.path.isdir('frames'):
        shutil.rmtree('frames')

    place_name = "La Paz, Bolivia"
    G = ox.graph_from_place(place_name, network_type="drive")
    
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
    

    # start = random.choice(list(G.nodes))
    # end =  random.choice(list(G.nodes))
        
    start = get_street_info(G, input())
    end = get_street_info(G, input())

    # print(start, end)
    
    init_dijkstra(start, end, G)
    init_a_star(start, end, G)
    