from api import get_friends
import time
import igraph
from igraph import Graph, plot
import numpy as np


def get_network(user_id, as_edgelist=True, backoff_factor=0.3):

    response = get_friends(user_id, 'id')['response']['items']
    uid_list = []
    network = []
    sec_uid_list = []
    for l in range(len(response)):
        uid = response[l]['id']
        name = response[l]['first_name'] + ' ' + response[l]['last_name']
        uid_list.append((uid, name))

    for i in range(len(uid_list)):
        n = 1
        try:
            sec_friends = get_friends(
                uid_list[i][0], 'id')['response']['items']
        except KeyError:
            print('Wait...')
            delay = backoff_factor * (2 ** n)
            time.sleep(delay)
            continue

        for j in range(len(sec_friends)):
            sec_uid = sec_friends[j]['id']
            for k in range(len(uid_list)):
                if uid_list[k][0] == sec_uid:
                    network.append((i, k))

    for i in range(len(uid_list)):
        print(f'{i}: {uid_list[i][1]}')

    return network


def plot_graph(graph, get_list=True):

    last_vert = 0
    for m in range(len(graph)):
        for n in graph[m]:
            if last_vert > max(graph[m]):
                continue
            last_vert = max(graph[m])
    vertices = [i for i in range(last_vert + 1)]

    g = Graph(vertex_attrs={"label": vertices},
              edges=graph, directed=False
              )
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)
    g.simplify(multiple=True, loops=True)

    try:
        communities = g.community_edge_betweenness(directed=False)
        clusters = communities.as_clustering()
        print(clusters)
        pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
        g.vs['color'] = pal.get_many(clusters.membership)
    except igraph._igraph.InternalError:
        pass
    finally:
        plot(g, **visual_style)


if __name__ == '__main__':
    print(plot_graph(get_network(user_id)))
