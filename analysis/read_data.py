import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from itertools import zip_longest


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
    return lines[:-1]


def get_new_line(lst):
    return '\t'.join([s if s else 'NaN' for s, i in zip_longest(lst, range(41))])


if __name__ == '__main__':
    files = glob("data/experiment_data_*_*.csv")
    with open('analysis/files.txt') as fh:
        files = [f'experiment/data/{f[:-1]}' for f in fh]
    print(files)
    data = []
    for fn in files:
        name, identifier = fn.split('.csv')[0].split('_')[-2:]
        # if not 'lrjs' in identifier:
        #     continue  # this is tabea
        d = pd.read_csv(fn, sep=',')
        d['name'] = name
        d['id'] = identifier
        print(d.shape)
        data.append(d)
    data = pd.concat(data)
    idxs = ~np.isnan(data.response)
    data = data[idxs]
    # print(data)

    gb = data.groupby('id')
    ids = list(gb.groups.keys())

    data['duration'] = data.stimulus.apply(get_duration)
    rprop = data.groupby('duration').response.mean()
    data_x = rprop.index
    print(rprop)
    data_n = data.groupby('duration').response.agg(len)
    data_r = data.groupby('duration').response.sum()
    rprop.plot(style='.')
    plt.show()

    max_durations = 41

    with open('analysis/data_x.txt') as fh:
        lines = get_padded_lines(fh)
    line = get_new_line(rprop.index.map(str))
    lines.append(line+'\n')
    with open('analysis/data_x_c.txt', 'w') as fh:
        fh.writelines(lines)

    with open('analysis/data_n.txt') as fh:
        lines = get_padded_lines(fh)
    line = get_new_line(data_n.map(int).map(str))
    lines.append(line+'\n')
    with open('analysis/data_n_c.txt', 'w') as fh:
        fh.writelines(lines)

    with open('analysis/data_r.txt') as fh:
        lines = get_padded_lines(fh)
    line = get_new_line(data_r.map(int).map(str))
    lines.append(line+'\n')
    with open('analysis/data_r_c.txt', 'w') as fh:
        fh.writelines(lines)

    with open('analysis/data_rprop.txt') as fh:
        lines = get_padded_lines(fh)
    line = get_new_line(data_r.map(str))
    lines.append(line+'\n')
    with open('analysis/data_rprop_c.txt', 'w') as fh:
        fh.writelines(lines)
