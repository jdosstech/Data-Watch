import json
import requests 
import time

def get_crypto_price(coin):
    #Get the URL
    url = 'https://api.coinbase.com/v2/prices/' + coin.upper() + '-USD/spot'

    #Make a request to the website
    JSON = requests.get(url)

    #Parse the JSON
    data = json.loads(JSON.text)

    #Find the current price 
    text = []
    text.append(data['data']['amount'])
    text.append(data['data']['currency'])

    #Return the price 
    return ' '.join(text)

cryptocurrency = input('cryptocurrency: ')

'''
suggested intervals:
    - bitcoin: 55 seconds
    - ethereum: 63 seconds?
'''
interval = input('interval (seconds): ')
while True:
    print(get_crypto_price(cryptocurrency))
    time.sleep(int(interval.strip()))
