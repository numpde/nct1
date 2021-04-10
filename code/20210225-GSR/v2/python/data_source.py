# RA, 2021-04-09

from bugs import *
from tcga.utils import First
from scipy.io import loadmat
import typing

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

    'RanBP1·Ran·GTP (c)': "RanGTP--RanBP1",
    # 'RanBP1 (c)': "RanBP1",

    'Free cargo (c)': "Cargo cyto",
    'Free cargo (n)': "Cargo nuc",

    'Cargo·Impβ (c)': "ImpB--Cargo cyto",
    'Cargo·Impβ (n)': "ImpB--Cargo nuc",
}


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
