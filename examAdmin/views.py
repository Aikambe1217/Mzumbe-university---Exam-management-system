from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # type: ignore
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models import Sum
from datetime import date
from django.urls import reverse # type: ignore
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt  
from django.utils import timezone

from main.models import RecordCollection
from main.models import RecordSubmission
from main.models import RecordReturn
from django.http import JsonResponse
import json
import subprocess
import os
from django.conf import settings
from datetime import datetime
from django.urls import reverse
import re

@login_required
def backup_database(request):
    if request.method == 'POST':
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_host = settings.DATABASES['default'].get('HOST', 'localhost')
        db_port = settings.DATABASES['default'].get('PORT', '5432')
        db_password = settings.DATABASES['default']['PASSWORD']

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{db_name}_backup_{timestamp}.sql"
        backup_path = os.path.join(settings.BASE_DIR, 'backups')

        os.makedirs(backup_path, exist_ok=True)
        file_path = os.path.join(backup_path, filename)

        # Set the environment password variable for pg_dump
        os.environ['PGPASSWORD'] = db_password

        # Run pg_dump command
        result = subprocess.run([
            'pg_dump',
            '-h', db_host,
            '-p', db_port,
            '-U', db_user,
            '-F', 'c',  # Custom format
            '-b',       # Include blobs
            '-f', file_path,
            db_name
        ], capture_output=True)

        if result.returncode == 0:
            return HttpResponse(f"Backup created successfully at: {file_path}")
        else:
            return HttpResponse(f"Backup failed: {result.stderr.decode()}")

    return HttpResponse("Invalid request method.")


# Create your views here.
@login_required(login_url='/admin-auth')
def dashboard(request):
     
    total_booklets_submitted = RecordSubmission.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    total_booklets_collected = RecordCollection.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    total_booklets_returned = RecordReturn.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    recent_submission = RecordSubmission.objects.all().order_by('-created_at').first()
    recent_collection = RecordCollection.objects.all().order_by('-created_at').first()
    recent_return = RecordReturn.objects.all().order_by('-created_at').first()
    pendingBooks = int(total_booklets_collected) - int(total_booklets_returned)
    recent_user = User.objects.all().order_by('-date_joined').first()

    submissionOrder = RecordSubmission.objects.all().order_by('-created_at')[:6]
    collectedOrder = RecordCollection.objects.all().order_by('-created_at')[:6]

    current_date = timezone.now().date()
    # Aggregate data
    total_booklets_submitted = RecordSubmission.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    total_booklets_collected = RecordCollection.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    total_booklets_returned = RecordReturn.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    pendingBooks = int(total_booklets_collected) - int(total_booklets_returned)
    total_submission = RecordSubmission.objects.all().count()
    total_collection= RecordCollection.objects.all().count()
    total_return = RecordReturn.objects.all().count()
    total_pending = RecordCollection.objects.filter(is_returned=False).count()

    # Uncollected records
    uncollected_records = RecordCollection.objects.filter(is_returned=False, expect_return__lt=current_date).order_by('created_at')[:6]
    return render(request, 'admin/dashboard.html',{
        'total_submission': total_booklets_submitted,
        'total_collection': total_booklets_collected,
        'total_return': total_booklets_returned,
        'recent_submission': recent_submission,
        'recent_collection': recent_collection,
        'recent_return' : recent_return,
        'pendingBooks': pendingBooks,
        'recent_users': recent_user,
        'subs': submissionOrder,
        'collectsOrder': collectedOrder,
        'pendings': uncollected_records,
        'total_rows':total_submission,
        'total_rows_collected': total_collection,
        'total_rows_returned': total_return,
        'total_pending_rows': total_pending
        })



   




@login_required(login_url='/admin-auth')
def collections(request):

    allRecord = RecordCollection.objects.all()

    # Get filter values from POST request
    course = request.POST.get('course')
    department = request.POST.get('department')
    exam_type = request.POST.get('exam_type')
    year = request.POST.get('year')
    semester = request.POST.get('semester')

    # Apply filters if values are present
    if course:
        allRecord = allRecord.filter(course=course)

    if department:
        allRecord = allRecord.filter(department=department)

    if exam_type:
        allRecord = allRecord.filter(exam_type=exam_type)

    if year:
        allRecord = allRecord.filter(academic_year=year)

    if semester:
        allRecord = allRecord.filter(semester_number=semester)

   
    # Uncollected records
    notreturned = RecordCollection.objects.filter(is_returned=False).count()
    total_message = notreturned 
    uncollected_records = RecordCollection.objects.filter(is_returned=False)

    current_date = timezone.now().date()
    notreturned = RecordCollection.objects.filter(is_returned=False, expect_return__lt=current_date).count()
    total_message = notreturned 
    uncollected_records = RecordCollection.objects.filter(is_returned=False, expect_return=current_date)
    # Create context dictionary

    
    # else:
    #     lecture = RecordSubmission.objects.values('lect_name').distinct()
       

     
    context = {
        'allRecord': allRecord,
        'courses': RecordCollection.objects.values_list('course', flat=True).distinct(),
        'departments': RecordCollection.objects.values_list('department', flat=True).distinct(),
        'years': RecordCollection.objects.values_list('academic_year', flat=True).distinct(),
        'semesters': RecordCollection.objects.values_list('semester_number', flat=True).distinct(),
        'selected_year': year or '',
        'selected_semester': semester or '',
        'total_messages': total_message,
        'pendings': uncollected_records,
        # 'lectures': lecture,
        
    }
    return render(request, 'admin/collections.html', context)






@login_required(login_url='/admin-auth')
def marked(request):
    # if request.method == 'POST':
    # form_type = request.POST.get('form_type')
    allRecord = RecordReturn.objects.all()

    # Get filter values from POST request
    course = request.POST.get('course')
    department = request.POST.get('department')
    exam_type = request.POST.get('exam_type')
    year = request.POST.get('year')
    semester = request.POST.get('semester')

    # Apply filters if values are present
    if course:
        allRecord = allRecord.filter(course=course)

    if department:
        allRecord = allRecord.filter(department=department)

    if exam_type:
        allRecord = allRecord.filter(exam_type=exam_type)

    if year:
        allRecord = allRecord.filter(academic_year=year)

    if semester:
        allRecord = allRecord.filter(semester_number=semester)


    current_date = timezone.now().date()
    notreturned = RecordCollection.objects.filter(is_returned=False, expect_return=current_date).count()
    total_message = notreturned 
    uncollected_records = RecordCollection.objects.filter(is_returned=False, expect_return__lt=current_date)

   
    
        
       
    # Create context dictionary
    context = {
        'allRecord': allRecord,
        'courses': RecordReturn.objects.values_list('course', flat=True).distinct(),
        'departments': RecordReturn.objects.values_list('department', flat=True).distinct(),
        'years': RecordReturn.objects.values_list('academic_year', flat=True).distinct(),
        'semesters': RecordReturn.objects.values_list('semester_number', flat=True).distinct(),
        'selected_year': year or '',
        'selected_semester': semester or '',
        'total_messages': total_message,
        'pendings': uncollected_records,
        # 'lectures': lecture,
    }
    return render(request, 'admin/marked-materials.html', context)

   





@login_required(login_url='/admin-auth')
def profile(request):

    user = request.user

    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname= request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')

      
        if User.objects.exclude(pk=user.pk).filter(username=uname).exists():
            messages.error(request, "Sorry! This username is Taken")

        elif User.objects.exclude(pk=user.pk).filter(email=email).exists():
            messages.error(request, "Sorry! This email taken")

        else:
     
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.username=uname
            

            user.save()
            messages.success(request, "profile update was succesfull")
            return redirect('profile')


    return render(request, 'admin/profile.html')




@login_required(login_url='/admin-auth')
def reports(request):

     # Get all unique academic years and semesters for the dropdown options
    years = RecordReturn.objects.values('academic_year').distinct()
    semesters = RecordReturn.objects.values('semester_number').distinct()

    # Check if filter parameters are provided
    selected_year = request.GET.get('year')
    selected_semester = request.GET.get('semester')
   
    # Initialize queryset with all data
    queryset = RecordReturn.objects.all()

    # Apply filters if parameters are provided
    if selected_year:
        queryset = queryset.filter(academic_year=selected_year)

    if selected_semester:
        queryset = queryset.filter(semester_number=selected_semester)


    current_date = timezone.now().date()
    # Aggregate data
    total_booklets_submitted = RecordSubmission.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    total_booklets_collected = RecordCollection.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    total_booklets_returned = RecordReturn.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    pendingBooks = int(total_booklets_collected) - int(total_booklets_returned)

    # Uncollected records
    uncollected_records = RecordCollection.objects.filter(is_returned=False, expect_return__lt=current_date)
    total_submission = RecordSubmission.objects.all().count()
    total_collection= RecordCollection.objects.all().count()
    total_return = RecordReturn.objects.all().count()
    total_pending = RecordCollection.objects.filter(is_returned=False).count()

    # Render the report page with all the required context
    return render(request, 'admin/reports.html', {
        'pendings': uncollected_records,
        'total_submission': total_booklets_submitted,
        'total_collection': total_booklets_collected,
        'total_return': total_booklets_returned,
        'pendingBooks': pendingBooks,
        'years': years,
        'semesters': semesters,
        'filtered_data': queryset,
        'selected_year': selected_year,
        'selected_semester': selected_semester,
        'total_rows':total_submission,
        'total_rows_collected': total_collection,
        'total_rows_returned': total_return,
        'total_pending_rows': total_pending
    })







def get_academic_year_and_semester():
    today = date.today()
    year = today.year
    month = today.month

    if month >= 10:
        academic_year = f"{year}/{year + 1}"
        semester = 1
    elif month >= 3:
        academic_year = f"{year - 1}/{year}"
        semester = 2
    else:
        academic_year = f"{year - 1}/{year}"
        semester = 1

    return academic_year, semester



from django.db import connection
from django.shortcuts import render

def get_database_size():
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
        size = cursor.fetchone()[0]
    return size

@login_required(login_url='/admin-auth')
def system_settings(request):
    academic_year, semester = get_academic_year_and_semester()
    db_size = get_database_size()
    total_users = User.objects.count()
    total_submissions = RecordSubmission.objects.count()
    total_collection = RecordCollection.objects.count()
    print(f"Academic Year: {academic_year}")
    print(f"Semester: {semester}")

    context = {
        'system_name': 'Examination Materials Management System',
        'university_name': 'Mzumbe University',
        'academic_year': academic_year,
        'semester': semester,
        'default_due_date': 7,
        'timezone': 'UTC+3',
        'date_format': 'YYYY-MM-DD',
        'timezones': ['UTC+0', 'UTC+1', 'UTC+2', 'UTC+3', 'UTC+4'],
        'date_formats': ['YYYY-MM-DD', 'DD-MM-YYYY', 'MM-DD-YYYY'],
        'db_size': db_size,
        'total_users': total_users,
        'total_submissions': total_submissions,
        'total_collections': total_collection
    }

    return render(request, 'admin/settings.html', context)




@login_required(login_url='/admin-auth')
def submissions(request):
    allRecord = RecordSubmission.objects.all()

    # Get filter values from POST request
    course = request.POST.get('course')
    department = request.POST.get('department')
    exam_type = request.POST.get('exam_type')
    year = request.POST.get('year')
    semester = request.POST.get('semester')

    # Apply filters if values are present
    if course:
        allRecord = allRecord.filter(course=course)

    if department:
        allRecord = allRecord.filter(department=department)

    if exam_type:
        allRecord = allRecord.filter(exam_type=exam_type)

    if year:
        allRecord = allRecord.filter(academic_year=year)

    if semester:
        allRecord = allRecord.filter(semester_number=semester)

    uncollected = RecordSubmission.objects.filter(is_collected=False)
    pending_returns = RecordReturn.objects.filter(is_returned=False)


    # total_booklets_collected = RecordCollection.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    # total_booklets_returned = RecordReturn.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0

    lectCollect = RecordCollection.objects.all().count()
    lectSubmit = RecordSubmission.objects.all().distinct().count()
    pendingReturn = int(lectSubmit)-int(lectCollect)
    # pendingBooks = int(lectCollect) - int(total_booklets_returned)

    current_date = timezone.now().date()
    # Uncollected records
    notreturned = RecordCollection.objects.filter(is_returned=False, expect_return=current_date).count()
   
    total_message = notreturned 
    uncollected_records = RecordCollection.objects.filter(is_returned=False, expect_return=current_date)
    # Create context dictionary

    
    
       
        
    context = {
        'allRecord': allRecord,
        'courses': RecordSubmission.objects.values_list('course', flat=True).distinct(),
        'departments': RecordSubmission.objects.values_list('department', flat=True).distinct(),
        'years': RecordSubmission.objects.values_list('academic_year', flat=True).distinct(),
        'semesters': RecordSubmission.objects.values_list('semester_number', flat=True).distinct(),
        'selected_year': year or '',
        'selected_semester': semester or '',
        'uncollected': uncollected,
        'pending_returns': pending_returns,
        'notification_count': uncollected.count() + pending_returns.count(),
        'total_messages': total_message,
        'pendings': uncollected_records,
        
    }

    return render(request, 'admin/submissions.html', context)


   


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST

User = get_user_model()

@require_POST
def toggle_staff_status(request):
    # Get the user ID from the form
    user_id = request.POST.get('user_id')
    
    # Get the next URL to redirect to after processing
    next_url = request.POST.get('next', '/')
    
    # Check if the is_staff checkbox was checked
    is_staff = 'is_staff' in request.POST
    
    try:
        # Get the user object
        user = get_object_or_404(User, id=user_id)
        
        # Update the is_staff status
        user.is_staff = is_staff
        user.save(update_fields=['is_staff'])
        
        # Add a success message
        messages.success(
            request, 
            f"Staff status for {user.username} has been {'enabled' if is_staff else 'disabled'}"
        )
    except Exception as e:
        # Add an error message if something goes wrong
        messages.error(request, f"Error updating staff status: {str(e)}")
    
    # Redirect back to the original page
    return redirect(next_url)

@login_required(login_url='/admin-auth')
def users(request):
    role_input = request.GET.get('role')
    status_input = request.GET.get('status')

    users_qs = User.objects.all()

    # Map role strings to is_staff boolean
    if role_input == 'Administrator':
        users_qs = users_qs.filter(is_superuser=True)
    elif role_input == 'Exam Officer':
        users_qs = users_qs.filter(is_superuser=False)

    # Map status strings to is_active boolean
    if status_input == 'Active':
        users_qs = users_qs.filter(is_active=True)
    elif status_input == 'Not Active':
        users_qs = users_qs.filter(is_active=False)

    def is_strong_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit."
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            return False, "Password must contain at least one special character."
        return True, ""
        
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        role = request.POST.get('role')
        status = request.POST.get('status')
        superuser = request.POST.get('is_superuser')  # checkbox value: "yes" or None
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        is_valid, error_message = is_strong_password(password)
        if not is_valid:
            messages.error(request, f"Password Error: {error_message}")
            return redirect('users')

        # Validation
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Sorry! Username is already taken. Try another one.')
            return redirect('user')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Sorry! Email is already taken. Try another one.')
            return redirect('user')

        is_staff = True  # both roles are treated as staff
        is_active = status == 'active'
        is_superuser = (role == 'admin') or (superuser == 'yes')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname,
            is_active=is_active,
            is_staff=is_staff,
        )

        if is_superuser:
            user.is_superuser = True
            user.save()

        messages.success(request, 'User registration successful!')
        return redirect('users')  # Redirect to your user list view



    

    return render(request, 'admin/users.html', {
        'users': users_qs,
        'roles': ['Administrator', 'Exam Officer'],
        'statuses': ['Active', 'Not Active'],
        'selected_role': role_input,
        'selected_status': status_input,
    })




def delete_submitted_item(request, pk):
    if request.method == "POST":
        # Get the original submission
        item = get_object_or_404(RecordSubmission, id=pk)
        
        # Use its field values to find related records
        lect_name = item.lect_name
        course = item.course
        department = item.department
        exam_type = item.exam_type
        academic_year = item.academic_year
        semester_number = item.semester_number

        # Delete the submission
        item.delete()

        # Delete all matching records in collection and return tables
        RecordCollection.objects.filter(
            lect_name=lect_name,
            course=course,
            department=department,
            exam_type=exam_type,
            academic_year = academic_year,
            semester_number = semester_number
        ).delete()

        RecordReturn.objects.filter(
            lect_name=lect_name,
            course=course,
            department=department,
            exam_type=exam_type,
            academic_year = academic_year,
            semester_number = semester_number
        ).delete()

        messages.success(request, f"All records related to {lect_name} were deleted successfully.")
        return redirect('submissions')
   
def delete_collected_item(request, pk):      
    if request.method == "POST":
        # Get the original submission
        item = get_object_or_404(RecordCollection, id=pk)
        
        # Use its field values to find related records
        lect_name = item.lect_name
        course = item.course
        department = item.department
        exam_type = item.exam_type
        academic_year = item.academic_year
        semester_number = item.semester_number

        # Delete the collection
        item.delete()

        # Delete all matching records in collection and return tables
        RecordReturn.objects.filter(
            lect_name=lect_name,
            course=course,
            department=department,
            exam_type=exam_type,
            academic_year = academic_year,
            semester_number = semester_number
        ).delete()

        RecordSubmission.objects.filter(
            lect_name=lect_name,
            course=course,
            department=department,
            exam_type=exam_type,
            academic_year=academic_year,
            semester_number=semester_number
        ).update(is_collected=False)
        
        messages.success(request, f"{item.lect_name} deleted successfully!")
        return redirect('collections')

       
   

def delete_returned_item(request, pk):
    if request.method == "POST":
        item = get_object_or_404(RecordReturn, id=pk)

        lect_name = item.lect_name
        course = item.course
        department = item.department
        exam_type = item.exam_type
        academic_year = item.academic_year
        semester_number = item.semester_number

        item.delete()

        RecordCollection.objects.filter(
            lect_name=lect_name,
            course=course,
            department=department,
            exam_type=exam_type,
            academic_year = academic_year,
            semester_number = semester_number
        ).update(is_returned=False)

        messages.success(request, f"{item.lect_name} deleted successfully!")
        return redirect('marked')
    
def delete_user(request, pk):
    if request.method == "POST":
        item = get_object_or_404(User, id=pk)
        user = item.username  # Save before deletion
        item.delete()
        messages.success(request, f"{user} deleted successfully!")
        return redirect('users')
   

def addsubmission(request):
    
    if request.method == 'POST':
        academic_year = request.POST.get("academic_year")
        semester = request.POST.get("semester_number")
        exam_type = request.POST.get("exam_type")
        inv_name = request.POST.get("inv_name")
        department = request.POST.get("inv_dept")
        lect_name = request.POST.get("lect_name")
        course = request.POST.get("course_name")
        exam_date = request.POST.get("exam_date")
        number_booklets = request.POST.get("number_booklets")
        additional_notes = request.POST.get("additional_notes")
        file = request.FILES.get("file")

        if exam_type and inv_name and department and lect_name and course and exam_date and number_booklets:
            RecordSubmission.objects.create(
                    academic_year=academic_year,
                    semester_number=semester,
                    exam_type = exam_type,
                    inv_name=inv_name,
                    department=department,
                    lect_name=lect_name,
                    course=course,
                    exam_date=exam_date,
                    number_of_booklets=number_booklets,
                    additional_notes=additional_notes,
                    file=file,
                )

            messages.success(request, "Submission Added!")
            return redirect('addsubmission')
        else:
            messages.error(request, "* are neccessary,  required!")
            return redirect('addsubmission')
        
    return render(request, 'admin/add.html')

def addcollection(request):
    if request.method == 'POST':
        academic_year = request.POST.get("academic_year")
        semester_number = request.POST.get("semester_number")
        exam_type = request.POST.get("exam_type")
        lect_name = request.POST.get("lect_name")
        number_of_booklets = int(request.POST.get("number_booklets") or 0)
        course = request.POST.get("course")
        department = request.POST.get("department")
        phone = request.POST.get("phone")
        expect_return = request.POST.get("return_date")
        additional_notes = request.POST.get("addition")

        if exam_type and lect_name and number_of_booklets and phone and expect_return and course and department:
            # Check if such a record exists in submission
            instance = RecordSubmission.objects.filter(
                academic_year=academic_year,
                semester_number=semester_number,
                lect_name=lect_name,
                course=course,
                department=department,
                exam_type=exam_type,
            ).first()

            if instance is None:
                messages.error(request, "Error! No matching submission found.")
                return redirect('addcollection')


            submission_qs = RecordSubmission.objects.filter(
                academic_year=academic_year,
                semester_number=semester_number,
                lect_name=lect_name,
                course=course,
                department=department,
                exam_type=exam_type,
            )

            if not submission_qs.exists():
                messages.error(request, " Error: No matching submission found.")
                return redirect('addcollection')

            # 2. Get total submitted booklets for that combination
            total_submitted = submission_qs.aggregate(total=Sum('number_of_booklets'))['total'] or 0

            # 3. Get total already collected booklets for same combination
            total_collected = RecordCollection.objects.filter(
                lect_name=lect_name,
                course=course,
                department=department,
                exam_type=exam_type,
            ).aggregate(total=Sum('number_of_booklets'))['total'] or 0


            if RecordCollection.objects.filter(academic_year=instance.academic_year, semester_number=instance.semester_number, lect_name=instance.lect_name, course=instance.course, department=instance.department, exam_type=instance.exam_type).exists():
                messages.error(request, f" Error: {instance.lect_name} has already taken Booklets for marking of {instance.exam_type} for academic year {instance.academic_year}, semester {instance.semester_number}.")
                return redirect('addcollection')

            # 4. Check if collecting more than what was submitted
            if total_collected + number_of_booklets != total_submitted:
                messages.error(request, f" Error: {instance.lect_name} has to take {total_submitted} Booklets for marking.")
                return redirect('addcollection')
            else:
                for submission in submission_qs:
                    submission.is_collected = True
                    submission.save()



            # Create the collection record
            RecordCollection.objects.create(
                academic_year=academic_year,
                semester_number=semester_number,
                exam_type = exam_type,
                lect_name=instance.lect_name,
                number_of_booklets=number_of_booklets,
                phone=phone,
                expect_return=expect_return,
                additional_notes=additional_notes,
                course = instance.course,
                department = instance.department,
            )

            messages.success(request, "Collection Added!")
            return redirect('addcollection')
        else:
            messages.error(request, "* All fields are required!")
            return redirect('addcollection')
        
    else:
        lecture = RecordSubmission.objects.values('lect_name').distinct()
        courseName = RecordSubmission.objects.values_list('course', flat=True).distinct()
        departmentName = RecordSubmission.objects.values_list('department', flat=True).distinct()
        collect = RecordCollection.objects.all().order_by('-created_at')
        collectedOrder = RecordCollection.objects.all().order_by('-created_at')[:4]

        return render(request, 'admin/add.html', {
            'lectures': lecture,
            'courses': courseName,
            'departments': departmentName,
            'collects': collect,
            'collectsOrder': collectedOrder,
        })



   

def addmarked(request):
     if request.method == 'POST':
        academic_year = request.POST.get("academic_year")
        semester_number = request.POST.get("semester_number")
        exam_type = request.POST.get("exam_type")
        lect_name = request.POST.get("lect_name")
        number_of_booklets = int(request.POST.get("number_booklets") or 0)
        course = request.POST.get("course")
        department = request.POST.get("department")
        return_date = request.POST.get("return_date")
        additional_notes = request.POST.get("addition")
        return_by = request.POST.get("return_by")
        condition = request.POST.get("condition")

        if exam_type and lect_name and number_of_booklets and return_by and return_date and course and department and condition:
            # Check if such a record exists in submission
            instance = RecordCollection.objects.filter(
                academic_year=academic_year,
                semester_number=semester_number,
                lect_name=lect_name,
                course=course,
                department=department,
                exam_type=exam_type,
            ).first()

            if instance is None:
                messages.error(request, "Error! No matching collection found.")
                return redirect('addmarked')


            collection_qs = RecordCollection.objects.filter(
                lect_name=lect_name,
                course=course,
                department=department,
                exam_type=exam_type,
            )

            if not collection_qs.exists():
                messages.error(request, " Error: No matching submission found.")
                return redirect('addmarked')

            # 2. Get total submitted booklets for that combination
            total_collected = collection_qs.aggregate(total=Sum('number_of_booklets'))['total'] or 0

            # 3. Get total already collected booklets for same combination
            total_collected_combo = RecordCollection.objects.filter(
                lect_name=lect_name,
                course=course,
                department=department,
                exam_type=exam_type,
            ).aggregate(total=Sum('number_of_booklets'))['total'] or 0


            if RecordReturn.objects.filter(academic_year=academic_year, lect_name=instance.lect_name, course=instance.course, department=instance.department, exam_type=instance.exam_type, ).exists():
                messages.error(request, f" Error: {instance.lect_name} has already made Returns for {instance.exam_type} for academic year {instance.academic_year} of semester {instance.semester_number}.")
                return redirect('addmarked')

            # 4. Check if collecting more than what was submitted
            if number_of_booklets != total_collected:
                messages.error(request, f" Error: {instance.lect_name} has to Return {total_collected} Booklets.")
                return redirect('addmarked')
            else:
                for collected in collection_qs:
                    collected.is_returned = True
                    collected.save()



            # Create the collection record
            RecordReturn.objects.create(
                academic_year=academic_year,
                semester_number=semester_number,
                exam_type = exam_type,
                lect_name=instance.lect_name,
                number_of_booklets=number_of_booklets,
                return_by=return_by,
                return_date=return_date,
                additional_notes=additional_notes,
                course = instance.course,
                department = instance.department,
                condition = condition,
            )


            messages.success(request, "Return Added!")
            return redirect('addmarked')
        else:
            messages.error(request, "* All fields are required!")
            return redirect('addmarked')
        
     else:
        lecture = RecordCollection.objects.values('lect_name').distinct()
        courseName = RecordCollection.objects.values_list('course', flat=True).distinct()
        departmentName = RecordCollection.objects.values_list('department', flat=True).distinct()
        returns = RecordReturn.objects.all().order_by('-created_at')
        returnedOrder = RecordReturn.objects.all().order_by('-created_at')[:4]

        return render(request, 'admin/add.html', {
            'lectures': lecture,
            'courses': courseName,
            'departments': departmentName,
            'returns': returns,
            'returnsOrder': returnedOrder,
        })
     
@login_required(login_url='/admin-auth')
def edit_submission_record(request):
    if request.method == "POST":
        record_id = request.POST.get("record_id")  # ← get the ID from the form
        record = get_object_or_404(RecordSubmission, id=record_id)
        # record = get_object_or_404(RecordSubmission, id=id)
        departments = RecordSubmission.objects.values_list('department', flat=True).distinct()
        courses = RecordSubmission.objects.values_list('course', flat=True).distinct()

            # BEFORE you change any field:
        old_values = {
            'lect_name': record.lect_name,
            'exam_type': record.exam_type,
            'department': record.department,
            'course': record.course,
            'academic_year': record.academic_year,
            'semester_number': record.semester_number,
            
        }

        # Now update fields
        record.academic_year = request.POST.get("academic_year")
        record.semester_number = request.POST.get("semester_number")
        record.exam_type = request.POST.get("exam_type")
        record.department = request.POST.get("inv_dept")
        record.lect_name = request.POST.get("lect_name")
        record.course = request.POST.get("course_name")
        record.exam_date = request.POST.get("exam_date")
        record.number_of_booklets = request.POST.get("number_booklets")

        record.save()

        # Use old values to find and update matching records
        RecordCollection.objects.filter(
            **old_values
        ).update(
            number_of_booklets=record.number_of_booklets,
            lect_name=record.lect_name,
            exam_type=record.exam_type,
            department=record.department,
            course=record.course,
            academic_year=record.academic_year,
            semester_number=record.semester_number
        )

        RecordReturn.objects.filter(
            **old_values
        ).update(
            number_of_booklets=record.number_of_booklets,
            lect_name=record.lect_name,
            exam_type=record.exam_type,
            department=record.department,
            course=record.course,
            academic_year=record.academic_year,
            semester_number=record.semester_number
        )



        messages.success(request, "Edited was Successfull in all Tables !")
        return redirect('submissions')

    # fallback for GET, maybe show a 404 or redirect
    return redirect('submissions')
