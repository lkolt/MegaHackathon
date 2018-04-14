import time
import random
import json


class User:
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

class Port:
    def __init__(self, id, type, min_val, max_val):
        self.id = id
        self.type = type
        self.min_val = min_val
        self.max_val = max_val

    def __hash__(self):
        return hash((self.id, self.type))

    def __eq__(self, other):
        return (self.id, self.type) == (other.id, other.type)


class Controller:
    def __init__(self, ports, mac):
        self.ports = ports
        self.mac = mac

def mean_param(port):
    return (port.min_val + port.max_val) // 2

def in_min_max(val, port):
    return port.min_val <= val <= port.max_val

def sens_norm_params(prev, go_to):
    tmp = prev + go_to_val(prev, go_to)
    return tmp

def go_to_val(val, go_to):
    if go_to == val:
        return 0
    return (go_to - val) // abs(go_to - val)

def norm_params(controller, prev, go_to):
    dic = {'time': prev['time'] + 1,
            'sensors': {x : sens_norm_params(prev['sensors'][x], go_to[x]) for x in controller.ports},
           'mac' : controller.mac
    }
    return dic

def get_A_B(port):
    delt = (port.max_val - port.min_val) // 7
    mean_val = (port.min_val + port.max_val) // 2
    return mean_val - delt, mean_val + delt

def create_norm_params(controller):
    dic = {'time' : time.time(),
           'sensors' : {x : mean_param(x) for x in controller.ports},
           'mac' : controller.mac
           }

    prev = dic
    ab_vals = {x : get_A_B(x) for x in controller.ports}
    go_to = {x : random.randint(*ab_vals[x]) for x in ab_vals}
    while True:
        prev = norm_params(controller, prev, go_to)
        for x in prev['sensors']:
            if prev['sensors'][x] == go_to[x]:
                go_to[x] = random.randint(*ab_vals[x])

        tmp = {}
        tmp['time'] = prev['time']
        tmp['mac'] = prev['mac']
        tmp['sensors'] = [{'id':x.id, 'type':x.type, 'value':prev['sensors'][x]} for x in controller.ports]
        yield tmp

ports = []
ports.append(Port(1, 4, 10, 20))
ports.append(Port(2, 9, 5, 31))
ports.append(Port(3, 10, 7, 89))
ports.append(Port(4, 7, 30, 100))

contr = Controller(ports, '262g34hg45y4')

# for x in create_norm_params(contr):
#     tmp = json.dumps(x, indent=2, sort_keys=True)
#     print(tmp)
#     time.sleep(1)







