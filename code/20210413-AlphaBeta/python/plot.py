# RA, 2021-04-10

import numpy as np
import pandas as pd

from plox import rcParam

from bugs import *
from twig import log

import matplotlib.colors as mcolors

out_dir = mkdir(Path(__file__).with_suffix('').resolve())

style = {
    rcParam.Text.usetex: True,
    rcParam.Text.Latex.preamble: '\n'.join([r'\usepackage{siunitx}']),
}


def process(runs, species):
    with Plox(style) as px:
        fmt = {
            '(c)': dict(ls="--", lw=1, alpha=0.5),
            '(n)': dict(ls="-.", lw=1, alpha=0.9),
            'NPC': dict(ls="-", lw=1, alpha=0.8),
        }

        for s in fmt:
            px.a.plot(1, 0, **fmt[s], color='k', label=f"...{s}")

        runs = runs.sort_values(by='hydro')

        for (i, (datafile, run)) in enumerate(runs.iterrows()):
            hydro = np.squeeze(run.hydro)

            color = f"C{i}"
            label = r"$k_{\mathrm{hydrolysis}}$" + rf" = $\num{{{hydro:.01e}}}$ " + r"$\mathrm{s^{-1}}$"
            px.a.plot(1, 0, "-", color=color, label=label)

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
    from data_source import runs as all_runs

    for (folder, runs) in all_runs.items():
        for species in ["CAS", "ImpB", "ImpA", "GTP"]:
            for px in process(runs, species):
                if px:
                    img_file = mkdir(out_dir / folder) / f"{species}.png"
                    log.info(f"Writing {relpath(img_file)} .")
                    px.f.savefig(img_file)


if __name__ == '__main__':
    main()
