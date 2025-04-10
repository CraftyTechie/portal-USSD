import aiohttp
import asyncio
import requests
import base64
import traceback
from django.conf import settings

def generate_access_token():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    print("consumer key", consumer_key)
    print("consumer secret", consumer_secret)

    try:
        encoded_credentials = base64.b64encode(
            f"{consumer_key}:{consumer_secret}".encode()).decode()
        print("encoded credentials", encoded_credentials)
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url, headers=headers) as response:
        response = requests.get(url, headers=headers)
        print("RESPONSE: ", response)
        print("STATUS CODE: ", response.status_code)
        data = response.json()

        print("RESPONSE:")
        print(data)

        if "access_token" in data:
            return data["access_token"]
        else:
            raise Exception("Failed to get access token: " + data.get("error_description", "No error description provided"))
    except Exception as e:
        traceback.print_exc()
        raise Exception("Failed to get access token: " + str(e))

# Example usage:
# async def main():
#     try:
#         access_token = await generate_access_token()
#         print("Access token:", access_token)
#     except Exception as e:
#         print("Error:", e)

# asyncio.run(main())
