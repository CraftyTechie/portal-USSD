import africastalking
from django.conf import settings
from django.db import models
from django.core.mail import send_mail

# Create your models here.


class Student(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    pin = models.CharField(
        max_length=4, blank=True, null=True
    )  # PIN is optional for first-time users
    phone = models.CharField(max_length=20, unique=True, null=True)
    email = models.EmailField(unique=True, default="default_email@example.com")

    def __str__(self):
        return self.registration_number


class Year(models.Model):
    YEAR_CHOICES = (
        (1, "Year 1"),
        (2, "Year 2"),
        (3, "Year 3"),
        (4, "Year 4"),
    )
    year_number = models.IntegerField(choices=YEAR_CHOICES)

    def __str__(self):
        return str(self.year_number)


class Unit(models.Model):
    UNIT_CHOICES = (
        ("BIT 110", "BIT 111"),
        ("BIT 123", "BIT 117"),
        ("BIT 210", "BIT 211"),
        ("BIT 213", "BIT 227"),
        ("BIT 313", "BIT 310"),
        ("BIT 311", "BIT 322"),
        ("BIT 410", "BIT 411"),
        ("BIT 423", "BIT 424"),
    )

    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, choices=UNIT_CHOICES)

    class Meta:
        unique_together = ("code", "year")

    def __str__(self):
        return f"{self.code}- year {self.year.year_number}"



class Transcript(models.Model):
    YEAR_CHOICES = (
        (1, "Year 1"),
        (2, "Year 2"),
        (3, "Year 3"),
        (4, "Year 4"),
    )
    GRADE_CHOICE = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
        ("I", "I"),
    )
    code = models.ForeignKey(Unit, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=True
    )
    year = models.IntegerField(choices=YEAR_CHOICES)
    result_session = models.IntegerField()
    result_grade = models.CharField(max_length=2, choices=GRADE_CHOICE)  # B, C, D, etc.

    class Meta:
        unique_together = ("code", "student", "year")

    def __str__(self):
        return f"{self.code}- year {self.year} - {self.result_grade}"


class SupplementaryExam(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ("unit", "student")


class SpecialExam(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ("unit", "student")


class fee(models.Model):
    fee_balance = models.FloatField()
    fee_statement = models.FloatField()
    fee_structure = models.FloatField()


class ClearanceRequest(models.Model):
    phone_number = models.CharField(max_length=15)
    department = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, default="Pending")
    timestamp = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True) 

    def run_on_approve(self):
        
        print("sending message.")
        
        
    
        try:
            
            subject = "Clearance Approved"
            message = f"🎉 Your clearance for {self.department} has been approved!"
            recipient_email = self.student.email  # Get student's email

            if recipient_email:
                send_mail(
                    subject,            # Subject of the email
                    message,            # Email message
                    settings.DEFAULT_FROM_EMAIL,  # Sender email address (ensure this is set in your settings)
                    [recipient_email],  # List of recipient email addresses
                    fail_silently=False,
                )
                print(" Email sent successfully!")
            else:
                print(" No email found for the student.")

        except Exception as e:
            print(f" Failed to send email: {e}")

    def save(self, *args, **kwargs):
        
        if self.pk: 
            original = ClearanceRequest.objects.get(pk=self.pk)
            
            if not original.approve and self.approve:
              
                self.status = "Approved"
                self.run_on_approve()

        
        super(ClearanceRequest, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone_number} - {self.department}"
