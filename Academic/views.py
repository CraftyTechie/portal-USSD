import re
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    ClearanceRequest,
    Student,
    Transcript,
    Unit,
    SupplementaryExam,
    SpecialExam,
    MpesaIDs,
    fee,
)

from .mpesa import stk_push

import re
from django.shortcuts import get_object_or_404
import requests
from datetime import datetime
import base64


@api_view(["POST"])
def mpesa_callback(request):
    my_dict = request.data
    if my_dict["Body"]["stkCallback"]["ResultCode"] == 0:
        # date = datetime.strptime(str(my_dict["Body"]["stkCallback"]["CallbackMetadata"]["Item"][2]["Value"]), "%Y%m%d%H%M%S")
        amount = my_dict["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        phone = my_dict["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
        mpesa_code = my_dict["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1][
            "Value"
        ]
        checkoutRequestID = my_dict["Body"]["stkCallback"]["CheckoutRequestID"]
        try:
            newMpesaid = MpesaIDs.objects.get(checkoutRequestID=checkoutRequestID)
            newFee = fee.objects.create(student=newMpesaid.student, amount=amount)
        except MpesaIDs.DoesNotExist:
            return HttpResponse("Null")


# @api_view()
@csrf_exempt
def home(request):
    pattern = r"^[A-Z]{3} \d{3}$"
    session_id = request.POST.get("sessionId")
    service_code = request.POST.get("serviceCode")
    phone_number = request.POST.get("phoneNumber")
    print("Phone: ", phone_number.split("+")[1])
    text = request.POST.get("text")
    response = ""
    student = None
    parts = text.split("*")

    if parts and parts[-1] == "00":
        if len(parts) >= 2:
            parts = parts[:-2]  # Remove the last choice and the '00'
        else:
            parts = []  # If nothing left, go to main menu
        text = "*".join(parts)

    if len(parts) >= 3:
        reg_no = parts[1].strip()
        student = Student.objects.filter(registration_number=reg_no).first()

    # # print("text: ", phone_number)
    if text == "":
        response = "CON Welcome to MMUST student portal.\n"
        response = response + "1. Login"
        return HttpResponse(response)

    if text == "1":
        # First request
        print("# First request", text)
        response = "CON enter your registration number\n"
        return HttpResponse(response)

    # SIT/B/01-02282/2021

    if len(parts) == 2 and parts[1].strip():  # Ensure input is valid
        reg_no = parts[1].strip()
        print(f"Checking registration number: {reg_no}")

        student = Student.objects.filter(registration_number=reg_no).first()
        print(f"Student found: {student}")

        if student:
            response = "CON Enter your 4-digit PIN"
        else:
            response = "END Invalid registration number"
    if len(parts) == 3:
        pin = parts[-1]
        if student.pin == pin:

            response = "CON What do you want to view \n"
            response += "1. Examination \n"
            response += "2. Fees \n"
            response += "3. Clearance \n"
            response += "00. Back\n"
        else:
            response = "END You have entered the wrong pin"
    if len(parts) == 4 and parts[-1] == "1":
        response = "CON Choose to view units/Transcripts or apply for exam \n"
        response += "1. Units \n"
        response += "2. Transcript \n"
        response += "3. Special\n"
        response += "4. Supplementary\n"
        response += "00. Back\n"
    if len(parts) == 4 and parts[-1] == "2":
        response = "CON What do you want to view \n"
        response += "1. Pay fees\n"
        response += "2. Fee balance \n"
        response += "3. Fee structure\n"
        response += "00. Back\n"
    elif len(parts) == 5 and parts[-2] == "2" and parts[-1] == "1":
        response = "CON Enter amount to pay:\n"
        response += "00. Back\n"
    elif len(parts) == 6 and parts[-3] == "2" and parts[-2] == "1":
        amount = parts[-1]
        try:
            print(f"USSD parts: {parts}")  # Debugging the input
            amount = int(parts[-1])  # Get amount from user input
            print(f"Amount entered: {amount}, Type: {type(amount)}")

            if amount <= 0:
                response = "END Invalid amount. Please enter a positive value."
            else:
                print(" Amount is valid. Proceeding to initiate MPESA payment...")

                try:
                    payment_response = stk_push(
                        phone_number.split("+")[1], amount, student
                    )
                    print(f"📲 Payment response: {payment_response}")

                    if not payment_response:
                        response = "END Payment failed: No response from MPESA."
                    elif "errorMessage" in payment_response:
                        response = f"END Payment initiation failed: {payment_response['errorMessage']}"
                    elif "ResponseDescription" in payment_response:
                        response = f"END You’re about to pay KES {amount}. Check your phone and enter MPESA PIN to complete payment."
                    else:
                        response = "END Payment response received, but could not parse it properly."

                except Exception as e:
                    print(f" Error during STK Push: {e}")
                    response = "END  Something went wrong during payment. Please try again later."

        except ValueError:
            print(" Could not convert input to an integer.")
            response = "END Please enter a valid number for the amount."

        except Exception as e:
            print(f" Unexpected error: {e}")
            response = "END Something went wrong. Try again later."

    if len(parts) == 4 and parts[-1] == "3":
        response = "CON Where do you want to clear \n"
        response += "1. Finance \n"
        response += "2. Registrar\n"
        response += "3. School \n"
        response += "3. Library \n"
        response += "00. Back\n"
    elif len(parts) == 3 and parts[0] == "5" and parts[1] == "1":
        dept_choice = parts[2]
        departments = {"1": "Finance", "2": "Registrar", "3": "School", "4": "Library"}

        department = departments.get(dept_choice)

        if department:
            try:
                clearance = ClearanceRequest.objects.create(
                    student=student,  # Assuming you have student object earlier
                    phone_number=phone_number,
                    department=department,
                    status="Pending",
                )
                clearance.save()
                response = f"END Clearance request sent to {department}.\nYou'll receive an SMS once it's processed."
            except Exception as e:
                response = f"END  Failed to save: {str(e)}"
        else:
            response = "END  Invalid department choice. Please try again."
    if len(parts) == 5 and parts[3] == "3":
        if parts[-1] == "1":
            finClear = ClearanceRequest.objects.create(
                phone_number=student.phone,
                department="Finance",
            )
            finClear.save()
            response = "END Your request has been received!!"
        if parts[-1] == "2":
            finClear = ClearanceRequest.objects.create(
                phone_number=student.phone,
                department="Registrar",
            )
            finClear.save()
            response = "END Your request has been received!!"
        if parts[-1] == "3":
            finClear = ClearanceRequest.objects.create(
                phone_number=student.phone,
                department="School",
            )
            finClear.save()
            response = "END Your request has been received!!"
        if parts[-1] == "4":
            finClear = ClearanceRequest.objects.create(
                phone_number=student.phone,
                department="Library",
            )
            finClear.save()
            response = "END Your request has been received!!"
    if len(parts) == 5 and parts[3] == "1" and parts[-1] == "1":
        response = "CON choose the year \n"
        response += "1. Year 1\n"
        response += "2. Year 2\n"
        response += "3. Year 3\n"
        response += "4. Year 4\n"
        response += "00. Back\n"
    # Handling Year Selection (Examination > Units > Year)
    elif len(parts) == 6 and parts[3] == "1" and parts[4] == "1":
        year = parts[-1]  # Selected Year (1, 2, 3, or 4)
        print(f"Selected Year: {year}")  # Debugging output to see the selected year

        # Validate the year is correct
        if year in ["1", "2", "3", "4"]:
            # Fetch units for the student for the selected year
            units = Unit.objects.filter(year__year_number=int(year))

            # Check if any units were found for the selected year
            if units.exists():
                unit_list = "\n".join([f"{unit.code}" for unit in units])
                response = f"END Your Units for Year {year}:\n{unit_list}"
            else:
                response = f"END No units found for Year {year}."
        else:
            response = (
                "END Invalid year selected. Please choose between Year 1, 2, 3, or 4."
            )

    if len(parts) == 5 and parts[3] == "1" and parts[4] == "2":
        print("Checking transcript")
        response = "CON Choose the year \n"
        response += "1. Year 1\n"
        response += "2. Year 2\n"
        response += "3. Year 3\n"
        response += "4. Year 4\n"
        response += "00. Back\n"
        print("parts= ", parts)

    if len(parts) == 6 and parts[3] == "1" and parts[4] == "2":
        year = parts[-1]  # Selected Year (1, 2, 3, or 4)
        print(f"Selected Year: {year}")  # Debugging output to see the selected year

        # Validate the year is correct
        if year in ["1", "2", "3", "4"]:
            # Fetch units for the student for the selected year
            units = Transcript.objects.filter(student=student, year=year)

            # Check if any units were found for the selected year
            if units.exists():
                unit_list = "\n".join(
                    [f"{unit.code.code} - {unit.result_grade}" for unit in units]
                )
                response = f"END Your results for Year {year}:\n{unit_list}"

            else:
                response = f"END No results found for Year {year}."
        else:
            response = (
                "END Invalid year selected. Please choose between Year 1, 2, 3, or 4."
            )
        # response = "CON Enter unit code \n"
    if len(parts) == 5 and parts[3] == "1" and parts[4] == "3":
        response = "CON Enter unit code eg: BIT 111: \n"
    if len(parts) == 6 and parts[3] == "1" and parts[4] == "3":
        if re.match(pattern, parts[-1]):
            try:

                unit = Unit.objects.get(code=parts[-1])
                supp = SpecialExam.objects.create(student=student, unit=unit)
                supp.save()
                response = "END Special exam registered successfully!!"
            except Unit.DoesNotExist:
                response = "END Unit code does not exist!!"
               
        
           
            except Unit.MarksAlreadyExist:
              response="END Marks already Exits"
        else:
            response = "END Enter a valid unit code!!"
    if len(parts) == 5 and parts[3] == "1" and parts[4] == "4":
        response = "CON Enter unit code eg: BIT 111 \n"
    if len(parts) == 6 and parts[3] == "1" and parts[4] == "4":
        if re.match(pattern, parts[-1]):
            try:

                unit = Unit.objects.get(code=parts[-1])
                supp = SupplementaryExam.objects.create(student=student, unit=unit)
                supp.save()
                response = "END Supplementary registered successfully!!"
            except Unit.DoesNotExist:
                response = "END Unit code does not exist!!"
        else:
            response = "END Enter a valid unit code!!"

    return HttpResponse(response)
