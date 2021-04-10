# RA, 2021-04-10

from bugs import *
from twig import log

out_dir = mkdir(Path(__file__).with_suffix('').resolve())


def process(runs):
    import matplotlib.colors as mcolors
    assert [runs.tx, runs.ImpB, runs.RanBP1, runs.RanGAP, runs.t_react]

    with Plox() as px:
        runs = runs.assign(m=runs.tx.apply(lambda X: X['Total GTP'][X.index <= min(X.index) + 100].median()))
        runs = runs.sort_values(by='m', ascending=False)

        for ((name, run), color) in zip(runs.iterrows(), mcolors.TABLEAU_COLORS):
            X = run.tx
            X.index = X.index - min(X.index)

            marker = dict(marker="o", mfc="none", mec="k")

            if run.ImpB and run.RanBP1:
                marker = dict(marker="s", mfc="none", mec="k")

            if run.ImpB and not run.RanBP1:
                marker = dict(marker="s", mfc="k", mec="k")

            if not run.ImpB and run.RanBP1:
                marker = dict(marker="^", mfc="none", mec="k")

            if not run.ImpB and not run.RanBP1:
                marker = dict(marker="o", mfc="k", mec="k")

            label = f"RanBP1 = {run.RanBP1}µM, ImpB = {run.ImpB}µM"
            ii = (X.index == min(X.index[X.index >= 100]))
            px.a.plot(X.index, X['Total GTP'], '-', color=color)
            px.a.plot(X.index[ii], X['Total GTP'][ii], '-', color=color, **marker, label=label)

        px.a.set_xlabel("Time")
        px.a.set_ylabel("Total GTP, µM")

        px.a.legend(loc='upper right')

        yield px


def main():
    from data_source import runs

    runs = runs['results_fig4a']

    for (RanGAP, runs) in runs.groupby('RanGAP'):
        if RanGAP:
            for px in process(runs):
                px.f.savefig(out_dir / f"RanGAP={RanGAP}.png")


if __name__ == '__main__':
    main()
