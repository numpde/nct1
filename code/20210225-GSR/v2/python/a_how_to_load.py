# RA, 2021-04-01

"""
Demo how to read the matlab files.
"""

from bugs import *

path = Path(__file__).parent.parent / "results"
assert path.is_dir()

file = first(path.glob("*.mat"))
assert file.is_file()

from scipy.io import loadmat

data = pd.Series(loadmat(str(file)))
# print(data)

x = pd.DataFrame(
    index=pd.Series(data.t.squeeze(), name='t', dtype=float),
    columns=pd.Series(data.names.squeeze(), name='species').transform(unlist1),
    data=data.x,
    dtype=float,
)

print(x)
"""
species       RanGTP_nuc  ...      ImpB GAP
t                         ...              
0.000000        0.000000  ...  0.000000e+00
0.009652        0.000029  ...  3.262940e-11
0.019304        0.000131  ...  2.184277e-10
0.027118        0.000288  ...  5.932979e-10
0.034932        0.000531  ...  1.385795e-09
...                  ...  ...           ...
4812.828157     3.288096  ...  3.847590e-02
5616.930540     3.288083  ...  3.847640e-02
6421.032923     3.288082  ...  3.847644e-02
7225.135306     3.288092  ...  3.847604e-02
10000.000000    3.288090  ...  3.847613e-02
"""

