import postgresql
import numpy as np
import random as rd
import alex.create_dataset as cr_data
import time
db = postgresql.open('pq://postgres:@10.0.1.99:5432/hackathondb')

def get_data(mac):
    nf = db.query("SELECT COUNT(*) FROM (SELECT DISTINCT id_port FROM log WHERE mac = '" + mac + "') as f")[0][0]
    s = db.query("SELECT * FROM log WHERE mac = '" + mac + "' ORDER BY time desc LIMIT " + str(nf * 50))
    s = list(map(lambda x: [x[1], x[3], x[4], x[6]], s))
    s.sort(key=lambda x: (x[2], x[0]))
    s = [x[3] for x in s]
    s = np.array(s)
    s = s.reshape(s.shape[0] // nf, nf)
    id_sens = db.query("SELECT DISTINCT id_port FROM log WHERE mac = '" + mac + "' ORDER BY 1")
    id_sens = list(map(lambda x: x[0], id_sens))
    min_max = []
    for x in id_sens:
        kek = db.query(f"SELECT min_value, max_value FROM ports WHERE mac = '{mac}' AND id_port = '{x}' ")
        min_max.append(kek[0])

    return s, min_max

def predict(data, min_max):
    prob = 0
    for x in range(data.shape[1]):
        feat_data = data[:, x]
        mean = feat_data.mean()
        c = (min_max[x][1] + min_max[x][0]) // 2
        prob1 = int((mean - c) / (min_max[x][1] - c) * 100)
        prob2 = int((c - mean) / (c - min_max[x][0]) * 100)
        prob = max(prob, max(prob1, prob2))
        if prob == 70:
            print(feat_data, min_max[x])
            exit(0)
    return prob


def set_contr(mac):
    res = predict(*get_data(mac))
    db.query(f"UPDATE controllers SET probability = {res} WHERE mac = '{mac}'")
    return


def get_prob(mac):
    prob = db.query(f"SELECT probability FROM controllers WHERE mac = '{mac}'")
    return prob[0][0]

def set_prob(mac, val):
    db.query(f"UPDATE controllers SET probability = {val} WHERE mac = '{mac}'")
    return


# mac = '00:26:57:00:1f:02'
# set_contr(mac)


if __name__ == '__main__':
    controllers = cr_data.contrs
    macs = [x.mac for x in controllers]
    bad_macs = [x.mac for x in controllers if any(map(lambda y: y.badness != 0, x.ports))]
    good_macs = [x for x in macs if x not in bad_macs]
    while True:
        for x in macs:
            # if x in good_macs:
            #     cur_prob = get_prob(x)
            #     delt = rd.choice([-2, -1, 1, 2])
            #     new_prob = cur_prob + delt
            #     if new_prob <= 0 or new_prob >= 100:
            #         new_prob = cur_prob - delt
            #     set_prob(x, new_prob)
            # else:
            #     set_contr(x)
            set_contr(x)
        time.sleep(1)







