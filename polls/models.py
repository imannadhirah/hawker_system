from django.db import models

# Create your models here.


class Signup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name", help_text="Enter your full name.")
    password = models.CharField(max_length=128, verbose_name="Password", help_text="Store hashed passwords securely.")
    manager_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="Manager ID", help_text="ID of the manager if applicable.")
    nric = models.CharField(max_length=15, unique=True, verbose_name="NRIC", help_text="Enter a valid NRIC (unique).")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number", help_text="Enter a valid phone number.")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Enter a valid email address.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Account Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def __str__(self):
        return self.name

class Hawker(models.Model):
    name = models.CharField(max_length=100)
    hawker_id = models.CharField(max_length=15, verbose_name="NRIC", blank=True, null=True)
    password = models.CharField(max_length=128, verbose_name="Password", help_text="Store hashed passwords securely.", blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Enter a valid email address.", blank=True, null=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'PENDING'),
        ('inspected', 'INSPECTED'),
        ('approved', 'APPROVED'),
        ('rejected', 'REJECTED'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'UNPAID'),
        ('paid', 'PAID'),
    ]
    STATUS_SCHEDULE = [
        ('scheduled', 'Scheduled'),
        ('not_scheduled', 'Not Scheduled'),
    ]
    hawker = models.ForeignKey(Hawker, on_delete=models.CASCADE, related_name="applications", blank=True, null=True)
    application_id = hawker.name
    fullname = models.CharField(max_length=100, blank=True, null=True)
    nric = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    race = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name="Email", help_text="Enter a valid email address.", blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    home_address = models.CharField(max_length=200, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    stall_number = models.CharField(max_length=100, null=True, blank=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    license_type = models.CharField(max_length=100, blank=True, null=True)
    nric_document = models.FileField(upload_to="uploads/nric_documents/", blank=True, null=True)
    food_handling_cert = models.FileField(upload_to="uploads/food_handling_cert/", blank=True, null=True)
    application_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid', blank=True, null=True)
    schedule_status = models.CharField(max_length=15,choices=STATUS_SCHEDULE,default='not_scheduled')

    ##for now

    inspector = models.CharField(null=True,blank=True, max_length=100, verbose_name="inspector assign")


    def __str__(self):
        return f"Application for {self.fullname}"


class License(models.Model):
    LICENSE_STATUS_CHOICES = [
        ('pending', 'PENDING'),
        ('active', 'ACTIVE'),
        ('expired', 'EXPIRED'),
    ]
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="license", blank=True, null=True)
    license_id = models.CharField(max_length=15, blank=True, null=True)
    license_status = models.CharField(max_length=10, choices=LICENSE_STATUS_CHOICES, default='pending', blank=True, null=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"License {self.license_id}"

class Renewal(models.Model):
    hawker = models.ForeignKey(Hawker, on_delete=models.CASCADE, related_name="renewal", blank=True, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="renewal", blank=True, null=True)
    expiration_date = models.DateField(null=True, blank=True)
    business_changes = models.CharField(max_length=500, blank=True, null=True)
    document_update = models.FileField(upload_to="uploads/document_update/", blank=True, null=True)

    def __str__(self):
        return f"Renewal Application for {self.hawker.name}"
    

#Inspector Class 

class Inspector(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    inspector_id = models.CharField(max_length=50, blank=True, null=True)
    nric = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    

class Inspection(models.Model):
    INSPECTION_STATUS= [
        ('done', 'done'),
        ('not yet', 'not_yet'),
    ]
    RESULT_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail','Fail')
    ]
    inspection_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="inspection", blank=True, null=True)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name="inspection", blank=True, null=True)
    inspection_date = models.DateField(null=True,blank=True,  verbose_name="Inspection Date")
    inspection_time = models.TimeField(null=True,blank=True,  max_length=100, verbose_name="Inspection Time")
    status_inspection = models.CharField(max_length=10, choices=INSPECTION_STATUS, default='not yet', blank=True, null=True)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inspection for inspector {self.inspector.name}- hawker {self.application.hawker.name}"

class EmergencyInspection(models.Model):
    RESULT_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail','Fail')
    ]
    FINES_CHOICES = [
        ('Pass', 'Pass'),
        ('Approve Fines','Approve_Fines'),
        ('processing', 'processing')
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="emergencyins", blank=True, null=True)
    inspection_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_inspect = models.DateField()
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    fines = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    fines_approval = models.CharField(max_length=20, choices=FINES_CHOICES, default='processing')

    def __str__(self):
        return f"Emergency Inspection {self.application.hawker.name} - {self.result}"


class Fines(models.Model):
    FINE_PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'UNPAID'),
        ('paid', 'PAID'),
    ]
    hawker = models.ForeignKey(Hawker, on_delete=models.CASCADE, related_name="fines", blank=True, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="fines", blank=True, null=True)
    fines_name = models.CharField(max_length=50, blank=True, null=True) 
    issued_date = models.DateField(blank=True, null=True)
    fine_amount = models.CharField(max_length=50, blank=True, null=True)   
    fine_payment_status = models.CharField(max_length=10, choices=FINE_PAYMENT_STATUS_CHOICES, default='unpaid', blank=True, null=True)  
   

    def __str__(self):
        return f"Fines Record for {self.hawker.name}"
 

