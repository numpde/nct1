# -- coding: utf-8 --
# RA, 2021-10-01

import os.path

import numpy as np
import pandas as pd

import contextlib

from bugs import *
from tcga.utils import from_iterable
from twig import log
from plox import rcParam

import matplotlib.colors as mcolors

# from sigfig import round

out_dir = mkdir(Path(__file__).resolve().with_suffix(''))

from data_source import style, sp_specs, NPC_CONCENTRATION_FACTOR, IMG_WIDTH

# Wide figure
style.update({rcParam.Figure.figsize: (9, 1)})


def plot_total_steadystate(run, spp):
    with Plox(style) as px:
        fmt = {
            '(c)': dict(ls="--", lw=2, alpha=0.5),
            '(n)': dict(ls="-.", lw=2, alpha=0.9),
            'NPC': dict(ls="-", lw=2, alpha=0.8),
        }

        # for s in fmt:
        #     px.a.plot(1, 0, **fmt[s], color='k', label=f"...{s}")

        color = f"C{0}"
        # px.a.plot(1, 0, "-", color=color, label=label)

        # Aggregate by suffix
        spp_by_suffix = {
            suffix: [sp for sp in spp if sp.endswith(suffix)]
            for suffix in ["(c)", "NPC", "(n)"]  # order for display
        }

        if len(spp) != sum(map(len, spp_by_suffix.values())):
            log.warning(f"Unknown suffix for species: {set(spp) - set(from_iterable(spp_by_suffix.values()))}")

        # `time` x `species` table of concentrations
        tx: pd.DataFrame = run.tx

        agg_by_suffix = pd.DataFrame(data={
            suffix: tx[spp].sum(axis=1) * (
                NPC_CONCENTRATION_FACTOR if (suffix == 'NPC') else 1
            )
            for (suffix, spp) in spp_by_suffix.items()
        })

        x01: pd.DataFrame = agg_by_suffix.iloc[[0, -1]]

        # Make heatmap

        cmap = mcolors.LinearSegmentedColormap.from_list('concentration', ["white", "darkblue"])

        # vmax = 10 ** np.ceil(np.log10(x01.max().max()))
        # vmax = x01.values.sum().sum()
        vmax = x01.loc[:, spp_by_suffix].sum(axis=1).max()

        # sanity fix
        vmax = (vmax if not np.isclose(vmax, 0) else 1)

        im = px.a.imshow(x01, cmap=cmap, vmin=0, vmax=vmax, origin="upper", aspect="auto")

        assert (2 == len(x01.index)), "Expect initial and final state in rows."
        px.a.set_yticks(np.arange(0, len(x01.index)))
        px.a.set_yticklabels(["Initial", "Final"])

        px.a.set_xticks(np.arange(0, len(x01.columns)))
        px.a.set_xticklabels(x01.columns)

        for i in range(x01.shape[0]):
            for j in range(x01.shape[1]):
                alignment = dict(ha="center", va="center")
                im.axes.text(j, i, "{:.3g}".format(x01.iloc[i, j]), fontsize=17, color="red", **alignment)

        # (xlim, ylim) = (px.a.get_xlim(), px.a.get_ylim())

        yield px


def main():
    from data_source import runs

    # `Not a species` placeholder
    nas = ("?" * 100)

    summary = pd.DataFrame()

    for (i, run) in sorted(runs.iterrows()):
        for sp_spec in sp_specs:
            # Species to include in the plot
            spp = [c for c in run.tx.columns if (sp_spec['+'] in c) and not (sp_spec.get('-', nas) in c)]

            # File name and proto-ylabel
            name = sp_spec['+'] + (f" (excl. {sp_spec['-']})" if ('-' in sp_spec) else "")

            for px in plot_total_steadystate(run, spp):
                img_file = mkdir(out_dir / i) / f"{name}.png"
                summary.loc[name, i] = img_file

                label = fr"{name}, $\mu$M"
                label = label.replace("Δ", r"$\Delta$")  # pdflatex issue with UTF
                px.a.set_title(label)

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
