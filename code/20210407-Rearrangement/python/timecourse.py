# RA, 2021-04-07

from bugs import *
from plox import rcParam

path = Path(__file__).parent.parent / "results"
assert path.is_dir()

file = first(path.glob("*.mat"))
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

X = X[["ImpB", "ImpB'", "Cargo", "Cargo'", "Cargo·ImpB", "Cargo·ImpB*", "Cargo·ImpB*'"]]
X = X[(1e-1 <= X.index) & (X.index <= 1e3)]

kw = {
    "ImpB": dict(color='C0', ls='-', lw=3),
    "ImpB'": dict(color='C0', ls='--', lw=3),
    "Cargo": dict(color='C3', ls='-', lw=3),
    "Cargo'": dict(color='C3', ls='--', lw=3),
    "Cargo·ImpB": dict(color='C1', ls='-', lw=2),
    "Cargo·ImpB*": dict(color='C4', ls='-', lw=3),
    "Cargo·ImpB*'": dict(color='C4', ls='--', lw=3),
}

style = {
    rcParam.Font.size: 12,
}

with Plox(style) as px:
    for (i, c) in enumerate(X.columns):
        px.a.plot(X.index, X[c], **kw.get(c, {}), label=c, alpha=0.8)
    px.a.set_xscale('log')
    px.a.set_xlabel("Time, s")
    px.a.set_ylabel("Concentration, $\mu$M")
    px.a.set_yticks([0, 1, 2])
    px.a.grid(zorder=-10)
    px.a.legend(loc='upper left')

    for ex in ["png", "pdf"]:
        px.f.savefig(Path(__file__).with_suffix(f".{ex}"))

