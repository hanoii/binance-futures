import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    binance = {'api_key':os.getenv('BINANCE_API_KEY'), 'secret_key': os.getenv('BINANCE_API_SECRET')}
    if os.getenv('BINANCE_TESTNET') == 'true':
        binance['url'] = 'https://testnet.binancefuture.com'
    request_client = RequestClient(**binance)
    result = request_client.get_account_information_v2()
    context = {'binance': result}
    return render(request, "index.html", context)


@require_http_methods(["POST"])
def stop(request):
    try:
        mydata = json.loads(request.body.decode("utf-8"))
        return JsonResponse(mydata)
    except:
        return JsonResponse({'success': 'false', 'error': 'Invalid payload.'})

