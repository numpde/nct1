# RA, 2021-04-07

from bugs import *
from plox import rcParam

path = Path(__file__).parent.parent / "results"
assert path.is_dir()

for file in path.glob("*.mat"):
    assert file.is_file()

    from scipy.io import loadmat

    data = pd.Series(loadmat(str(file)))
    # print(data)

    X = pd.DataFrame(
        index=pd.Series(data.t.squeeze(), name='t', dtype=float),
        columns=pd.Series(data.names.squeeze(), name='species').transform(unlist1),
        data=data.x,
        dtype=float,
    )

    x = X.iloc[-1]

    qoi = {
        "total_cargo_ratio": "{:0.01g}".format(x['Total cargo ratio']),
        "total_impb_ratio": "{:0.03g}".format(x['Total ImpB ratio']),
    }

    for (fn, q) in qoi.items():
        with (mkdir(Path(__file__).with_suffix('')) / f"{file.stem}_{fn}.tex").open(mode='w') as fd:
            print(q, file=fd, end="")
