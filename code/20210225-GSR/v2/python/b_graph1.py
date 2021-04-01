# RA, 2021-04-01

"""
Visualize concentrations in a graph -- draft.
"""

from bugs import *
from twig import log
from scipy.io import loadmat
from scipy.interpolate import interp1d

from tcga.utils import First

import typing
import networkx as nx


def load_data() -> typing.Dict[str, pd.DataFrame]:
    load = First(str).then(loadmat).then(pd.Series).then(
        lambda data: pd.DataFrame(
            index=pd.Series(data.t.squeeze(), name='t', dtype=float),
            columns=pd.Series(data.names.squeeze(), name='species').transform(unlist1),
            data=data.x,
            dtype=float,
        )
    )

    data = {
        file.stem: load(file)
        for file in (Path(__file__).parent.parent / "results").glob("*.mat")
    }

    return data


def interp(data, t):
    return pd.Series(name=t, index=data.columns, data=interp1d(data.index, data, axis=0)(t))


def get_graph():
    g = nx.MultiDiGraph()

    species = {
        # Display name -- Matlab name

        # 'GTP': "GTP",
        # 'GDP': "GDP",

        'Ran·GTP (n)': "RanGTP_nuc",
        'Ran·GTP (c)': "RanGTP_cyto",

        # 'Total Ran·GTP (c)': "Total cyto RanGTP",

        'Ran·GDP (n)': "RanGDP_nuc",
        'Ran·GDP (c)': "RanGDP_cyto",

        # 'Tot Impβ (n)': "Total cyto ImpB",
        # 'Tot Impβ (c)': "Total nuc ImpB",

        'Free Impβ (n)': "ImpB nuc",
        'Free Impβ (c)': "ImpB cyto",

        'Impβ·Ran·GTP (n)': "ImpB--RanGTP nuc",
        'Impβ·Ran·GTP (c)': "ImpB--RanGTP cyto",

        # 'RanBP1·Ran·GTP (c)': "RanGTP--RanBP1",
    }

    g.add_nodes_from(species.keys())
    nx.set_node_attributes(g, species, name="matlab")

    # Flux and how to get its value
    g.add_edge('Ran·GTP (n)', 'Ran·GTP (c)', matlab="FluxRanGTP")
    g.add_edge('Ran·GDP (n)', 'Ran·GDP (c)', matlab="FluxRanGDP")
    g.add_edge('Ran·GTP (c)', 'Ran·GDP (c)', matlab="GAP")
    g.add_edge('Impβ·Ran·GTP (c)', 'Ran·GDP (c)', matlab="ImpB GAP")
    g.add_edge('Impβ·Ran·GTP (c)', 'Free Impβ (c)', matlab="ImpB GAP")
    g.add_edge('Free Impβ (n)', 'Free Impβ (c)', matlab="F ImpB")
    g.add_edge('Ran·GDP (n)', 'Ran·GTP (n)', matlab="Nuc RanGDP to RanGTP conversion")
    g.add_edge('Impβ·Ran·GTP (n)', 'Impβ·Ran·GTP (c)', matlab="F ImpB--RanGTP")
    g.add_edge('Impβ·Ran·GTP (n)', 'Free Impβ (n)', matlab="R nuc")
    g.add_edge('Impβ·Ran·GTP (n)', 'Ran·GTP (n)', matlab="R nuc")
    g.add_edge('Impβ·Ran·GTP (c)', 'Free Impβ (c)', matlab="R cyto")
    g.add_edge('Impβ·Ran·GTP (c)', 'Ran·GTP (c)', matlab="R cyto")

    if not set(g.nodes).issubset(species):
        log.warning(f"Don't know species: {set(g.nodes) - set(species)}.")

    return g


def show(g: nx.MultiDiGraph, state: pd.Series):
    pos = nx.shell_layout(g)
    pos = nx.planar_layout(g)
    pos = nx.spring_layout(g)
    pos = {
        'Free Impβ (c)': [-4, +3], 'Impβ·Ran·GTP (c)': [-3, +3], 'Ran·GTP (c)': [-2, +2], 'Ran·GDP (c)': [+2, +2],
        'Free Impβ (n)': [-4, -3], 'Impβ·Ran·GTP (n)': [-3, -3], 'Ran·GTP (n)': [-2, -2], 'Ran·GDP (n)': [+2, -2],
    }
    # pos = nx.get_node_attributes(g, name='pos')

    species = pd.Series(nx.get_node_attributes(g, name='matlab'))
    # species = pd.DataFrame({'matlab': species, 'value': species.map(state)})
    species = species.map(state)

    if any(species.isna()):
        log.warning(f"Species have no data: \n{list(species[species.isna()].index)}")

    # Directed multifluxes
    fluxes = pd.Series(nx.get_edge_attributes(g, name='matlab'))
    fluxes = pd.DataFrame({'matlab': fluxes, 'value': fluxes.map(state)})
    # Directed fluxes
    f = fluxes.reset_index().groupby(by=['level_0', 'level_1']).value.sum().to_dict()
    # One directed edge per pair - version of the graph
    ug = (lambda ug: nx.DiGraph(ug).edge_subgraph(ug.edges))(nx.Graph(g))
    # Combined fluxes
    fluxes = pd.Series(index=list(ug.edges), data=list(ug.edges)).transform(
        lambda e: (f.get(e, 0) - f.get((e[1], e[0]), 0))
    )

    if any(fluxes.isna()):
        log.warning(f"Fluxes have no data: \n{list(fluxes[fluxes.isna()].index)}")

    # log.info(f"Species: \n{species}")
    # log.info(f"Fluxes: \n{fluxes}")

    node_size = species.fillna(0)
    # node_size = node_size[node_size > 0]
    # node_size = node_size / node_size.sum()
    node_size = 300 * node_size

    edge_width = fluxes
    edge_width = edge_width[edge_width != 0]
    (fwd, bwd) = (edge_width[edge_width >= 0].index, edge_width[edge_width < 0].index)
    edge_width = edge_width.transform(lambda x: np.log10(np.abs(x)))
    edge_width = 1 + (edge_width - edge_width.min()) / ((edge_width.max() - edge_width.min()) or 1)

    edge_labels = fluxes.transform(lambda x: f"{x:0.02g}").to_dict()

    with Plox() as px:
        kw = dict(G=g, pos=pos, ax=px.a, alpha=0.8)
        nx.draw_networkx_nodes(**kw, nodelist=node_size.index, node_size=node_size, node_color="C0", linewidths=0)

        kw = dict(G=ug, pos=pos, ax=px.a, alpha=0.5, edge_color='g')
        nx.draw_networkx_edges(**kw, width=edge_width[fwd], edgelist=fwd)
        nx.draw_networkx_edges(**kw, width=edge_width[bwd], edgelist=[(v, ug) for (ug, v) in bwd])

        kw = dict(G=ug, pos=pos, ax=px.a, alpha=0.9)
        nx.draw_networkx_edge_labels(**kw, edge_labels=edge_labels, font_size=3)

        kw = dict(G=g, pos=pos, ax=px.a, alpha=0.7)
        nx.draw_networkx_labels(**kw, font_size=5, font_color='k', verticalalignment="bottom")

        px.show()


def main():
    data = load_data()

    data = data['Baseline']

    t = 7000
    state = interp(data, t)

    g = get_graph()
    show(g, state)


if __name__ == '__main__':
    main()
