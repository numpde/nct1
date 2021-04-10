# RA, 2021-04-10

from bugs import *
from twig import log
from tcga.utils import First
from scipy.io import loadmat
import typing


def load_runs(folder) -> pd.DataFrame:
    load_tx = First(str).then(loadmat).then(pd.Series).then(
        lambda data: pd.DataFrame(
            index=pd.Series(data.t.squeeze(), name='t', dtype=float),
            columns=pd.Series(data.names.squeeze(), name='species').transform(unlist1),
            data=data.x,
            dtype=float,
        ).loc[data.t.squeeze() >= data.t_react.squeeze()]
    )

    load_params = First(str).then(loadmat).then(pd.Series).then(
        lambda data: data[["ImpB", "RanBP1", "RanGAP", "t_react"]].transform(lambda x: np.array(x).squeeze()),
    )

    data = pd.DataFrame({
        file.stem: pd.Series({
            'tx': load_tx(file),
            **load_params(file).to_dict()
        })
        for file in folder.glob("*.mat")
    })

    return data.T


runs = {
    folder.name: load_runs(folder)
    for folder in Path(__file__).parent.parent.glob("results*")
    if folder.is_dir()
}

log.info(f"Loaded runs from folders: {', '.join(runs)} .")

if __name__ == '__main__':
    print(runs)
