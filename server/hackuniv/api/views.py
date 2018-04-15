from .constants import dot_number
from random import randint
from collections import defaultdict
from datetime import datetime
import json
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Max


def checkMac(request, mac):
    json_resp = {}
    try:
        cntr = Controllers.objects.get(mac=mac)
        ports = Ports.objects.filter(mac=mac)

        if any(port.max_value is None or port.min_value is None or port.description is None
               for port in ports
               ):
            json_resp['status'] = "ok"
            json_resp['message'] = []
            for port in Ports.objects.filter(mac=mac):
                try:
                    descr = PortDesc.objects.get(type=port.type)
                except:
                    continue
                cur_dict = {}
                json_resp['message'].append(cur_dict)
                cur_dict['id'] = port.id_port
                cur_dict['type'] = descr.name
                cur_dict['description'] = port.description
                cur_dict['min_value'] = port.min_value
                cur_dict['max_value'] = port.max_value
                cur_dict['measurement'] = descr.measurement
        else:
            json_resp['status'] = 'error'
            json_resp['message'] = ""
    except Controllers.DoesNotExist:
        json_resp['status'] = 'error'
        json_resp['message'] = ""

    resp = JsonResponse(json_resp)
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


@csrf_exempt
def setPorts(request):
    def verify_json(json_data):
        keys_fst = [
            'mac',
            'description',
            'ports'
        ]
        keys_snd = [
            'max_value',
            'min_value',
            'type',
            'description',
            'measurement',
            'id'
        ]
        return all(k in json_data for k in keys_fst) and all(k in d for d in json_data['ports'] for k in keys_snd)
    json_res = {}
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        if verify_json(json_data):
            mac = json_data['mac']
            description = json_data['description']
            try:
                cntr = Controllers.objects.get(mac=mac)
                setattr(cntr, 'description', description)
                setattr(cntr, 'description', description)
                setattr(cntr, 'description', description)
                setattr(cntr, 'description', description)
                setattr(cntr, 'description', description)
            except:
                cntr = Controllers(mac=mac, description=description)
                cntr.save()
                cntr.save()
                cntr.save()
                cntr.save()
                cntr.save()
            for port in json_data['ports']:
                min_val = port['min_value']
                max_val = port['max_value']
                measurement = port['measurement']
                descr = port['description']
                name = port['type']
                id_port = port['id']
                try:
                    type_id = PortDesc.objects.get(name=name, measurement=measurement).type
                except:
                    json_res = {"status": "error", "message": "cannot find {}{} pair".format(name, measurement)}
                    break
                if min_val > max_val:
                    json_res = {"status": "error", "message": "max value must be greater or equal then min value"}
                    break
                new_port = Ports(mac=mac, type=type_id, description=descr,
                                 min_value=min_val, max_value=max_val, id_port=id_port)
                new_port.save()
        else:
            json_res = {"status": "error", "message": "invalid json (some fields are missing"}
    if "status" not in json_res:
        json_res = {"status": "ok", "message": ""}
    resp = JsonResponse(json_res)
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


def getControllers(request, user_id):

    controllers = Controllers.objects.filter(user_id=user_id)
    macs = [contr.mac for contr in controllers]
    mac2controller = dict((controller.mac, controller) for controller in controllers)
    ports = Ports.objects.filter(mac__in=macs)
    port_types = [port.type for port in ports]
    all_port_descriptions = PortDesc.objects.filter(type__in=port_types)
    res_dict = {'controllers': [], 'notifications': []}

    for mac in macs:
        cur_dict = {}
        cur_controller = mac2controller[mac]
        res_dict['controllers'].append(cur_dict)
        cur_dict['mac'] = mac
        cur_dict['description'] = cur_controller.description
        cur_dict['probability'] = int(cur_controller.probability) if cur_controller.probability is not None else None

        if cur_dict['probability'] is not None:
            if cur_dict['probability'] <= 35:
                color = 'text-info'
            elif cur_dict['probability'] <= 70:
                color = 'text-warning'
            else:
                color = 'text-danger'

            cur_dict['color'] = color
        else:
            cur_dict['color'] = 'text-info'

        cur_dict['ports'] = []
        port_gen = filter(lambda x: x.mac == mac, ports)
        flag = False
        for port in port_gen:
            port_desc = next(desc for desc in all_port_descriptions if desc.type == port.type)
            log = Log.objects.filter(id_port=port.id_port, mac=mac).aggregate(Max('time'))
            max_time = log['time__max']
            if max_time is not None:
                log = Log.objects.get(time=max_time, id_port=port.id_port, mac=mac)
            else:
                continue
            port_dict = {}
            if not flag:
                cur_dict['current_port'] = port_dict
            cur_dict['ports'].append(port_dict)
            port_dict['value'] = log.value
            port_dict['type'] = port_desc.name
            port_dict['description'] = port.description
            port_dict['min_value'] = port.min_value
            port_dict['max_value'] = port.max_value
            port_dict['measure'] = port_desc.measurement
            port_dict['icon'] = port_desc.icon
            if log.value is not None and port.min_value is not None and port.max_value is not None:
                port_dict['alert'] = False if port.min_value <= log.value <= port.max_value else True
            else:
                port_dict['alert'] = False

            port_dict['options'] = {
                "seriesBarDistance": 10,
                "axisX": {
                  "showGrid": False
                },
                "height": '245px'
              }

            logs = Log.objects.filter(id_port=port.id_port, mac=mac)
            port_dict['data'] = {
                "labels": [],
                "series": [
                    [x.value for x in sorted(logs, key=lambda x: x.time)[-dot_number:]]
                ]
            }

            port_dict['isActive'] = not flag
            flag = True

    for controller in res_dict['controllers']:
        cur_dict = {}
        res_dict['notifications'].append(cur_dict)
        cur_dict['mac'] = controller['mac']
        cur_dict['color'] = controller['color']
        cur_dict['description'] = controller['description']

    resp = JsonResponse(res_dict)
    resp['Access-Control-Allow-Origin'] = "*"
    return resp


def getLogs(request):
    res_dict = defaultdict(lambda: defaultdict(dict))
    for log in Log.objects.all():
        mac = log.mac
        id_port = log.id_port
        time = log.time
        val = log.value
        res_dict[mac][id_port][time] = val
    a = {
        '11:f6:02:a8:02:12': {
            2: [32, 22, 23, 22, 26, 28],
            3: [11, 12, 11, 12, 11, 13]
        }
    }
    resp = JsonResponse(a)
    resp['Access-Control-Allow-Origin'] = "*"
    return resp

def insertTest(request):
    qq = Users(login="bad_motherfucker", pass_field='1488')
    qq.save()
    return HttpResponse('success')

@csrf_exempt
def insertControllers(request):
    rows = json.loads(request.body.decode('utf-8'))
    norm_time = datetime.fromtimestamp(rows['time']).strftime('%Y-%m-%d %H:%M:%S')
    mac = rows['mac']
    for triple in rows['sensors']:
        value, type, port_id = triple['value'], triple['type'], triple['id']
        try:
            port = Ports.objects.get(id_port=port_id,  mac=mac)
            status = 0
            if port.min_value is not None and port.max_value is not None:
                if port.min_value <= value <= port.max_value:
                    status = 0
                else:
                    status = 1
            temp_row = Log(id_port=port_id, mac=mac, type=type, time=rows['time'], time_string=norm_time,
                           value=value, status=status)
            temp_row.save()
        except Ports.DoesNotExist:
            new_port = Ports.objects.create(id_port=port_id, mac=mac, type=type)
            if Controllers.objects.filter(mac=mac).count() == 0:
                new_contr = Controllers.objects.create(mac=mac)
                new_contr.save()
    return HttpResponse(status=200)
