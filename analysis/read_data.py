import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from itertools import zip_longest
from collections import defaultdict


def get_duration(s):
    return int(s[7:10])


def string_or_nan(lst, N):
    for s, i in zip_longest(lst, range(N)):
        if s:
            yield s
        else:
            yield 'NaN'

def get_padded_lines(fh):
    lines = []
    for line in fh:
        lst = line[:-1].split('\t')
        lines.append('\t'.join([s for s in string_or_nan(lst, max_durations)])+'\n')
    return lines


def get_new_line(lst):
    return '\t'.join([s if s else 'NaN' for s, i in zip_longest(lst, range(41))])


if __name__ == '__main__':
    files = glob("data/experiment_data_*_*.csv")
    name_dict = defaultdict(list)
    with open('analysis/files.txt') as fh:
        for line in fh:
            name, fn = line.rstrip().split(',')
            print(fn)
            name_dict[name].append(fn)
    files = [f'experiment/data/{f}' for f in name_dict.values()]
    print(name_dict)

    datalst = []
    for name, fns in name_dict.items():
        for fn in fns:
            print(fn)
            name2, identifier = fn.split('.csv')[0].split('_')[-2:]
            if name != name2:
                print(name2, "is now called", name)
            # if not 'lrjs' in identifier:
            #     continue  # this is tabea
            d = pd.read_csv(f'experiment/data/{fn}', sep=',')
            d['name'] = name
            d['id'] = identifier
            print(name, identifier, d.shape)
            datalst.append(d)
    data = pd.concat(datalst, ignore_index=True)
    idxs = ~np.isnan(data.response)
    data = data[idxs]
    # print(data)
    data['duration'] = data['stimulus'].apply(get_duration)

    gb = data.groupby('name')
    names = list(gb.groups.keys())

    data_x, data_n, data_r, data_rprop = {}, {}, {}, {}
    for name, d in gb:
        # d['duration'] = d['stimulus'].apply(get_duration)
        data_rprop[name] = d.groupby('duration').response.mean()
        # print(data_rprop[name])
        data_x[name] = data_rprop[name].index
        # print(rprop)
        data_n[name] = d.groupby('duration').response.agg(len)
        # print(data_n[name])
        data_r[name] = d.groupby('duration').response.sum()
    # rprop.plot(style='.')
    # plt.show()

    max_durations = 41

    with open('analysis/data_x.txt') as fh:
        lines = get_padded_lines(fh)
    for name in names:
        line = get_new_line(data_x[name].map(str))
        lines.append(line+'\n')
    with open('analysis/data_x_c.txt', 'w') as fh:
        fh.writelines(lines)

    with open('analysis/data_n.txt') as fh:
        lines = get_padded_lines(fh)
    for name in names:
        line = get_new_line(data_n[name].map(int).map(str))
        lines.append(line+'\n')
    with open('analysis/data_n_c.txt', 'w') as fh:
        fh.writelines(lines)

    with open('analysis/data_r.txt') as fh:
        lines = get_padded_lines(fh)
    for name in names:
        line = get_new_line(data_r[name].map(int).map(str))
        lines.append(line+'\n')
    with open('analysis/data_r_c.txt', 'w') as fh:
        fh.writelines(lines)

    with open('analysis/data_rprop.txt') as fh:
        lines = get_padded_lines(fh)
    for name in names:
        line = get_new_line(data_rprop[name].map(str))
        lines.append(line+'\n')
    with open('analysis/data_rprop_c.txt', 'w') as fh:
        fh.writelines(lines)

    names = [f'Subject {i}' for i in range(1, 9)] + names
    with open('analysis/names.txt', 'w') as fh:
        fh.writelines(n + '\n' for n in names)
