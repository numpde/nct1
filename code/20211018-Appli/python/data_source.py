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
            columns=(
                pd.Series(data.names.squeeze(), name='species')
                    .transform(unlist1)
                # .transform(lambda sp: f"[{sp}]")
            ),
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

# sp_specs = [
#     {'+': "CAS"},
#     # {'+': "CAS", '-': "ImpA"},
#     {'+': "CAS·Ran·GTP"},
#     {'+': "ImpA·CAS·Ran·GTP"},
#     {'+': "ImpB"},
#     {'+': "ImpA"},
#     {'+': "ImpA·ImpB"},
#     {'+': "Ran·GTP"},
#     {'+': "NLS"},
# ]

suffixes = r"(\(n\))|(\(c\))|(·NPC)"

sp_specs = {
    "All CAS": r"(.*)(CAS)(.*)",
    "Free CAS": rf"^(CAS)({suffixes})$",

    "CAS·Ran·GTP": rf"^(CAS·Ran·GTP)({suffixes})$",
    "ImpA·CAS·Ran·GTP": rf"^(ImpA·CAS·Ran·GTP)({suffixes})$",

    "All ImpA": r"(.*)(ImpA)(.*)",
    "Free ImpA": rf"^(ImpA)({suffixes})$",

    "All ImpB": r"(.*)(ImpB)(.*)",
    "Free ImpB": rf"^(ImpB)({suffixes})$",

    "ImpA·ImpB": rf"^(ImpA·ImpB)({suffixes})$",

    "All Ran": rf"(.*)(Ran)(.*)",
    "All Ran·GTP": rf"(.*)(Ran·GTP)(.*)",
    "All Ran·GDP": rf"(.*)(Ran·GDP)(.*)",
    
    "Free Ran·GTP": rf"^(Ran·GTP)({suffixes})$",
    "Free Ran·GDP": rf"^(Ran·GDP)({suffixes})$",

    "All NLS": r"(.*)(NLS)(.*)",
    "Free NLS": rf"^(NLS)({suffixes})$",
}

NPC_CONCENTRATION_FACTOR = 100
IMG_WIDTH = 256  # on website

#

if __name__ == '__main__':
    pass
