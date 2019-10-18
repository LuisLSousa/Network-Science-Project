import pandas as pd
import numpy as np
import networkx as nx
import powerlaw

def calculateBasicStats(G):
    density = nx.density(G)  # orig: 0.0005403026973346214
    globalClusteringCoef = nx.transitivity(G)  # orig: 0.10315322452860086
    if nx.is_connected(G):
        avgShortPathLen = nx.average_shortest_path_length(G)  # orig: 18.989185424445708

    degrees = [i[1] for i in G.degree]
    alpha, sigma, loglikelihoodRatio, pVal = computePowerLawFitValues(degrees)

    giantComponentSize = calcGiantComponentSize(G)
    numComponents = nx.number_connected_components(G)

    d = [j for i, j in  list(G.degree())]
    avgDegree = sum(d)/len(d)

    # todo - Diameter??
    data = {k: v for k, v in locals().items()}
    del data['G']
    return data

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


def calcRemovedPercentage(G, initialNumNodes):
    return (1 - len(G.nodes())/initialNumNodes)


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

def calcGiantComponentSize(G):
    subGraphs = list(nx.connected_component_subgraphs(G, copy=True))
    giantComponent = max(subGraphs, key=len)
    return len(giantComponent.nodes())
