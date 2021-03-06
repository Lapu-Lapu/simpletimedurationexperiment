import pandas as pd
import numpy as np
from subprocess import run

D = pd.read_csv('data/data_x.txt', sep='\t', header=None)
print(D)

d = D.values.flatten()
d = d.astype(int)
d = set(d[~np.isnan(d)])
d = sorted(d)
print(d)

for ms in d:
    cmd = f"ffmpeg -i experiment/sounds/Sine_wave_440.ogg -ss 00:00:00.000 -t 00:00:00.{ms} -c copy experiment/sounds/{ms}_ms.ogg"
    print(cmd)
    out = run(cmd.split())
    print(out.returncode)
