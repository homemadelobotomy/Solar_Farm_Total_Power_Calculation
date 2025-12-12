# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from concurrent import futures
import requests
import time

CALLBACK_URL = "http://localhost:8001/api/solarpanel-requests/"  # URL основного сервиса
executor = futures.ThreadPoolExecutor(max_workers=5)
SERVICE_TOKEN = "12345678" 

def calculate_total_power(panels, insolation):    
    time.sleep(5)  
    power = 0.0
    for panel in panels:
        power += panel['power'] * panel['area'] / ((panel['width'] * panel['height']) / 1000000)
    
    v = power * insolation / 1000
    total = round(v, 2)
    
    return total

def result_callback(task, request_id):
    try:
        result = task.result()

        payload = {'total_power':result,
                   'token': SERVICE_TOKEN}
        headers = {'X-Service-Token':SERVICE_TOKEN}

        response = requests.put(CALLBACK_URL + str(request_id) + '/update-calculation',
                                json=payload, headers=headers, timeout=5)
    except futures._base.CancelledError:
        return
    

@api_view(['POST'])
def calculate_power_async(request):
 
    panels = request.data.get('panels', [])
    insolation = request.data.get('insolation', 0)
    request_id = request.data.get('request_id', 0)
    
    if not panels or not insolation:
        return Response(
            {'error': 'панели и инсоляция обязательны'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    task = executor.submit(calculate_total_power, panels, insolation)
    task.add_done_callback(lambda t: result_callback(t, request_id))
    
    return Response(
        {'message': 'Расчет мощности начался'},
        status=status.HTTP_200_OK
    )
