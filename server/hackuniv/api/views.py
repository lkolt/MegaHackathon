from datetime import datetime
import json
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt


def getControllers(request, user_id):
    user = Users.objects.get(id=user_id)
    return HttpResponse(str(len(user)))


def insertTest(request):
    qq = Users(login="bad_motherfucker", pass_field='1488')
    qq.save()
    return HttpResponse('success')


@csrf_exempt
def insertControllers(request):
    rows = json.loads(request.body.decode('utf-8'))
    norm_time = datetime.fromtimestamp(rows['time']).strftime('%Y-%m-%d %H:%M:%S')
    for triple in rows['sensors']:
        value, type, id = triple['value'], triple['type'], triple['id']
        try:
            port = Ports.objects.get(id_port=id,  mac=rows['mac'])
            if port.min_value is not None and port.max_value is not None:
                if port.min_value <= value <= port.max_value:
                    status = 0
                else:
                    status = 1
                temp_row = Log(id_port=id, mac=rows['mac'], type=type, time=rows['time'], time_string=norm_time,
                               value=value, status=status)
                temp_row.save()
        except Ports.DoesNotExist:
            new_port = Ports(id_port=id, mac=rows['mac'], type=type)
            new_contr = Controllers(mac=rows['mac'])
            new_port.save()
            new_contr.save()
    return HttpResponse(status=200)
