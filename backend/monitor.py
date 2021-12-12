import requests
import json
from flask import Flask, request
from pycoingecko import CoinGeckoAPI
import time
from plyer import notification
import pymongo
import logging
import threading
import time
import os
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler


load_dotenv()

# See bottom of file for how to use and try out on its own

class Monitor:

  def __init__(self, debug=False):
    self.debug = debug
    m_creds = os.getenv("MONGO_CREDS")
    # https://cloud.mongodb.com/v2/599107153b34b97bd19035e5#serverless/explorer/DataWatch/DataWatch/cryptos/find
    self.myclient = pymongo.MongoClient("mongodb+srv://"+m_creds+"@datawatch.7je0a.mongodb.net/DataWatch?retryWrites=true&w=majority")
    self.mydb = self.myclient["DataWatch"]
    self.cryptos_monitor_rules_col = self.mydb["cryptos_monitor_rules"]
    self.cryptos_history_col = self.mydb["cryptos_history"]
    self.x = threading.Thread(target=self.run)
    self.x.start()
    
  constructor = __init__

  def add(self, crypto_name, monitor_interval_secs, change_percentage_range, change_type):
    # Ideally, the user will be prompted to set an interval with a minimum of 60 seconds, so monitor_interval_secs < 60 should always be false
    local_monitor_interval_secs = monitor_interval_secs
    if(monitor_interval_secs < 60):
      self.error_alert("Monitor interval must be at least 60 seconds, setting to 60 seconds for "+crypto_name)
      local_monitor_interval_secs = 60
  
    latest_price = int(self.get_starting_price(crypto_name)) # float?
    if latest_price == -1:
      self.error_alert("Could not get starting price for "+crypto_name)
      return

    self.cryptos_monitor_rules_col.find_one_and_delete({  "crypto_name": crypto_name,
                                                          "monitor_interval_secs": local_monitor_interval_secs,
                                                          "change_percentage_range": float(change_percentage_range),
                                                          "change_type": change_type.lower()
                                                        })
    self.cryptos_monitor_rules_col.insert_one({ "crypto_name": crypto_name,
                                                "monitor_interval_secs": local_monitor_interval_secs,
                                                "change_percentage_range": float(change_percentage_range),
                                                "change_type": change_type.lower(),
                                                "previous_price": 0,
                                                "latest_price": latest_price,
                                                "last_checked": time.time()
                                              })

  #-----------------------------------------------------
  # Thread
  #-----------------------------------------------------
  def run(self):
    while True:
      for crypto in self.cryptos_monitor_rules_col.find():
        cur_time = time.time()
        if (cur_time - int(crypto["last_checked"])) >= (int(crypto["monitor_interval_secs"])):
          self.update(crypto, cur_time)
      time.sleep(15)

  #-----------------------------------------------------
  def get_starting_price(self, crypto_name="bitcoin"): #remove default TODO
    starting_price = self.get_crypto_price_cg(crypto_name)
    return starting_price

  #-----------------------------------------------------
  def update(self, crypto, update_time):
    # Get the current price
    current_price = int(self.get_crypto_price_cg(crypto["crypto_name"]))
    # Check if the price has changed
    if current_price > crypto["latest_price"]:
      percentage_change = 1 - (crypto["latest_price"] / current_price)
      # Check if the price has gone up
      if crypto["change_type"] == "up" or crypto["change_type"] == "both":
        # Check if the price has gone up by a certain amount
        if percentage_change > crypto["change_percentage_range"]:
          # Send an alert
          self.alert_user("Price of "+crypto["crypto_name"]+" went up by "+str(percentage_change)+"%")
          
          self.cryptos_history_col.insert_one({ "crypto_name": crypto["crypto_name"],
                                                "change": "up",
                                                "previous_price": crypto["latest_price"],
                                                "current_price": current_price,
                                                "change_percentage": percentage_change,
                                                "time": time.time(),
                                                "monitor_rule_id": crypto["_id"]
                                              })
    elif current_price < crypto["latest_price"]:
      # Check if the price has gone down
      percentage_change = 1 - (current_price / crypto["latest_price"])
      if crypto["change_type"] == "down" or crypto["change_type"] == "both":
        # Check if the price has gone down by a certain amount
        if percentage_change  > crypto["change_percentage_range"]:
          # Send an alert
          self.alert_user("Price of "+crypto["crypto_name"]+" went down by "+str(percentage_change)+"%")
          
          self.cryptos_history_col.insert_one({ "crypto_name": crypto["crypto_name"],
                                                "change": "down",
                                                "previous_price": crypto["latest_price"],
                                                "current_price": current_price,
                                                "change_percentage": percentage_change,
                                                "time": time.time(),
                                                "monitor_rule_id": crypto["_id"]
                                              })

    self.cryptos_monitor_rules_col.update_one({ "crypto_name": crypto["crypto_name"],
                                                "monitor_interval_secs": crypto["monitor_interval_secs"],
                                                "change_percentage_range": crypto["change_percentage_range"],
                                                "change_type": crypto["change_type"]},
                                                { "$set": { "latest_price": current_price,
                                                            "previous_price": crypto["latest_price"],
                                                            "last_checked": update_time
                                                          }
                                              })


  #-----------------------------------------------------
  def error_alert(self, message):
    if self.debug:
      print(message)

  #-----------------------------------------------------
  def alert_user(self, message):
    # The title parameter should be used to specify a title for the notification
    # The app_name parameter is currently set to Python no matter what
    # The app_icon parameter can be used to specify an icon (must be a .ICO file on Windows)
    #notification.notify(app_name='Data Watch', message=message)
    print(message)

  #-----------------------------------------------------
  def get_crypto_price_cg(self,cryptos="bitcoin",currency="usd"):
    from pycoingecko import CoinGeckoAPI
    cg = CoinGeckoAPI()
    json_data = cg.get_price(ids=cryptos.lower(), vs_currencies=currency.lower())
    try:
      return json_data[cryptos.lower()][currency.lower()]
    except Exception:
      self.error_alert("Invalid crypto: "+cryptos+" or currency: "+currency)
      return -1

app   = Flask(__name__)
store = {}

@app.route('/')
def index():
  return 'Index', 200

@app.route('/set', methods = ['POST'])
def set():
  for key, value in request.args.items():
    store[key] = value
  return f'{json.dumps(store, indent = 2)}\n', 200

@app.route('/get', methods = ['GET'])
def get():
  key = request.args.get('key', default=None, type=str)
  if key and key in store:
    return f'{key} = {store[key]}\n'
  return 'Key not found.\n', 404

@app.route('/remove', methods = ['DELETE'])
def remove():
  key = request.args.get('key', default=None, type=str)
  if key and key in store:
    del store[key]
    return f'{json.dumps(store, indent = 2)}\n', 200
  return 'Key not found.\n', 404
    
# Main
if __name__ == "__main__":
  theMon = Monitor(True)
  theMon.add("bitcoin", 60, 0.001, "both")
  theMon.add("bitcoin", 300, 0.01, "both")
  theMon.add("bitcoin", 3600, 0.1, "both")
  theMon.add("ethereum", 60, 0.001, "both")
  theMon.add("ethereum", 300, 0.01, "both")
  theMon.add("ethereum", 3600, 0.1, "both")
# Monitors bitcoin price every 5 minutes and alerts if it goes down by more than .01%, debug is True
  app.run(host='0.0.0.0', port=8000)



