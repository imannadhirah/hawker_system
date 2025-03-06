
class Hawker(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128, verbose_name="Password", help_text="Store hashed passwords securely.")
    nric = models.CharField(max_length=15, unique=True, verbose_name="NRIC", help_text="Enter a valid NRIC (unique).")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Enter a valid email address.")
    def __str__(self):
        return self.name


class Inspector(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name", help_text="Enter your full name.")
    password = models.CharField(max_length=128, verbose_name="Password", help_text="Store hashed passwords securely.")
    inspector_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Inspector ID", help_text="ID of the inspector if applicable.")
    nric = models.CharField(max_length=15, unique=True, verbose_name="NRIC", help_text="Enter a valid NRIC (unique).")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number", help_text="Enter a valid phone number.")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Enter a valid email address.")
    

    def _str_(self):
        return self.name
    
    
    class Meta:
        db_table = 'Inspector'  # Explicitly set the table name


class Signup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name", help_text="Enter your full name.")
    password = models.CharField(max_length=128, verbose_name="Password", help_text="Store hashed passwords securely.")
    manager_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Manager ID", help_text="ID of the manager if applicable.")
    nric = models.CharField(max_length=15, unique=True, verbose_name="NRIC", help_text="Enter a valid NRIC (unique).")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number", help_text="Enter a valid phone number.")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Enter a valid email address.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Account Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")


class application(models.Model):
    STATUS_SCHEDULE = [
        ('scheduled', 'Scheduled'),
        ('not_scheduled', 'Not Scheduled'),
    ]
    hawker = models.ForeignKey(
        Hawker, 
        on_delete=models.CASCADE,  # Deletes Application if Hawker is deleted
        related_name="applications"  # Allows reverse lookup (hawker.applications.all())
    )
    application_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Application ID", help_text="ID of the manager if applicable.")
    application_date = models.DateTimeField()
    application_schedule_status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='not_scheduled')
    inspection_location =models.CharField(null=True, blank=True, max_length=200)
    inspection_date = models.DateField(null=True,blank=True,  verbose_name="Inspection Date")
    inspection_time = models.CharField(null=True,blank=True,  max_length=100, verbose_name="Inspection Time")
    inspector = models.CharField(null=True,blank=True, max_length=100, verbose_name="inspector assign")
    def __str__(self):
        return f"Application for {self.hawker.name} - {self.application_status}"


class Application(models.Model):
    STATUS_SCHEDULE = [
        ('scheduled', 'Scheduled'),
        ('not_scheduled', 'Not Scheduled'),
    ]
    STATUS_CHOICES = [
        ('pending', 'PENDING'),
        ('approved', 'APPROVED'),
        ('rejected', 'REJECTED'),
    ]
    hawker = models.ForeignKey(Hawker, on_delete=models.CASCADE, related_name="applications")
    dob = models.DateField(null=True) 
    nationality = models.CharField(max_length=50)
    race = models.CharField(max_length=50)
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Enter a valid email address.")
    phone_number = models.CharField(max_length=15)
    home_address = models.CharField(max_length=200)
    business_name = models.CharField(max_length=100)
    stall_number = models.CharField(max_length=10, unique=True, null=True, blank=True)  # Newly added
    proposed_location = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100)
    license_type = models.CharField(max_length=100)
    nric_document = models.FileField(upload_to="uploads/nric_documents/")
    food_handling_cert = models.FileField(upload_to="uploads/food_handling_cert/")
    application_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True)  # Automatically sets when created
    application_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Application ID", help_text="ID of the manager if applicable.")
    application_schedule_status = models.CharField(max_length=15,choices=STATUS_SCHEDULE,default='not_scheduled')



    def _str_(self):
        return f"Application for {self.}"

class Inspection(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="Inspections")
    inspection = models.CharField(max_length=15, unique=True, verbose_name="NRIC", help_text="Enter a valid NRIC (unique).")
    inspection_date = models.DateField(null=True,blank=True,  verbose_name="Inspection Date")
    inspection_time = models.CharField(null=True,blank=True,  max_length=100, verbose_name="Inspection Time")
    inspector_id = models.ForeignKey(Inspector.inspector_id, on_delete=models.CASCADE, related_name="Inspections")


class FineRecord(models.Model):
    fine_name = models.CharField(max_length=100)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    payment_status = models.CharField(
        max_length=10,
        choices=[('unpaid', 'UNPAID'), ('paid', 'PAID')],
        default='unpaid'
    )
    fine_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.issued_date + timedelta(days=30)
        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.fine_name} - Due: {self.due_date}"

















