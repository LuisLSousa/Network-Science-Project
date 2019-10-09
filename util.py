import matplotlib.colors as mcolors
from sklearn.preprocessing import normalize
from matplotlib import pylab
import scipy.stats as stats
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import powerlaw


def bar_chart(ax: plt.Axes, xvalues: list, yvalues: list, title: str, xlabel: str, ylabel: str, percentage=False,
              logScale=False):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if logScale:
        ax.set_yscale('log')
        ax.set_xscale('log')
    if percentage:
        ax.set_ylim(0.0, 1.0)
    ax.bar(xvalues, yvalues, edgecolor='grey')

def plotDegreeDistribution(degreeFrequencies, show=True, logScale=False):
    degrees = [i for i in range(len(degreeFrequencies))]
    bar_chart(plt.gca(), xvalues=degrees, yvalues=degreeFrequencies, title='Degree distribution', xlabel='Degree Value', \
              ylabel='Nº of nodes with given degree', logScale=logScale)
    if show:
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

    smallColor = 'r'
    mediumColor = 'orange'
    bigColor = 'b'

    # quantile25 = np.quantile(x, .25)
    quantile85 = np.quantile(x, .85)

    # nodeColor = [bigColor if i > quantile85 else mediumColor if i > quantile25 else smallColor for i in x]
    nodeColor = [bigColor if i > quantile85 else smallColor for i in x]

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

def drawGraphWithHubs(G):
    # Initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)

    pos = nx.spring_layout(G)
    degrees = list(G.degree)
    nodeColors = ['r' if i[1] >=17 else 'b' for i in G.degree]

    nx.draw_networkx_nodes(G, pos, node_color=nodeColors)
    nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_labels(graph, pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig('graphWithHubs', bbox_inches="tight")
    pylab.close()
    del fig


def drawDegreeDistributionWithPowerLaw(degrees):
    fig = plt.figure()
    ax = plt.axes()

    series = pd.Series(degrees)
    bins = 20
    var = 'Degree frequencies'

    values = series.sort_values().values

    n, bins, patches = ax.hist(values, bins, density=True, edgecolor='grey')

    # Linear bins
    powerlaw.plot_pdf(values, ax=ax, linear_bins=True, color='b')

    # Logoritmic bins
    powerlaw.plot_pdf(values, ax=ax, linear_bins=False, color='r')

    distributions = dict()
    multiple_line_chart(ax, values, distributions, 'Best fit for %s' % var, var, 'probability')

    fig.tight_layout()
    plt.legend(['Linearly spaced bins', 'logarithmically spaced bins'])
    plt.show()

def computePowerLawFitValues(degrees):
    series = pd.Series(degrees)

    # Linear vs Logarithmic Bins
    results = powerlaw.Fit(degrees)
    alpha = results.power_law.alpha
    sigma = results.power_law.sigma
    loglikelihoodRatio, pVal = results.distribution_compare('power_law', 'lognormal')
    print('Best values for power law fit: alpha({}) sigma({}) loglikelihoodRatio({}) pVal({})'.format(
        alpha, sigma, loglikelihoodRatio, pVal))

    return alpha, sigma, loglikelihoodRatio, pVal

def multiple_line_chart(ax, xvalues, yvalues, title, xlabel, ylabel, percentage=False):
    legend: list = []
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if percentage:
        ax.set_ylim(0.0, 1.0)
    for name, y in yvalues.items():

        ax.plot(xvalues, y)
        legend.append(name)
    ax.legend(legend, loc='best', fancybox=True, shadow=True)