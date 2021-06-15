import os
import sys
import json
import traceback
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

def binance_request_client():
    binance = {'api_key':os.environ['BINANCE_API_KEY'], 'secret_key': os.environ['BINANCE_API_SECRET']}
    if os.getenv('BINANCE_TESTNET') == 'true':
        binance['url'] = 'https://testnet.binancefuture.com'
    request_client = RequestClient(**binance)
    return request_client


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    request_client = binance_request_client()
    result = request_client.get_account_information_v2()
    positions = []
    for position in result.positions:
        if position.entryPrice:
            row = {}
            row['symbol'] = position.symbol
            row['entryPrice'] = position.entryPrice
            row['unrealizedProfit'] = position.unrealizedProfit
            #price = request_client.get_mark_price(position.symbol)
            #row['markPrice'] = price.markPrice
            positions.append(row)

    context = {'positions': positions}
    return render(request, "index.html", context)


@require_http_methods(["POST"])
def stop(request):
    response = {}
    try:
        quantity = 0
        payload = json.loads(request.body.decode("utf-8"))

        if not 'symbol' in payload:
            raise ValueError("symbol not in payload.")

        if not 'operation' in payload:
            raise ValueError("operation not in payload.")

        if payload['operation'] not in ['sell', 'buy']:
            raise ValueError("operation must be either 'buy' or 'sell'.")


        response['payload'] = payload
        request_client = binance_request_client()

        result = request_client.get_exchange_information()
        found = False
        for symbol in result.symbols:
            if symbol.symbol == payload['symbol']:
                found = True
                precision = symbol.quantityPrecision

        if not found:
            raise ValueError("Symbol " + payload['symbol'] + " not found.")

        if not 'quantity' in payload:
            result = request_client.get_position_v2()
            for position in result:
                if position.symbol == payload['symbol']:
                    quantity = position.positionAmt
                    response['quantity'] = quantity
        else:
            quantity = payload['quantity']
            response['quantity'] = quantity

        if quantity > 0:
            quantity = ("{:." + str(precision) + "f}").format(quantity)
            order = {
                'symbol': payload['symbol'],
                'ordertype': OrderType.MARKET,
                'quantity': quantity,
                'side': OrderSide.SELL
            }
            response['order'] = order
            result = request_client.post_order(**order)
        else:
            raise ValueError("quantity is 0.")
        return JsonResponse({'success': 'true', 'context': response})
    except:
        var = traceback.format_exc()
        return JsonResponse({'success': 'false', 'traceback': var.splitlines()})

