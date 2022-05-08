# -- coding: utf-8 --
# RA, 2021-04-10

import re
import os.path

import numpy as np
import pandas as pd

import contextlib

from bugs import *
from tcga.utils import from_iterable
from twig import log
from plox import rcParam

out_dir = mkdir(Path(__file__).resolve().with_suffix(''))

from data_source import style, sp_specs, NPC_CONCENTRATION_FACTOR, IMG_WIDTH

# Wide-ish figure
style.update({
    rcParam.Figure.figsize: (8, 3),
    rcParam.Axes.labelsize: 'large',
    rcParam.Xtick.labelsize: 'large',
    rcParam.Ytick.labelsize: 'large',
    rcParam.Legend.fontsize: 'medium',
})


def plot_total_timecourse(run, spp):
    with Plox(style) as px:
        fmt = {
            '(c)': dict(ls="--", lw=3, alpha=0.5),
            '(n)': dict(ls="-.", lw=3, alpha=0.9),
            'NPC': dict(ls="-", lw=3, alpha=0.8),
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
            if suffix == 'NPC':
                f = NPC_CONCENTRATION_FACTOR
            else:
                f = 1

            x = tx[spp].sum(axis=1) * f
            px.a.plot(tx.index / 3600, x, **fmt[suffix], color=color)

        px.a.set_yticks([y for y in px.a.get_yticks() if (y >= 0)])
        px.a.set_yticklabels([f"{y:.2g}" for y in px.a.get_yticks()])

        px.a.set_xlabel(f"Time, h")

        px.a.set_xscale('log')
        px.a.legend(loc="upper left")

        yield px


def main():
    from data_source import runs

    summary = pd.DataFrame()

    for (i, run) in sorted(runs.iterrows()):
        for (sp_display, sp_pattern) in sp_specs.items():
            # Species to include in the plot
            collect_spp = [candidate for candidate in run.tx.columns if re.match(sp_pattern, candidate)]

            if collect_spp:
                log.info(f"Species for spec `{sp_display}`: {collect_spp}.")
            else:
                log.warning(f"No species selected for spec `{sp_display}`.")

            # File name and proto-ylabel
            name = sp_display

            for px in plot_total_timecourse(run, collect_spp):
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
                    lambda p: f'<a href="{p}"><img style="width:{IMG_WIDTH}px" src="{p}"/></a>'
                ).to_html(
                    escape=False
                )
            )


if __name__ == '__main__':
    main()
