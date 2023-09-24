# Import the requests library to make HTTP requests to the API
import requests

# Define the API key to authenticate with the exchange rate API for currency conversion
API_KEY = "xxxxxxxxxxxxxxxxxxxxxx"

# Define the URL of the API endpoint for fetching currency symbols
SYMBOLS_URL = 'https://api.exchangerate.host/symbols'


# Define a function to find matching currencies based on user input
def find_matching_currencies(currency):
    # Initialize an empty list to store the matching currencies
    matching_currencies = []
    
    # Send a GET request to the symbols API and store the response in a variable
    response = requests.get(SYMBOLS_URL)
    
    # Check if the API request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the JSON response into a Python dictionary
        data = response.json()
        
        # Check if the 'success' field in the response is True
        if data.get('success', False):
            # Retrieve the 'symbols' dictionary from the response
            symbols = data.get('symbols', {})
            
            # Iterate over each symbol in the 'symbols' dictionary
            for symbol, details in symbols.items():
                # Convert the description to lowercase and check if the user input is contained in it
                description = details.get('description', '').lower()
                if currency.lower() in description:
                    # If a match is found, append a tuple with description and symbol to the list of matching currencies
                    matching_currencies.append((description, symbol))
                    
    # Return the list of matching currencies
    return matching_currencies


# Define a function to get the exchange rate between USD and the target currency
def get_exchange_rate(base_currency, target_currency):
    # Construct the URL for the exchange rate API
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    
    # Send a GET request to the API and store the response in a variable
    response = requests.get(url)
    
    # Parse the JSON response into a Python dictionary
    data = response.json()
    
    # Retrieve the exchange rate for the target currency from the 'conversion_rates' field in the response
    return data.get('conversion_rates', {}).get(target_currency)


# Define the main function to execute the program
def main():
    print("----- Currency Symbol Finder -----")
    # Take a part of currency name as input from the user
    currency_part = input('Please Enter a part of Your Currency Name to find its Symbol: ')
    
    # Call the find_matching_currencies function and store the result in a variable
    matching_currencies = find_matching_currencies(currency_part)

    print("Search Results:")
    # Print each matching currency on a new line
    for currency in matching_currencies:
        print(f"{currency[0]} ({currency[1]})")

    print("----- Currency Converter -----")
    # Ask the user to enter the desired currency symbol based on the search results
    target_currency = input("Now, Please check the search result and get your desired symbol to find your currency rate with respect to USD: ").upper()
    
    # Call the get_exchange_rate function and store the result in a variable
    exchange_rate = get_exchange_rate("USD", target_currency)

    # Check if an exchange rate was found and print the result, or print an error message if not found
    if exchange_rate:
        print(f"One USD = {exchange_rate} {target_currency}")
    else:
        print("Currency not found or error occurred.")

    
    print("Thanks For Using the Program!")


# Check if the script is run directly and not imported as a module, and if so, call the main function
if __name__ == "__main__":
    main()
