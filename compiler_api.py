import requests

def main(code):

    cid = "60e41708ceb7b9479453d3a906f5baef"
    csecret = "9221c3ca93e850c49b62a153c561e4fefedfe5b4137b56eabb6bdb1dac18966c"
    # Define the API endpoint URL
    url = 'https://api.jdoodle.com/v1/execute'
    # Prepare the payload data for the API request
    data = {
         "clientId" : cid,
         "clientSecret" : csecret,
         "script" : code,
         "language" : "python3",
         "versionIndex" : "0"
    }
    # Send a POST request to the API endpoint
    response = requests.post(url,json=data)
    # Parse the response JSON
    response_data = response.json()

    # Check if the request was successful
    if response.ok:
        # Print the output or error message
        # print("Output:")
        # print(response_data["output"])
        res = response_data["output"]

    elif response.status_code == 429:
        # Print the error message
        res = "Error: Daily limit of compiler use reached. Try again tomorrow."
    else:
        res = "Error: " + response_data["error"]
    
    return res

def check_usage():
    cid = "60e41708ceb7b9479453d3a906f5baef"
    csecret = "9221c3ca93e850c49b62a153c561e4fefedfe5b4137b56eabb6bdb1dac18966c"
    # Define the API endpoint URL
    url = 'https://api.jdoodle.com/v1/credit-spent'
    # Prepare the payload data for the API request
    data = {
         "clientId" : cid,
         "clientSecret" : csecret
    }
    # Send a POST request to the API endpoint
    response = requests.post(url,json=data)
    # Parse the response JSON
    response_data = response.json()

    if response.ok:
        res = "Credits used: " + str(response_data["used"])
        rem = "Credits remaining: " + str(200 - response_data["used"])
        return res + "\n" + rem
    else:
        res = "Error: " + response_data["error"]
        return res
#main()   
