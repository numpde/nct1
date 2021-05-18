# RA, 2021-04-10

import numpy as np
import pandas as pd

from plox import rcParam

from bugs import *
from twig import log

import matplotlib.colors as mcolors

out_dir = mkdir(Path(__file__).resolve().with_suffix(''))

style = {
    rcParam.Text.usetex: True,
    rcParam.Text.Latex.preamble: '\n'.join([r'\usepackage{siunitx}']),
}


def plot_total(run, species):
    with Plox(style) as px:
        fmt = {
            '(c)': dict(ls="--", lw=1, alpha=0.5),
            '(n)': dict(ls="-.", lw=1, alpha=0.9),
            'NPC': dict(ls="-", lw=1, alpha=0.8),
        }

        for s in fmt:
            px.a.plot(1, 0, **fmt[s], color='k', label=f"...{s}")

        color = f"C{0}"
        # px.a.plot(1, 0, "-", color=color, label=label)

        tx: pd.DataFrame = run.tx
        for suffix in ["(c)", "(n)", "NPC"]:
            s = [s for s in tx.columns if (species in s) and (s.endswith(suffix))]
            x = tx[s].sum(axis=1)
            px.a.plot(tx.index / 3600, x, **fmt[suffix], color=color)

        px.a.set_xlabel(f"Time, h")
        px.a.set_ylabel(f"Total {species}, " + r"$\mu$M")

        px.a.set_xscale('log')
        px.a.legend(fontsize=7)

        yield px


def main():
    from data_source import runs

    for (i, run) in runs.iterrows():
        for species in ["CAS", "ImpB", "ImpA", "GTP", "NLS"]:
            for px in plot_total(run, species):
                img_file = mkdir(out_dir / i) / f"total_{species}.png"
                log.info(f"Writing {relpath(img_file)} .")
                px.f.savefig(img_file)


if __name__ == '__main__':
    main()
