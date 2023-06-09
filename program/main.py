from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from func_messaging import send_message


# MAIN FUNCTION
if __name__ == "__main__":

  # note TestNet data maybe weired and not the same as MainNet.  You need to create another Client for MainNet if you want to get Production data

  # Message on start
  send_message("Bot launch successful")

  # Connect to client
  try:
    print("Connecting to Client...")
    client = connect_dydx()
  except Exception as e:
    print("Error connecting to client: ", e)
    send_message(f"Failed to connect to client {e}")
    exit(1)




  # Abort all open positions
  if ABORT_ALL_POSITIONS:
    try:
      print("Closing all positions...")
      close_orders = abort_all_positions(client)
    except Exception as e:
      print("Error closing all positions: ", e)
      send_message(f"Error closing all positions {e}")
      exit(1)

  # Find Cointegrated Pairs
  if FIND_COINTEGRATED:

    # Construct Market Prices - it stores all tradable markets into a dataframe
    try:
      print("Fetching market prices, please allow 3 mins...")
      df_market_prices = construct_market_prices(client)
      # print(df_market_prices) # delete me - just to see how the dataframe looks like
    except Exception as e:
      print("Error constructing market prices: ", e)
      send_message(f"Error constructing market prices {e}")
      exit(1)

    # Store Cointegrated Pairs - it takes all the tradable markets in dataframe, loop through all and come up with tradable pairs, and store all these pairs into a .csv file
    try:
      print("Storing cointegrated pairs...")
      stores_result = store_cointegration_results(df_market_prices)
      if stores_result != "saved":
        print("Error saving cointegrated pairs")
        exit(1)
    except Exception as e:
      print("Error saving cointegrated pairs: ", e)
      send_message(f"Error saving cointegrated pairs {e}")
      exit(1)

  # Run as always on
  while True:

    # Place trades for opening positions
    if MANAGE_EXITS:
      try:
        print("Managing exits...")
        manage_trade_exits(client)
      except Exception as e:
        print("Error managing exiting positions: ", e)
        send_message(f"Error managing exiting positions {e}")
        exit(1)

    # Place trades for opening positions
    if PLACE_TRADES:
      try:
        print("Finding trading opportunities...")
        open_positions(client)
      except Exception as e:
        print("Error trading pairs: ", e)
        send_message(f"Error opening trades {e}")
        exit(1)
