
import requests
import aiohttp
from datetime import datetime
import json
import asyncio
from django.conf import settings
import base64
from .models import Transaction
from .acccess_token import generate_access_token
from asgiref.sync import sync_to_async

passkey = settings.PASSKEY
# datetime.
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
shortCode = "174379"

async def create_transaction(phone, amount, reg_no):
    # Convert synchronous database operations to asynchronous using sync_to_async
    create_transaction_async = sync_to_async(Transaction.objects.create)
    
    # Perform database operation asynchronously
    transaction = await create_transaction_async(phone=phone, amount=amount, student_reg=reg_no)
    return transaction
     
    
async def stk_push(phone, amount, reg_no):
    print("pushing")
    access_token = generate_access_token()
    print("access token", access_token)
    password = base64.b64encode((shortCode + passkey + timestamp).encode('utf-8')).decode('utf-8')
    print(password)
    # async with aiohttp.ClientSession() as session:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": 25474510778,
        "PartyB": 174379,
        "PhoneNumber": phone,
        # "CallBackURL": "https://django-server-hazel.vercel.app/callback/",
        "CallBackURL": "https://21bdbn4c-8000.uks1.devtunnels.ms/callback/",
        "AccountReference": "FEEWIZ",
        "TransactionDesc": "Payment of fEE"
    }
    print("hitting the endpoint")
    response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, json=payload)
    print("endpoint hit")
    # data = response.text()
    print(response)
    if json.loads(response.text)['ResponseCode'] == "0":
        loop = asyncio.get_event_loop()
        asyncio.create_task(create_transaction(phone, amount, reg_no))

    return
        # return data
