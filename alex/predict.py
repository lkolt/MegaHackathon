import postgresql
import numpy as np
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

mac = '00:26:57:00:1f:02'
set_contr(mac)






