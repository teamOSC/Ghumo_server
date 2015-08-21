from flask import Flask, request, render_template, url_for, redirect
import json
from app import app
from travel import *


@app.route('/testing')
def testing():
    return "API Working!"


@app.route('/api/travel/cabs', methods=['GET', 'GET'])
def travel_api():
    result = []

    ''' ========================Example JSON to be sent===============
    result = [
            {
                'provider': 'provider_name',
                'time_of_arrival': 'time in minutes',
                'price_per_km': 'price in INR/Km',
                'display_name': 'Black/X/GO',
                'min_price': 'minimum_price',
            },
        ]
    =============================================================='''

    try:
        list_of_result = uber_api(request.args.get('lat'), request.args.get('lng'))
        for res in list_of_result:
            result.append(copy.deepcopy(res))
    except:
        pass

    try:
        list_of_result = taxi_for_sure_api(request.args.get('lat'), request.args.get('lng'))
        for res in list_of_result:
            result.append(copy.deepcopy(res))
    except:
        pass

    final_result = sorted(result, key=lambda k: k['time_of_arrival'])

    return json.dumps(final_result)
