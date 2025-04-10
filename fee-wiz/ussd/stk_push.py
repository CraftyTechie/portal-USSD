# import requests
# from datetime import datetime
# import traceback
# # from django.conf import settings
# import os
# import base64
# import requests
# import json


# # PASSKEY = os.environ.get('MPESA_PASSKEY')
# # CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
# # CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')   
# PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
# CONSUMER_KEY = "0vhJIhAU92k9nnVxCPNzcoF8oGbFHpcVkacYimXDffUCamRy"
# CONSUMER_SECRET = "s25vbvJFcAuTkGWzmMa8TyWouScb7AcZ52PCWo9cnoxorpMJPsKOmGLIoAIyXAZE"   
# # datetime.
# timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
# shortCode = "174379"
# # phone = "254114400824"
# # amount = "1"
from .models import Transaction

def create_transaction(phone, amount, reg_no):
    
    transaction = Transaction.objects.create(phone=phone, amount=amount, student_reg=reg_no)
    transaction.save()


# def generate_access_token():
#     consumer_key = CONSUMER_KEY
#     consumer_secret = CONSUMER_SECRET
#     url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
#     try:
#         encoded_credentials = base64.b64encode(
#             f"{consumer_key}:{consumer_secret}".encode()).decode()
#         print("encoded credentials",encoded_credentials)
#         headers = {
#             "Authorization": f"Basic {encoded_credentials}",
#             "Content-Type": "application/json"
#         }
#         # Send the request and parse the response
#         response = requests.get(url, headers=headers)
#         print("STATUS CODE: ",response.status_code)
#         print("response= ",response)

#         response = response.json()

#         # print("json response= ",response)

#         print("RESPONSE")
#         # name = json
#         # Check for errors and return the access token
#         if "access_token" in response.keys():
#             return response["access_token"]
#         else:
#             raise Exception("Failed to get access token: " +
#                             response["error_description"])
#     except Exception as e:
#         traceback.print_exc()
#         raise Exception("Failed to get access token: " + str(e))

# # +254 795 290373

# def stk_push(phone, amount, reg_no):
#     access_token = generate_access_token()
#     print(access_token)

#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {access_token}'
#     }
#     payload = {
#         "BusinessShortCode": 174379,
#         "Password": base64.b64encode((shortCode + PASSKEY + timestamp).encode('utf-8')).decode('utf-8'),
#         "Timestamp": timestamp,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": amount,
#         "PartyA": 25474510778,
#         "PartyB": 174379,
#         "PhoneNumber": phone,
#         "CallBackURL": "https://django-server-hazel.vercel.app/callback/",
#         "AccountReference": "FEEWIZ",
#         "TransactionDesc": "Payment of fEE"
#     }

#     response = requests.request(
#         "POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, json=payload)
#     print((response.text))
#     # print(json.loads(response.text)['ResponseCode'])
#     print()
#     if json.loads(response.text)['ResponseCode'] == "0":
#         print("success")
#         create_transaction(phone, amount, reg_no)
#         # pass

# # stk_push()

import requests
from datetime import datetime
import traceback
# from django.conf import settings
import os
import base64
import requests
from datetime import datetime
import json


# PASSKEY = os.environ.get('MPESA_PASSKEY')
# CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
# CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')   
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
CONSUMER_KEY = "0vhJIhAU92k9nnVxCPNzcoF8oGbFHpcVkacYimXDffUCamRy"
CONSUMER_SECRET = "s25vbvJFcAuTkGWzmMa8TyWouScb7AcZ52PCWo9cnoxorpMJPsKOmGLIoAIyXAZE"   
# datetime.
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
shortCode = "174379"
phone = "254740510778"
amount = "1"


def generate_access_token():
    print("hello")

    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        encoded_credentials = base64.b64encode(
            f"{consumer_key}:{consumer_secret}".encode()).decode()
        print("encoded credentials",encoded_credentials)
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
        # Send the request and parse the response
        response = requests.get(url, headers=headers)
        print("STATUS CODE: ",response.status_code)
        print("text response= ",response.text)
        print("res errors ",response.content)
        print("json response= ",response.json())

        response = response.json()

        # print("json response= ",response)

        print("RESPONSE")
        # name = json
        # Check for errors and return the access token
        if "access_token" in response.keys():
            return response["access_token"]
        else:
            print(response["error_description"])

            # raise Exception("Failed to get access token: " +
            #                 response["error_description"])
    except Exception as e:
        print("status code",response.status_code)
        return response.status_code
        pass
        # traceback.print_exc()
        # raise Exception("Failed to get access token: " + str(e))

# +254 795 290373

def stk_push(phone, amount, reg_no):
    accessToken = generate_access_token()
    if accessToken == 400:

        print("unable to handle the request at this moment. Try again later..")
        return "unable to handle your request at this moment.  Try again later.."
    print("ACCESS TOKEN",accessToken)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessToken}'
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": base64.b64encode((shortCode + PASSKEY + timestamp).encode('utf-8')).decode('utf-8'),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": 25474510778,
        "PartyB": 174379,
        "PhoneNumber": phone,
        "CallBackURL": "https://django-server-hazel.vercel.app/callback/",
        "AccountReference": "FEEWIZ",
        "TransactionDesc": "Payment of fEE"
    }

    response = requests.request(
        "POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, json=payload)
    # print(type(response.text))
    print("STATUS CODE ",response.status_code)
    data = response.json()
    print("safaricom json response ",response.json())
    if response.status_code == 200:
        print(data["CustomerMessage"])
        create_transaction(phone, amount, reg_no)
        return "Your request has been received you'll be promptEd for your MPESA PIN shortly.."

    else:
        print(data["errorMessage"])
        return "Cannot process your request at this time, Try again later.."
#     print("json",response.json())
#     # print(json.loads(response.text)['ResponseCode'])

#     print()
#     if json.loads(response.text)['ResponseCode'] == "0":
#         print("success")
#         print(response.text)
#         # pass

# # stk_push()