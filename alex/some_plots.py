import alex.create_dataset as cr_data
from matplotlib import pyplot as plt
import numpy as np

ar = []
f1 = cr_data.create_norm_params(cr_data.contr)
for x in range(100):
    ar.append(f1.__next__())
ar = [ar[x]['sensors'] for x in range(100)]
for x in range(100):
    ar[x] = list(map(lambda y: y['value'], ar[x]))
ar = np.array(ar)
print(ar[:, 3])


for x in range(len(cr_data.contr.ports)):
    plt.axes([0, 100, int(cr_data.contr.ports[x].min_val * 0.5), int(cr_data.contr.ports[x].max_val * 1.5)])
    plt.plot(list(range(100)), np.array(map(float, ar[:, x])))
    plt.show()