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
    return s

def predict(data):
    print(data)


mac = '00:26:57:00:1f:02'
predict(get_data(mac))





