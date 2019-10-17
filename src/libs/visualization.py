from matplotlib import pylab
import scipy.stats as stats
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import powerlaw

def drawGraphWithHubs(G, bigBoyPercentage, name):
    # Initialize Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)

    pos = nx.spring_layout(G)

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
