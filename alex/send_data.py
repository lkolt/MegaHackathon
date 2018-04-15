import alex.create_dataset as cr_data
import requests
import random
import time

f = []
s = int(time.time())
f.append(cr_data.create_norm_params(cr_data.contr, s))
f.append(cr_data.create_norm_params(cr_data.contr2, s))
f.append(cr_data.create_norm_params(cr_data.contr3, s))
f.append(cr_data.create_norm_params(cr_data.contr4, s))
f.append(cr_data.create_norm_params(cr_data.contr5, s))
f.append(cr_data.create_norm_params(cr_data.contr6, s))


#q = requests.post('http://10.0.1.107:8000/api/postControllers', json=f[0].__next__())

s = int(time.time())
d = 0
while True:
    for x in f:
        q = requests.post('http://10.0.1.107:8000/api/postControllers', json=x.__next__())
