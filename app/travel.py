import copy

import requests, json

from credentials import uber_credentials


def uber_api(latitude, longitude):
    url = 'https://api.uber.com/v1/estimates/time'

    parameters = {
        'server_token': uber_credentials['server_token'],
        'start_latitude': latitude,
        'start_longitude': longitude,
    }

    response_from_uber = requests.get(url, params=parameters)
    dataTime = response_from_uber.json()
    # print dataTime

    parameters = {
        'server_token': uber_credentials['server_token'],
        'latitude': latitude,
        'longitude': longitude,
    }

    url = 'https://api.uber.com/v1/products'
    response_from_uber = requests.get(url, params=parameters)
    data = response_from_uber.json()

    result = {
        'result': []
    }

    cab_provider = 'Uber'
    filler_dictionary = {}

    for x_data in dataTime['times']:

        filler_dictionary['provider'] = cab_provider
        filler_dictionary['time_of_arrival'] = int(int(x_data['estimate']) / 60)
        filler_dictionary['display_name'] = x_data['display_name']

        for y_data in data['products']:
            if y_data['display_name'] == x_data['display_name']:
                filler_dictionary['price_per_km'] = y_data['price_details']['cost_per_distance']
                filler_dictionary['min_price'] = y_data['price_details']['minimum']
                try:
                    filler_dictionary['product_id'] = y_data['product_id']
                except:
                    filler_dictionary['product_id'] = ''

        result['result'].append(copy.deepcopy(filler_dictionary))

    return result['result']


def taxi_for_sure_api(latitude, longitude):
    url = 'http://iospush.taxiforsure.com/getNearestDriversForApp/?density=320&appVersion=4.1.1&longitude=' \
          + str(longitude) + '&latitude=' + str(latitude)

    final_list = []
    filler_dict = {}

    data = requests.get(url)
    output = data.json()['response_data']['data']

    for res in output:
        filler_dict['provider'] = 'TaxiForSure'
        filler_dict['time_of_arrival'] = int(res['duration'])
        filler_dict['price_per_km'] = '16'
        filler_dict['display_name'] = res['carType']
        filler_dict['min_price'] = '50'
        try:
            filler_dict['product_id'] = res['product_id']
        except:
            filler_dict['product_id'] = ''

        final_list.append(copy.deepcopy(filler_dict))

    return final_list


def cabs_guru(lat, lng):
    url = "http://api.cabsguru.com/services/v2/caboption/p2p"

    headers = {'content-type': 'application/json'}
    pay = {
        "pickupTime": 1440186730057,
        "pickupNow": True,
        "mobileNo": "",
        "pickupLocation": {
            "latitude": str(lat),
            "longitude": str(lng),
            #"label": "Shyam Nagar, Okhla Industrial Area, New Delhi"
        },
        "dropoffLocation": {
            "latitude": "28.564193094506155",
            "longitude": "77.25882723927498",
            #"label": "Block G,  Sri Niwaspuri"
        },
        "distanceMatrix": {
            "distance": 3961,
            "distanceText": "4.0 km",
            "duration": 1023,
            "durationText": "17 mins"
        },
        "uniqueId": "",
        "deviceId": "358091058388825",
        "deviceType": "Android",
        "appversion": "27"
    }

    data = requests.post(url, data=json.dumps(pay), headers=headers)

    return json.dumps(data.json()['data']['searchcabresponse']['cabOperator'])


if __name__ == '__main__':
    print cabs_guru(28.5444571, 77.2721861)
