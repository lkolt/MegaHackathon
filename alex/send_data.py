import alex.create_dataset as cr_data
import requests
import random
import time

for x in cr_data.create_norm_params(cr_data.contr):
    r = requests.post('http://10.0.1.107:8000/api/postControllers', json=x)
    time.sleep(1)

# f1 = cr_data.create_norm_params(cr_data.contr)
# f2 = cr_data.create_norm_params(cr_data.contr2)
# print(f1.__next__())
# print(f2.__next__())
# print(f1.__next__())