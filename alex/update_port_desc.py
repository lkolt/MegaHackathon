import postgresql

# dic = {'Дж':'J',
#        'см':'cm',
#        'дм':'dm',
#        'м':'m',
#        'дБ':'dB',
#        'кг':'kg',
#        'г':'g',
#        'м/с':'m/s',
#        'см/с':'cm/s',
#        'рад':'rad',
#        'Гц':'Hz',
#        'Вт':'W',
#        'Па':'Pa'}

db = postgresql.open('pq://postgres:@10.0.1.99:5432/hackathondb')

macs = db.query(f"SELECT mac FROM controllers")
macs = [x[0] for x in macs]
macs = macs[1:]

for id, x in enumerate(macs):
    db.query(f"INSERT INTO controller_model VALUES ('{x}', {id} + 1)")