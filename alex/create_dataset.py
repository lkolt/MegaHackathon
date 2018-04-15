import time
import random
import json


class User:
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

class Port:
    def __init__(self, id, type, min_val, max_val, badness):
        self.id = id
        self.type = type
        self.min_val = min_val
        self.max_val = max_val
        self.badness = badness

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
    if port.badness == 0:
        delt = (port.max_val - port.min_val) // 7
        mean_val = (port.min_val + port.max_val) // 2
        return mean_val - delt, mean_val + delt
    elif port.badness == 1:
        mean_val = (port.min_val + port.max_val) // 2
        b = int(port.max_val * 1.3)
        return mean_val, b
    else:
        mean_val = (port.min_val + port.max_val) // 2
        a = int(port.min_val * 0.7)
        return a, mean_val

def create_norm_params(controller, time):
    dic = {'time' : time,
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
ports.append(Port(1, 4, 10, 20, 0))
ports.append(Port(2, 5, 5, 31, 0))
ports.append(Port(3, 1, 7, 89, 0))
ports.append(Port(4, 2, 30, 100, 0))
contr = Controller(ports, '00:26:57:00:1f:02')


ports2 = []
ports2.append(Port(1, 3, 10, 100, 1))
ports2.append(Port(5, 4, 5, 25, 0))
ports2.append(Port(6, 2, 23, 67, 0))
contr2 = Controller(ports2, '14:f6:02:a8:02:12')

ports3 = []
ports3.append(Port(2, 2, 40, 60, -1))
ports3.append(Port(3, 5, 15, 70, 1))
ports3.append(Port(6, 1, 35, 55, 1))
contr3 = Controller(ports3, '26:f1:09:d3:bb:9a')

ports4 = []
ports4.append(Port(1, 4, 30, 60, 0))
ports4.append(Port(2, 2, 300, 500, 0))
ports4.append(Port(5, 3, 70, 100, 0))
ports4.append(Port(9, 6, 60, 70, 0))
contr4 = Controller(ports4, '12:1d:1a:5b:4e:3c')

ports5 = []
ports5.append(Port(1, 2, 23, 80, 0))
ports5.append(Port(6, 3, 150, 250, 0))
ports5.append(Port(2, 3, 10, 40, 0))
ports5.append(Port(3, 6, 61, 79, 0))
contr5 = Controller(ports5, '16:82:e1:b1:5a:ff')

contrs = [contr, contr2, contr3, contr4, contr5]

# for x in create_norm_params(contr):
#     tmp = json.dumps(x, indent=2, sort_keys=True)
#     print(tmp)
#     time.sleep(1)







