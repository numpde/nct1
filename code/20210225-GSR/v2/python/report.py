# RA, 2021-04-09

from bugs import *
from data_source import load_data, species


def report(state: pd.Series):
    x = {
        'free_cargo_ratio':
            state[species['Free cargo (n)']] /
            state[species['Free cargo (c)']],

        'nuc_to_cyto_cargo_ratio':
            state[[species['Free cargo (n)'], species['Cargo·Impβ (n)']]].sum() /
            state[[species['Free cargo (c)'], species['Cargo·Impβ (c)']]].sum(),
    }

    for (n, x) in x.items():
        with (mkdir(Path(__file__).with_suffix('') / "report") / f"{n}.tex").open(mode='w') as fd:
            print(int(x), file=fd, end="")


def main():
    report(load_data()['Baseline'].iloc[-1])


if __name__ == '__main__':
    main()
