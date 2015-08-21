from flask import Flask, request, render_template, url_for, redirect
import json
from app import app
from travel import *


@app.route('/testing')
def testing():
    return "API Working!"


@app.route('/api/cabs', methods=['GET'])
def travel_api():
    result = []

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


@app.route('/api/newcabs', methods=['GET'])
def new_cabs():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    try:
        return cabs_guru(lat, lng)
    except:
        return json.dumps([])
