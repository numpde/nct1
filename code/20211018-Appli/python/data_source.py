# RA, 2021-05-13

from bugs import *
from twig import log
from tcga.utils import First, unlist1
from scipy.io import loadmat

from plox import rcParam

base = unlist1(Path(__file__).parent.parent.glob("results*"))


def load_runs(folder) -> pd.DataFrame:
    load_tx = First(str).then(loadmat).then(pd.Series).then(
        lambda data: pd.DataFrame(
            index=pd.Series(data.t.squeeze(), name='t', dtype=float),
            columns=pd.Series(data.names.squeeze(), name='species').transform(unlist1),
            data=data.x,
            dtype=float,
        )
    )

    load_params = First(str).then(loadmat).then(pd.Series)

    data = pd.DataFrame({
        file.stem: pd.Series({
            'tx': load_tx(file),
            **load_params(file).to_dict()
        })
        for file in folder.glob("*.mat")
    })

    return data.T


runs = load_runs(base)

log.info(f"Loaded runs: {', '.join(runs.index)}")

#

style = {
    rcParam.Text.usetex: True,
    rcParam.Text.Latex.preamble: '\n'.join([r'\usepackage{siunitx}']),
    rcParam.Font.size: 14,
}

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

NPC_CONCENTRATION_FACTOR = 100
IMG_WIDTH = 256  # on website

#

if __name__ == '__main__':
    pass
