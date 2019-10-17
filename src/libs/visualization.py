from matplotlib import pylab
import scipy.stats as stats
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import powerlaw


def drawGraphWithHubs(G, bigBoyPercentage, name, pos, dpi=180):
    # Initialize Figure
    # plt.figure(num=None, figsize=(20, 20), dpi=dpi)
    plt.figure(dpi=dpi)
    plt.axis('off')
    fig = plt.figure(1)

    # Calculations
    degrees = list(G.degree())
    degreeValues = [degree for node, degree in degrees]
    degreeValues = sorted(degreeValues, reverse=True)
    toKeep = len(degreeValues)*bigBoyPercentage
    degreeValues = degreeValues[0: int(toKeep)]
    nodeColors = ['r' if i[1] in degreeValues else 'b' for i in G.degree]

    nx.draw_networkx_nodes(G, pos, node_color=nodeColors)
    nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_labels(graph, pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(name + '.png', bbox_inches="tight")
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

    # Logarithmic bins
    powerlaw.plot_pdf(values, ax=ax, linear_bins=False, color='r')

    distributions = dict()
    multiple_line_chart(ax, values, distributions, 'Best fit for %s' % var, var, 'probability')

    fig.tight_layout()
    plt.legend(['Linearly spaced bins', 'logarithmically spaced bins'])
    plt.show()


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

def drawGiantComponent(G, file_name, pos):

    subGraphs = list(nx.connected_component_subgraphs(G, copy=True))

    giantComponent = max(subGraphs, key = len)
    subGraphs.remove(giantComponent)
    otherComponents = subGraphs if len(subGraphs) >= 1 else []

    nx.draw_networkx_nodes(G,
                           with_labels=False,
                           alpha=0.3,
                           node_size=10,
                           pos=pos
                           )

    nx.draw_networkx_edges(giantComponent, pos,
                           with_labels=False,
                           edge_color='red',
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
    #plt.xlim(0, xmax)
    #plt.ylim(0, ymax)

    plt.savefig(file_name, bbox_inches="tight", dpi=300)
    pylab.close()

def drawGraphWithHubsV2(G, pos, bigBoyPercentage, name, dpi=180):

    degrees = list(G.degree())
    degreeValues = [degree for node, degree in degrees]
    degreeValues = sorted(degreeValues, reverse=True)
    toKeep = len(degreeValues) * bigBoyPercentage
    degreeValues = degreeValues[0: int(toKeep)]

    degree_threshold = degreeValues[-1]

    # Initialze Figure
    plt.figure(dpi=dpi)
    plt.axis('off')
    fig = plt.figure(1)

    hubs, notHubs = extractHubs(G, degree_threshold)

    nx.draw_networkx_nodes(G, pos, nodelist=notHubs, node_color='blue', alpha=0.4, node_size=5)
    nx.draw_networkx_nodes(G, pos, nodelist=hubs, node_color='red', node_size=10)
    nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_labels(graph, pos)

    plt.savefig(name + '.png', bbox_inches="tight")

    pylab.close()
    del fig


def extractHubs(G, degree_threshold=10):
    hubs = []
    notHubs = []
    for i in G:
        if G.degree(i) >= degree_threshold:
            hubs.append(i)
        else:
            notHubs.append(i)
    return hubs, notHubs