# import package
import africastalking


# Initialize SDK
username = "sandbox"    # use 'sandbox' for development in the test environment
api_key = "63844ecae6efdf704ed70d2240b823184d6c48419258a10fcda65ab2847718ab"      # use your sandbox app API key for development in the test environment
print("blabla")
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
response = sms.send("Hello Message!", ["+254740510778"],'Fee-wiz')
print(response)

# # Or use it asynchronously
# def on_finish(error, response):
#     if error is not None:
#         raise error
#     print(response)

# sms.send("Hello Message!", ["+2547xxxxxx"], callback=on_finish)