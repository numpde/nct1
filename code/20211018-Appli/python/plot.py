# -- coding: utf-8 --
# RA, 2021-04-10

import os.path

import numpy as np
import pandas as pd

import contextlib
from plox import rcParam

from bugs import *
from tcga.utils import from_iterable
from twig import log

import matplotlib.colors as mcolors

out_dir = mkdir(Path(__file__).resolve().with_suffix(''))

style = {
    rcParam.Text.usetex: True,
    rcParam.Text.Latex.preamble: '\n'.join([r'\usepackage{siunitx}']),
    rcParam.Font.size: 14,
}


def plot_total_timecourse(run, spp):
    with Plox(style) as px:
        fmt = {
            '(c)': dict(ls="--", lw=2, alpha=0.5),
            '(n)': dict(ls="-.", lw=2, alpha=0.9),
            'NPC': dict(ls="-", lw=2, alpha=0.8),
        }

        for s in fmt:
            px.a.plot(1, 0, **fmt[s], color='k', label=f"...{s}")

        color = f"C{0}"
        # px.a.plot(1, 0, "-", color=color, label=label)

        # Aggregate by suffix
        spp_by_suffix = {
            suffix: [sp for sp in spp if sp.endswith(suffix)]
            for suffix in {"(c)", "(n)", "NPC"}
        }

        if len(spp) != sum(map(len, spp_by_suffix.values())):
            log.warning(f"Unknown suffix for species: {set(spp) - set(from_iterable(spp_by_suffix.values()))}")

        # time x species table of concentrations
        tx: pd.DataFrame = run.tx

        for (suffix, spp) in spp_by_suffix.items():
            x = tx[spp].sum(axis=1)
            px.a.plot(tx.index / 3600, x, **fmt[suffix], color=color)

        px.a.set_xlabel(f"Time, h")

        px.a.set_xscale('log')
        px.a.legend(fontsize=10)

        yield px


def main():
    from data_source import runs

    sp_specs = [
        {'+': "CAS"},
        {'+': "CAS·Ran·GTP"},
        {'+': "ImpA·CAS·Ran·GTP"},
        {'+': "ImpB"},
        {'+': "ImpA"},
        {'+': "ImpA·ImpB"},
        {'+': "Ran·GTP"},
        {'+': "NLS"},
    ]

    # `Not a species` placeholder
    nas = ("?" * 100)

    summary = pd.DataFrame()

    for (i, run) in sorted(runs.iterrows()):
        for sp_spec in sp_specs:
            # Species to include in the plot
            spp = [c for c in run.tx.columns if (sp_spec['+'] in c) and not (sp_spec.get('-', nas) in c)]

            if not spp:
                log.warning(f"No species selected for spec `{sp_spec}`.")

            # File name and proto-ylabel
            name = sp_spec['+'] + (f" (excl. {sp_spec['-']})" if ('-' in sp_spec) else "")

            for px in plot_total_timecourse(run, spp):
                img_file = mkdir(out_dir / i) / f"{name}.png"
                summary.loc[name, i] = img_file

                ylabel = fr"{name}, $\mu$M"
                ylabel = ylabel.replace("Δ", r"$\Delta$")  # pdflatex issue with UTF
                px.a.set_ylabel(ylabel)

                log.info(f"Writing: {relpath(img_file)}")
                px.f.savefig(img_file)

    # Write an HTML overview

    with (out_dir / "index.html").open(mode='w') as fd:
        with contextlib.redirect_stdout(fd):
            print(
                summary.applymap(
                    lambda p: os.path.relpath(p, out_dir)
                ).applymap(
                    lambda p: f'<a href="{p}"><img style="width:196px" src="{p}"/></a>'
                ).to_html(
                    escape=False
                )
            )


if __name__ == '__main__':
    main()
