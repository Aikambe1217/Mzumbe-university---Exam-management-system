from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import RecordCollection, RecordSubmission
from django.db.models import Sum

@receiver(post_delete, sender=RecordCollection)
def update_submission_on_delete(sender, instance, **kwargs):
    # Find matching submissions
    submissions = RecordSubmission.objects.filter(
        lect_name=instance.lect_name,
        course=instance.course,
        department=instance.department,
        exam_type = instance.exam_type,
        academic_year = instance.academic_year,
        semester_number = instance.semester_number,
    )

    # Get total submitted
    total_submitted = submissions.aggregate(total=Sum('number_of_booklets'))['total'] or 0

    # Get new total collected after deletion
    total_collected = RecordCollection.objects.filter(
        lect_name=instance.lect_name,
        course=instance.course,
        department=instance.department,
        exam_type = instance.exam_type,
        academic_year = instance.academic_year,
        semester_number = instance.semester_number,
    ).aggregate(total=Sum('number_of_booklets'))['total'] or 0

    # If less collected than submitted, set all to not collected
    if total_collected != total_submitted:
        for submission in submissions:
            submission.is_collected = False
            submission.save()

# from django.db.models.signals import post_delete
# from django.dispatch import receiver
# from .models import RecordCollection, RecordSubmission

# @receiver(post_delete, sender=RecordCollection)
# def reset_submission_status(sender, instance, **kwargs):
#     # Get the corresponding submission record
#     submission_record = RecordSubmission.objects.filter(
#         lect_name=instance.lect_name,
#         course_name=instance.course,
#         department=instance.department
#     ).first()

#     if submission_record:
#         # Reset the is_collected field in RecordSubmission
#         submission_record.is_collected = False
#         submission_record.save()

