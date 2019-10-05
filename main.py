import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.preprocessing import normalize
from matplotlib import pylab

def bar_chart(ax: plt.Axes, xvalues: list, yvalues: list, title: str, xlabel: str, ylabel: str, percentage=False):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(xvalues, rotation=90, fontsize='small')
    if percentage:
        ax.set_ylim(0.0, 1.0)
    ax.bar(xvalues, yvalues, edgecolor='grey')

def plotDegreeDistributionNormed(degreeFrequencies, show=True):
    degrees = [i for i in range(len(degreeFrequencies))]
    degreeFrequenciesNormed = normalize(np.reshape(degreeFrequencies, (degreeFrequencies.shape[0], 1)), axis=0).ravel()
    bar_chart(plt.gca(), xvalues=degrees, yvalues=degreeFrequenciesNormed, title='Degree distribution', xlabel='Degree Value', \
              ylabel='Percentage of nodes    with given degree')
    if show:
        plt.show()

def plotDegreeDistribution(degreeFrequencies, show=True):
    degrees = [i for i in range(len(degreeFrequencies))]
    bar_chart(plt.gca(), xvalues=degrees, yvalues=degreeFrequencies, title='Degree distribution', xlabel='Degree Value', \
              ylabel='Percentage of nodes    with given degree')
    if show:
        plt.show()

def drawGraphShit(G):

    ranks = nx.pagerank(G, alpha=0.85)
    x = list(ranks.values())
    siz = [i * 300000 for i in x]      # fixme

    smallColor = 'red'
    mediumColor = 'blue'
    bigColor = 'orange'

    quantile25 = np.quantile(x, .25)
    quantile75 = np.quantile(x, .85)

    nodeColor = [bigColor if i > quantile75 else mediumColor if i > quantile25\
        else smallColor for i in x]

    # plotdegreeDistributionNormed(degreeFrequencies)

    nx.draw_networkx(G, node_size=siz, node_color=nodeColor, with_labels=False)
    plt.show()

def drawGraph(graph, file_name, nodeColors):

    # Initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)

    pos = nx.spring_layout(graph)

    nx.draw_networkx_nodes(graph, pos, node_color=nodeColors)
    nx.draw_networkx_edges(graph, pos)
    # nx.draw_networkx_labels(graph, pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name, bbox_inches="tight")
    pylab.close()
    del fig

def drawGraphQuantile(G):
    ranks = nx.pagerank(G, alpha=0.85)
    x = list(ranks.values())

    smallColor = 'red'
    mediumColor = 'blue'
    bigColor = 'orange'

    quantile25 = np.quantile(x, .25)
    quantile75 = np.quantile(x, .85)

    nodeColor = [bigColor if i > quantile75 else mediumColor if i > quantile25 \
        else smallColor for i in x]

    drawGraph(G, 'graphVisualization', nodeColor)

def drawGiantComponent(G, file_name):
    try:
        import pygraphviz
        from networkx.drawing.nx_agraph import graphviz_layout
        layout = graphviz_layout
    except ImportError:
        try:
            import pydot
            from networkx.drawing.nx_pydot import graphviz_layout
            layout = graphviz_layout
        except ImportError:
            print("PyGraphviz and pydot not found;\n"
                  "drawing with spring layout;\n"
                  "will be slow.")
            layout = nx.spring_layout

    pos = layout(G)

    subGraphs = list(nx.connected_component_subgraphs(G, copy=True))

    giantComponent = subGraphs[0]
    otherComponents = subGraphs[1:]


    nx.draw_networkx_nodes(G,
                           with_labels=False,
                           alpha=0.3,
                           node_size=10,
                           pos=pos
                           )

    nx.draw_networkx_edges(giantComponent, pos,
                           with_labels=False,
                           edge_color='r',
                           alpha=1,
                           width=0.4
                           )
    for Gi in otherComponents:
        if len(Gi) > 1:
            nx.draw_networkx_edges(Gi, pos,
                                   with_labels=False,
                                   edge_color='green',
                                   alpha=0.4,
                                   width=0.4
                                   )


    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name, bbox_inches="tight", dpi=300)
    pylab.close()

G = nx.read_gml('power.gml', None)
degreeFrequencies = np.array(nx.degree_histogram(G))


# print(nx.info(G))
'''
Number of nodes: 4941
Number of edges: 6594
Average degree:   2.6691
'''

density = nx.density(G)                             # 0.0005403026973346214
globalclusteringCoefficient = nx.transitivity(G)    # 0.10315322452860086
localClusteringCoefficients = nx.clustering(G)
aspl = nx.average_shortest_path_length(G)             # 18.989185424445708


# plotDegreeDistributionNormed(degreeFrequencies)

# drawGraphQuantile(G)

# drawGiantComponent(G, 'giant')










