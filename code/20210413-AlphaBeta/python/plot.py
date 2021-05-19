# -- coding: utf-8 --
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


def plot_total(run, include):
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
            spp = [sp for sp in include if sp.endswith(suffix)]
            x = tx[spp].sum(axis=1)
            px.a.plot(tx.index / 3600, x, **fmt[suffix], color=color)

        px.a.set_xlabel(f"Time, h")

        px.a.set_xscale('log')
        px.a.legend(fontsize=7)

        yield px


def main():
    from data_source import runs

    spp = [
        {'+': "CAS", '-': "ΔCAS"},
        {'+': "ΔCAS"},
        {'+': "ImpB"},
        {'+': "ImpA"},
        {'+': "GTP"},
        {'+': "NLS"},
    ]

    # `Not a species` string
    nas = ("?" * 100)

    for (i, run) in runs.iterrows():
        for sp_spec in spp:
            include = [c for c in run.tx.columns if (sp_spec['+'] in c) and not (sp_spec.get('-', nas) in c)]
            name = sp_spec['+'] + (f" (excl. {sp_spec['-'] })" if ('-' in sp_spec) else "")
            for px in plot_total(run, include):

                ylabel = fr"{name}, $\mu$M"
                ylabel = ylabel.replace("Δ", r"$\Delta$")
                px.a.set_ylabel(ylabel)

                img_file = mkdir(out_dir / i) / f"{name}.png"
                log.info(f"Writing {relpath(img_file)} .")
                px.f.savefig(img_file)


if __name__ == '__main__':
    main()
