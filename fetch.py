import requests
from pycoingecko import CoinGeckoAPI
import time

# See bottom of file for how to use and try out on its own

class Monitor:

  def __init__(self, crypto_name, monitor_interval_secs, change_percentage_range, change_type, debug=False):
    self.debug = debug
    self.crypto_name = crypto_name
    self.monitor_interval_secs = monitor_interval_secs
    self.change_percentage_range = float(change_percentage_range)
    self.change_type = change_type.lower()
    self.last_price = int(self.get_starting_price()) # float?
    self.run()

  constructor = __init__

  #-----------------------------------------------------
  # Functions
  #-----------------------------------------------------

  #-----------------------------------------------------
  def get_starting_price(self):
    starting_price = self.get_crypto_price_cg(self.crypto_name)
    self.send_alert("Starting price: "+str(starting_price))
    return starting_price

  def run(self):
    while True:
      time.sleep(self.monitor_interval_secs)
      self.update()

  #-----------------------------------------------------
  def update(self):
    # Get the current price
    current_price = int(self.get_crypto_price_cg(self.crypto_name))
    self.send_alert("Current price: "+str(current_price))
    # Check if the price has changed
    if current_price > self.last_price:
      percentage_change = 1 - (self.last_price / current_price)
      # Check if the price has gone up
      if self.change_type == "up":
        # Check if the price has gone up by a certain amount
        if percentage_change > self.change_percentage_range:
          # Send an alert
          self.send_alert("Price went up by "+str(percentage_change)+"%")
    elif current_price < self.last_price:
      # Check if the price has gone down
      percentage_change = 1 - (current_price / self.last_price)
      if self.change_type == "down":
        # Check if the price has gone down by a certain amount
        if percentage_change  > self.change_percentage_range:
          # Send an alert
          self.send_alert("Price went down by "+str(percentage_change)+"%")
    # Update the last price
    self.last_price = current_price

  #-----------------------------------------------------
  def send_alert(self, message):
    if self.debug:
      print(message)

  #-----------------------------------------------------
  def get_crypto_price_cg(self,cryptos="bitcoin",currency="usd"):
    from pycoingecko import CoinGeckoAPI
    cg = CoinGeckoAPI()
    json_data = cg.get_price(ids=cryptos.lower(), vs_currencies=currency.lower())
    try:
      return json_data[cryptos.lower()][currency.lower()]
    except:
      self.send_alert("Invalid crypto: "+cryptos+" or currency: "+currency)


# Main
# Uncomment to run
# Monitor("bitcoin", 300, 0.01, "down", True)
# Monitors bitcoin price every 5 minutes and alerts if it goes down by more than .01%, debug is True
# Assign to a variable and destroy it when monitoring is no longer needed