import requests
from datetime import datetime
import os
import base64
import requests
from datetime import datetime
import json
from .models import MpesaIDs

PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
CONSUMER_KEY = "YiyUOpsGGem06AGgGTEGvjxjAB6AC9sBA9RqdQuqKTen6Lfa"
CONSUMER_SECRET = "nz9F3vO5uy8FpIiS4KxvGusu9ipqHDAH7hQGQ8PCHyWxeQ4nqL6mq4pBKpEoyFYa"
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
shortCode = "174379"
phone = "254740278095"
amount = "1"


def generate_access_token():

    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        encoded_credentials = base64.b64encode(
            f"{consumer_key}:{consumer_secret}".encode()
        ).decode()
        print("encoded credentials", encoded_credentials)
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }
        # Send the request and parse the response
        response = requests.get(url, headers=headers)
        print("STATUS CODE: ", response.status_code)
        print("text response= ", response.text)
        print("res errors ", response.content)
        print("json response= ", response.json())

        response = response.json()

        print("RESPONSE")
        if "access_token" in response.keys():
            return response["access_token"]
        else:
            print(response["error_description"])
    except Exception as e:
        print("status code", response.status_code)
        return response.status_code


def stk_push(phone, amount, student):
    accessToken = generate_access_token()
    if accessToken == 400:

        print("unable to handle the request at this moment. Try again later..")
        return "unable to handle your request at this moment.  Try again later.."
    print("ACCESS TOKEN", accessToken)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {accessToken}",
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": base64.b64encode(
            (shortCode + PASSKEY + timestamp).encode("utf-8")
        ).decode("utf-8"),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": 25474510778,
        "PartyB": 174379,
        "PhoneNumber": phone,
        "CallBackURL": "https://2gsvpcp1-8000.uks1.devtunnels.ms/mpesa/callback",
        "AccountReference": "MMUSTPORTAL",
        "TransactionDesc": "Paying of Fee",
    }

    response = requests.request(
        "POST",
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        headers=headers,
        json=payload,
    )
    # print(type(response.text))
    print("STATUS CODE ", response.status_code)
    data = response.json()
    print("safaricom json response ", response.json())
    if response.status_code == 200:
        print(data["CustomerMessage"])
        mID = data["MerchantRequestID"]
        cID = data["CheckoutRequestID"]
        newMpesaId = MpesaIDs.objects.create(
            merchantRequestID=mID, checkoutRequestID=cID, student=student
        )
        newMpesaId.save()
        return "Your request has been received you'll be promptEd for your MPESA PIN shortly.."

    else:
        print(data["errorMessage"])
        return "Cannot process your request at this time, Try again later.."


# stk_push(phone, amount)
