import requests
import pandas as pd
import json
import datetime

def power(x, y):
    if y == 0:
        return 1
    t = power(x, y // 2)
    if y % 2 == 0:
        return t * t
    else:
        return x * t * t
        
def processing_data(address, page, offset,apiKey,exchange_name) :
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&page={page}&offset={offset}&startblock=0&endblock=27025780&sort=desc&apikey={apiKey}"
    response = requests.request("GET", url)
    data = response.json()
    results = data["result"]
    final_list = []
    for result in results:
        dict = result
        token_Decimal = result["tokenDecimal"]
        token_time = datetime.datetime.fromtimestamp(int(result["timeStamp"]))
        token_From = result["from"]
        token_To = result["to"]
        token_Value = int(result["value"])/power(10,int(token_Decimal))
        dict["value_out"] = 0
        dict["value_in"] = 0
        if token_From.lower() == address.lower():
            dict["value_out"] = int(token_Value)
        else:
            if token_To.lower() == address.lower():
                dict["value_in"] = int(token_Value)
        dict["year"] = token_time.year
        dict["month"] = token_time.month
        dict["day"] = token_time.day
        dict["hour"] = token_time.hour
        dict["minute"] = token_time.minute
        dict["exchange_name"] = exchange_name
        final_list.append(dict)
    return final_list

if __name__ == "__main__":
    list = []
    apiKey = "PSI4IFEFAUF8USVB6M5BSEAM1VB9CX7FJZ"
    page = 1
    offset = 10000
    data = pd.read_csv('input1.csv')
    # test_address = data['address'].values
    # test_name = data['exchange name'].values
    for index, row in data.iterrows():
        address = row['address']
        exchange_name = row['exchange name']
        list.extend(processing_data(address, page, offset,apiKey,exchange_name))
    # address = test_address[0]
    # address = "0xf16E9B0D03470827A95CDfd0Cb8a8A3b46969B91"
    # for id in address:
    # list.extend(processing_data(address, page, offset,apiKey,exchange_name))
    now = datetime.datetime.now()
    date = now.date()
    df = pd.DataFrame(list)
    df.to_csv(f'{date}.csv', index=False)
    # df.to_csv('ouput1.csv', index= False)