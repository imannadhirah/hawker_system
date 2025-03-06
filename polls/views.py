from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Signup
from .models import Hawker
from .models import Application, Inspector, Inspection, License, EmergencyInspection, Fines, Renewal
from datetime import timedelta, date, datetime
from django.utils.timezone import now  
from django.contrib.auth import login, logout
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from datetime import timezone


# Create your views here.


    
def mainscreen(request):
    return render(request, "polls/home.html")



def signupManager(request):
    
    if request.method == "POST":
      
            name = request.POST.get("name")
            password = request.POST.get("password")
            manager_id = request.POST.get("manager_id") or None  # Convert empty string to None
            nric = request.POST.get("nric")
            phone_number = request.POST.get("phone_number")
            email = request.POST.get("email")

            # Check if email, NRIC, or phone number already exists
            if Signup.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use.")
                return redirect("signupManager")
            elif Signup.objects.filter(nric=nric).exists():
                messages.error(request, "NRIC is already registered.")
                return redirect("signupManager")
            elif Signup.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "Phone number is already in use.")
                return redirect("signupManager")
            else:
                # Save to database with hashed password
                Signup.objects.create(
                    name=name,
                    password=password,  # Hash password for security
                    manager_id=manager_id,
                    nric=nric,
                    phone_number=phone_number,
                    email=email,
                )
                messages.success(request, "Signup successful!")
                return redirect("login")  # Redirect to the signup page or another page

    return render(request, "polls/signup1.html")

def login(request):
    if request.method == "POST":
        manager_id = request.POST.get("manager_id")
        password = request.POST.get("password")
        try:
            user = Signup.objects.get(email=manager_id)
            id = user.manager_id
            if password == user.password:
                # ✅ Store user ID in session
                return redirect('manager_profile', manager_id=id)  # ✅ Redirect properly
            else:
                return HttpResponse("Login unsuccessful!")  
        except Signup.DoesNotExist:
            return HttpResponse("No user found")  

    return render(request, "polls/managerlogin.html")


def manager_profile(request, manager_id):
    user = get_object_or_404(Signup, manager_id=manager_id)
    action = request.POST.get("buttonaction")
    request.session['manager_id'] = user.manager_id 
       

    return render(request, "polls/profile.html", {"user": user})

def main_manager_schedule(request):
    # Get user_id from session
    
    hawkers = Hawker.objects.all()
    manager_id = request.session.get("manager_id")
    user = get_object_or_404(Signup, manager_id=manager_id)
    if request.method == "POST":
        schedule = request.POST.get("schedule-button")
        request.session['manager_id'] = manager_id 
        for hawker in hawkers:
            if schedule == hawker.hawker_id:
                request.session['hawker_id'] = hawker.hawker_id
                return redirect('manager_Schedule')
              
    hawkers = Hawker.objects.filter(applications__schedule_status='not_scheduled').distinct()
    return render(request, "polls/mainManagerSchedule.html", {
        "hawkers": hawkers,
        "user": user
         # Pass user_id to template
    })
    

def manager_Schedule(request):
    manager_id = request.session.get("manager_id")
    manager = get_object_or_404(Signup, manager_id=manager_id)
    hawker_id = request.session.get("hawker_id")
    hawkers = Hawker.objects.all()
    user= Hawker.objects.get(hawker_id=hawker_id)
    inspectors = Inspector.objects.all()
    if request.method == "POST":
        submit = request.POST.get("submit")
        time = request.POST.get("time-button")
        date = request.POST.get("date")
        inspector_id = request.POST.get("inspector-assign")
        inspector = Inspector.objects.get(inspector_id=inspector_id)
        if submit == "submit":  
           
            application = user.applications.first()
            application.schedule_status= "scheduled"
            Inspection.objects.create(
            application=application,
            inspection_date=date,
            inspection_time=time, 
            inspector=inspector,
            inspection_id = application.nric
            )
            application.save()
                
            return redirect('main_manager_schedule')
              
              

    return render(request, "polls/managerSchedule.html", {"user": user, "inspector": inspectors,"manager":manager})


def mainApproval(request):

    user_id = request.session.get('user_id')
    hawkers = Hawker.objects.all()
    manager_id = request.session.get("manager_id")
    user = get_object_or_404(Signup, manager_id=manager_id)
    if not user_id:
        return redirect('login')   
    hawkers = Hawker.objects.filter(applications__application_status='inspected').distinct()
    
    return render(request, "polls/mainLicenseApproval.html", {"hawkers": hawkers,"user":user})

def Approval(request,hawker_id):

    hawker = Hawker.objects.get(hawker_id=hawker_id)
    application = hawker.applications.first()
    inspection= application.inspection.first()
    manager_id = request.session.get("manager_id")
    user = get_object_or_404(Signup, manager_id=manager_id)

    if request.method == "POST":
        result = request.POST.get("button-result")
        if result == "approve":
            application.application_status = 'approved'
            application.save()
            return redirect("approval", hawker_id=hawker_id)
        if result == "reject":
            application.application_status = 'rejected'
            application.save()
            return redirect("approval", hawker_id=hawker_id)
        
    return render(request, "polls/Approval.html", {"hawker": hawker,"application":application,"inspection":inspection,"user":user})

    
def mainFines(request):
    manager_id = request.session.get("manager_id")
    user = get_object_or_404(Signup, manager_id=manager_id)
    emergency = EmergencyInspection.objects.filter(fines_approval='processing')
    return render(request, "polls/mainFines.html",{"emergency":emergency, "user":user})

def manage_fines(request,inspection_id):
    manager_id = request.session.get("manager_id")
    user = get_object_or_404(Signup, manager_id=manager_id)
    inspection = EmergencyInspection.objects.get(inspection_id=inspection_id)
    application = inspection.application  # Get related application
    hawker = application.hawker

    if request.method == "POST":
        result = request.POST.get("button-result")
        if result == "fines":
            inspection.fines_approval = 'Approve_Fines'
            inspection.save()
            fine = Fines.objects.create(
                hawker=hawker,
                application=application,
                fines_name="Violation Fine",  # Set an appropriate name
                issued_date=inspection.date_inspect,
                fine_amount= inspection.fines,
                fine_payment_status="unpaid",
            )
            fine.save()
            return redirect("fines", inspection_id)
            
        if result == "reject":
            inspection.fines_approval = 'Pass'
            inspection.save()
            return redirect("fines", inspection_id)
    return render(request, "polls/Fines.html" ,{"inspection":inspection, "user":user})





#Hawker views

def signupHawker(request):
    if request.method == "POST":
        name = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        nric = request.POST.get("ic_number")

        if Hawker.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('signupHawker')
        elif Hawker.objects.filter(hawker_id=nric).exists():
            messages.error(request, "NRIC is already registered.")
            return redirect('signupHawker')
        else:
            Hawker.objects.create(
                name=name,
                password=password,
                hawker_id=nric,
                email=email,
            )
            messages.success(request, "Signup successful! Redirecting to login.")
            return redirect('loginHawker')
    return render(request, "polls/signupHawker.html")



def loginHawker(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Hawker.objects.get(email=email)
            if password == user.password:
                request.session['hawker_id'] = user.hawker_id  # Store session
                return redirect('license')
            else:
                messages.error(request, "Incorrect password!")
        
        except Hawker.DoesNotExist:
            messages.error(request, "User does not exist.")
        
    return render(request, 'polls/signin.html')


def license(request):
    nric = request.session.get('hawker_id')
    
    request.session['hawker_id'] = nric
    # Ensure user exists
    try:
        user = Hawker.objects.get(hawker_id=nric)
    except Hawker.DoesNotExist:
        return redirect('loginHawker')  # Redirect to login if user not found

    # ✅ Check if an application exists for this hawker
    application_exists = Application.objects.filter(hawker=user).exists()

    # ✅ Redirect to licenseApplied if an application exists (even on GET requests)
    if application_exists:
        request.session['hawker_id'] = nric
        return redirect("licenseApplied")

    # ✅ If no application exists, proceed with rendering the form
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        dob = request.POST.get("dob")
        nationality = request.POST.get("nationality")
        race = request.POST.get("race")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        home_address = request.POST.get("home_address")
        business_name = request.POST.get("business_name")
        stall_number = request.POST.get("stall_number")
        business_type = request.POST.get("business_type")
        nric_document = request.FILES.get("nric_document")
        food_handling_cert = request.FILES.get("food_handling_cert")

        # Validation
        if not all([fullname, dob, nationality, race, email, phone_number, home_address,
                    business_name, stall_number, business_type, nric_document, food_handling_cert]):
            messages.error(request, "All fields are required. Please fill in all the details.")
            return redirect("license")

        # ✅ Create application linked to the correct Hawker
        Application.objects.create(
            hawker=user,
            nric=nric,
            application_status="pending",
            fullname=fullname,
            dob=dob,
            nationality=nationality,
            race=race,
            phone_number=phone_number,
            email=email,
            home_address=home_address,
            business_name=business_name,
            stall_number=stall_number,
            business_type=business_type,
            nric_document=nric_document,
            food_handling_cert=food_handling_cert,
            submission_date=date.today()
        )

        messages.success(request, "Your application has been successfully submitted!")
        request.session['hawker_id'] = nric
        return redirect("licenseApplied")

    return render(request, "polls/license.html")


def licenseApplied(request):   
    nric = request.session.get('hawker_id') 
    request.session['hawker_id'] = nric
    if request.method == "GET":
        # Check if the user is navigating to one of the sections
        if "application-status" in request.GET:
            return redirect("application_status")
        elif "digital" in request.GET:
            return redirect("digitalLicense")
        elif "renewal" in request.GET:
            return redirect("renewal")
        elif "fines" in request.GET:
            return redirect("finesHawker")
    
    return render(request, "polls/licenseApplied.html")


def application_status(request):
    nric = request.session.get('hawker_id')
    user = Hawker.objects.get(hawker_id=nric)
    application = Application.objects.filter(hawker=user).first()

    if request.method == "POST" and 'pay' in request.POST:
        # Create license only if it doesn't exist
        if not License.objects.filter(application=application).exists():
            License.objects.create(
                application=application,
                license_status='active',
                license_id=application.nric,
                valid_from=datetime.now(timezone.utc),
                valid_until=datetime.now(timezone.utc) + timedelta(days=365)
            )
        
        # Update application payment status
        application.payment_status = "paid"
        application.save()
        
        # Redirect to refresh the page and show updated status
        return redirect('application_status')

    # Handle navigation
    if request.method == "GET":
        if "license" in request.GET:
            return redirect("license")
        elif "digital" in request.GET:
            return redirect("digitalLicense")
        elif "renewal" in request.GET:
            return redirect("renewal")
        elif "fines" in request.GET:
            return redirect("finesHawker")
    
    return render(request, "polls/status.html", {
        "user": user,
        "application": application
    })


def digitalLicense(request):
    nric = request.session.get('hawker_id')

    # Check if the hawker has submitted an application
    application = Application.objects.filter(nric=nric).first()

    if not application:
        return render(request, 'polls/digitalLicense.html', {'error_message': 'You are not eligible for a digital license.'})

    # Check if the application is approved and paid
    if application.application_status == 'approved' and application.payment_status == "paid":
        license = License.objects.filter(application=application).first()
        return render(request, 'polls/digitalLicense.html', {'application': application, 'license': license})

    # If application exists but is not approved/paid, show an error message
    return render(request, 'polls/digitalLicense.html', {'error_message': 'You are not eligible for a digital license.'})

        
def renewalLicense(request):
    nric = request.session.get('hawker_id')
    user = Hawker.objects.get(hawker_id=nric)

    
    if request.method == "POST":
        expiration_date = request.POST.get("expiration_date")
        business_changes = request.POST.get("business_changes")
        document_update = request.FILES.get("document_update")

        today = datetime.now().date()
        expiration = datetime.strptime(expiration_date, '%Y-%m-%d').date()
        days_until_expiration = (expiration - today).days

        # Check if the license is eligible for renewal (within 30 days of expiration)
        if days_until_expiration > 30:
            messages.error(request, "You are not eligible for license renewal yet. Please apply within 30 days of your license expiration.")
            return redirect("renewal")

        # Check if all fields are filled
        if not all([expiration_date, document_update]):
            messages.error(request, "All fields are required. Please fill in all the details.")
            return redirect("renewal")

        # Save renewal application
        Renewal.objects.create(
            hawker=user,
            expiration_date=expiration_date,
            business_changes=business_changes,
            document_update=document_update
        )

        return redirect("renewalApplied")

    return render(request, "polls/renewal.html", {"user": user})


def renewalApplied(request):
    nric = request.session.get('hawker_id') 
    request.session['hawker_id'] = nric
    
    if request.method == "GET":
        if "application-status" in request.GET:
            return redirect("application_status")
        elif "license" in request.GET:
            return redirect("license")
        elif "digital" in request.GET:
            return redirect("digitalLicense")
        elif "fines" in request.GET:
            return redirect("finesHawker")
    
    return render(request, "polls/renewalApplied.html")

def finesRecord(request):
    # Get the hawker using the session data
    nric = request.session.get('hawker_id')
    user = Hawker.objects.get(hawker_id=nric)
    
    # Fetch all fines for the hawker (not just the first one)
    fines = Fines.objects.filter(hawker=user)

    # Check if the form is submitted to mark fines as paid
    if request.method == "POST" and 'fines' in request.POST:
        fine_id = request.POST.get('fine_id')
        fine = Fines.objects.get(id=fine_id)
        fine.payment_status = "paid"
        fine.save()

        # Return a JSON response after updating the payment status
        return redirect("fines")

    # Handle navigation buttons for other actions
    if request.method == "GET":
        if "license" in request.GET:
            return redirect("license")
        elif "renewal" in request.GET:
            return redirect("renewal")
        elif "application-status" in request.GET:
            return redirect("application_status")
        elif "digital" in request.GET:
            return redirect("digitalLicense")
        elif "fines" in request.GET:
            return redirect("finesHawker")

    return render(request, 'polls/finesHawker.html', {'user': user, 'fines': fines})

def logout_view(request):
    auth_logout(request)
    return redirect("loginHawker")

#inspector views

def inspector_signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        inspector_id = request.POST.get("inspector_id")
        nric = request.POST.get("nric")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")

        # Check if user already exists
        if Inspector.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("inspector_signup")

        # Create new user
        user = Inspector.objects.create(
            name=name,  # Using name as username
            email=email,
            inspector_id=inspector_id,
            nric=nric,
            phone_number=phone_number,
            password=make_password(password)  # Hash the password
        )

        # Save additional details (assuming you have a Profile model)
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("inspector_login")  # Redirect to login page

    return render(request, "polls/inspectorSignup.html")


def inspector_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        button = request.POST.get("signup_button")
        if button == "signup":
            return redirect(inspector_signup)

        try:
            user = Inspector.objects.get(email=email)  # Get user by email
            if check_password(password, user.password):  # Compare hashed password
                user.last_login = now()  # Manually update last_login
                user.save()
                request.session['user_id'] = user.nric  # Manual session handling
                return redirect("mainpage")
            else:
                messages.error(request, "Invalid email or password")
        except Inspector.DoesNotExist:
            messages.error(request, "Enter email and password")

    return render(request, 'polls/inspectorLogin.html')

def inspector_logout(request):
    logout(request)
    return redirect("inspector_login")

def inspector_mainpage(request):

    user_id = request.session.get("user_id")
    if request.method == "POST":
        button = request.POST.get("button")
        if button=="view_profile":
            request.session['user_id'] = user_id
            return redirect("profile")
    return render(request, "polls/mainpage.html")
    
def profile(request):
    user_id = request.session.get("user_id")
    user = Inspector.objects.filter(nric=user_id).first()
    return render(request, "polls/inspectorProfile.html",{"user":user})

def inspectlist(request):

    inspections = Inspection.objects.filter(status_inspection='not yet')
    if request.method == "POST":
        schedule = request.POST.get("do-button")
        
        for inspection in inspections:
            if schedule == inspection.inspection_id:
                request.session['inspection_id'] = inspection.inspection_id
                return redirect('doinspect')
    
    return render(request, "polls/inspectlist.html",{"inspections":inspections})

def doinspect(request):

    inspection_id =  request.session.get("inspection_id")
    inspection = Inspection.objects.get(inspection_id=inspection_id)
    if request.method == "POST":
        result = request.POST.get("result")
        comment = request.POST.get("comment") 

        inspection.result= result
        inspection.comment= comment
        inspection.application.application_status='inspected'
        inspection.application.save()
        inspection.status_inspection = 'done'

        inspection.save()
        return redirect("inspectlist")
    return render(request, "polls/doinspect.html",{"inspection":inspection})

def pastinspect(request):

    inspections = Inspection.objects.filter(status_inspection='done')

    emginspections = EmergencyInspection.objects.all()
    return render(request, "polls/pastinspect.html", {'inspections': inspections, 'emginspections': emginspections})

def emginspect(request):
    application = Application.objects.filter(application_status='approved').first()  # Get one approved application
    hawker = application.hawker if application else None

    if request.method == "POST":
        hawker_id = request.POST.get("hawker")
        inspection_id = request.POST.get("inspection_id")
        location = request.POST.get("location")
        date_inspect = request.POST.get("date_inspect")
        result = request.POST.get("result")
        fines = request.POST.get("fines")
        comment = request.POST.get("comment")
        hawker=Hawker.objects.get(hawker_id=hawker_id)

        if not application:
            messages.error(request, "No approved application found.")
            return redirect("emginspect")

        # Create new Emergency Inspection
        emergency_inspection = EmergencyInspection.objects.create(
            application = Application.objects.get(hawker=hawker),
            inspection_id=inspection_id,
            location=location,
            date_inspect=date_inspect,
            result=result,
            fines=fines,
            comment=comment,
        )
        emergency_inspection.save()

        messages.success(request, "Emergency Inspection Submitted")
        return redirect("emginspect")

    return render(request, "polls/emginspect.html", {"hawker": hawker})