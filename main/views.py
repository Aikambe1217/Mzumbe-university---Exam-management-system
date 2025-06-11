from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # type: ignore
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models import Sum
from datetime import datetime
from django.urls import reverse # type: ignore
from .models import RecordSubmission
from .models import RecordCollection
from .models import RecordReturn
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt  # Only needed if CSRF issues
from django.utils import timezone

# Create your views here.
@login_required(login_url='/authentication/')
def index(request):
    
    total_booklets_submitted = RecordSubmission.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    total_booklets_collected = RecordCollection.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    total_booklets_returned = RecordReturn.objects.aggregate(Sum('number_of_booklets'))['number_of_booklets__sum'] or 0
    recent_submission = RecordSubmission.objects.all().order_by('-created_at').first()
    recent_collection = RecordCollection.objects.all().order_by('-created_at').first()
    recent_return = RecordReturn.objects.all().order_by('-created_at').first()
    pendingBooks = int(total_booklets_collected) - int(total_booklets_returned)
    recent_user = User.objects.all().order_by('-date_joined').first()
    total_submission = RecordSubmission.objects.all().count()
    total_collection= RecordCollection.objects.all().count()
    total_return = RecordReturn.objects.all().count()
    total_pending = RecordCollection.objects.filter(is_returned=False).count()

    return render(request, 'index.html',{
        'total_submission': total_booklets_submitted,
        'total_collection': total_booklets_collected,
        'total_return': total_booklets_returned,
        'recent_submission': recent_submission,
        'recent_collection': recent_collection,
        'recent_return' : recent_return,
        'pendingBooks': pendingBooks,
        'recent_users': recent_user,
        'total_rows':total_submission,
        'total_rows_collected': total_collection,
        'total_rows_returned': total_return,
        'total_pending_rows': total_pending
        })


@login_required(login_url='/authentication/')
def submission(request):
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
            return redirect('submission')
        else:
            messages.error(request, "* are neccessary,  required!")
            return redirect('submission')
    else:
       
        submissionOrder = RecordSubmission.objects.all().order_by('-created_at')[:4]
        return render(request, 'record-submission.html', {'submitted': submission, 'subs': submissionOrder})


@login_required(login_url='/authentication/')
def collection(request):
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
                return redirect('collection')


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
                return redirect('collection')

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
                return redirect('collection')

            # 4. Check if collecting more than what was submitted
            if total_collected + number_of_booklets != total_submitted:
                messages.error(request, f" Error: {instance.lect_name} has to take {total_submitted} Booklets for marking.")
                return redirect('collection')
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
            return redirect('collection')
        else:
            messages.error(request, "* All fields are required!")
            return redirect('collection')

    else:
        lecture = RecordSubmission.objects.values('lect_name').distinct()
        courseName = RecordSubmission.objects.values('lect_name', 'course').distinct()
        departmentName = RecordSubmission.objects.values('department').distinct()
        collect = RecordCollection.objects.all().order_by('-created_at')
        collectedOrder = RecordCollection.objects.all().order_by('-created_at')[:4]

        return render(request, 'record-collection.html', {
            'lectures': lecture,
            'courses': courseName,
            'departments': departmentName,
            'collects': collect,
            'collectsOrder': collectedOrder,
        })



@login_required(login_url='/authentication/')
def return_page(request):
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
                return redirect('return_page')


            collection_qs = RecordCollection.objects.filter(
                lect_name=lect_name,
                course=course,
                department=department,
                exam_type=exam_type,
            )

            if not collection_qs.exists():
                messages.error(request, " Error: No matching submission found.")
                return redirect('return_page')

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
                return redirect('return_page')

            # 4. Check if collecting more than what was submitted
            if number_of_booklets != total_collected:
                messages.error(request, f" Error: {instance.lect_name} has to Return {total_collected} Booklets.")
                return redirect('return_page')
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
            return redirect('return_page')
        else:
            messages.error(request, "* All fields are required!")
            return redirect('return_page')

    else:
        lecture = RecordCollection.objects.values('lect_name').distinct()
        courseName = RecordCollection.objects.values('lect_name', 'course').distinct()
        departmentName = RecordCollection.objects.values('department').distinct()
        returns = RecordReturn.objects.all().order_by('-created_at')
        returnedOrder = RecordReturn.objects.all().order_by('-created_at')[:4]

        return render(request, 'record-return.html', {
            'lectures': lecture,
            'courses': courseName,
            'departments': departmentName,
            'returns': returns,
            'returnsOrder': returnedOrder,
        })





@login_required(login_url='/authentication/')
def report(request):
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
    return render(request, 'reports.html', {
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


@login_required(login_url='/authentication/')
def submission_records(request):
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
    uncollected_records = RecordCollection.objects.filter(is_returned=False, expect_return__lt=current_date)
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

    return render(request, 'submission_records.html', context)

@login_required(login_url='/authentication/')
def collection_records(request):

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
    notreturned = RecordCollection.objects.filter(is_returned=False, expect_return=current_date).count()
    total_message = notreturned 
    uncollected_records = RecordCollection.objects.filter(is_returned=False, expect_return__lt=current_date)
    # Create context dictionary
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
    }
    return render(request, 'collection_records.html', context)

@login_required(login_url='/authentication/')
def return_records(request):
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
    }
    return render(request, 'return_records.html', context)

@login_required(login_url='/authentication/')
def edit_submission_record(request):
    if request.method == "POST":
        record_id = request.POST.get("record_id")  # ← get the ID from the form
        record = get_object_or_404(RecordSubmission, id=record_id)

        # Update fields
        record.academic_year = request.POST.get("academic_year")
        record.semester_number = request.POST.get("semester_number")
        record.exam_type = request.POST.get("exam_type")
        record.department = request.POST.get("inv_dept")
        record.lect_name = request.POST.get("lect_name")
        record.course = request.POST.get("course_name")
        record.exam_date = request.POST.get("exam_date")
        record.number_of_booklets = request.POST.get("number_booklets")

        record.save()
        messages.success(request, "Edited Successfully!")
        return redirect('submission_records')

    # fallback for GET, maybe show a 404 or redirect
    return redirect('submission_records')



@login_required(login_url='/authentication/')
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
            messages.success(request, "profile update was succesfull, Login Required")
            return redirect('/')

    return render(request, 'profile.html')