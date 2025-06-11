from django.db import models
from django.db.models import Sum
from decimal import Decimal 

class RecordSubmission(models.Model):
    EXAMS_TYPE = [
        ('Quiz', 'QUIZ'),
        ('Test-1', 'Test-1'),
        ('Test-2', 'Test-2'),
        ('UE', 'UE'),
       
    ]
    academic_year = models.CharField(max_length=9)  # Example: "2024/25"
    semester_number = models.IntegerField(null=True, blank=True)  # 1, 2, or null
    
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: track when saved

    inv_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    lect_name =  models.CharField(max_length=50)
    course =  models.CharField(max_length=50)
    exam_date =  models.DateField()
    number_of_booklets = models.IntegerField()
    additional_notes =  models.CharField(max_length=50)
    exam_type = models.CharField(max_length=50, choices=EXAMS_TYPE, default="UE")
    file =  models.FileField(upload_to='files/')
    is_collected = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.academic_year} - {self.semester_number}"

class RecordCollection(models.Model):
    EXAMS_TYPE = [
        ('Quiz', 'QUIZ'),
        ('Test-1', 'Test-1'),
        ('Test-2', 'Test-2'),
        ('UE', 'UE'),
       
    ]
    academic_year = models.CharField(max_length=9)  # Example: "2024/25"
    semester_number = models.IntegerField(null=True, blank=True)  # 1, 2, or null
    
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: track when saved
    lect_name = models.CharField(max_length=50)
    number_of_booklets = models.IntegerField()
    course = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    expect_return = models.DateField()
    additional_notes = models.CharField(max_length=350)
    exam_type = models.CharField(max_length=50, choices=EXAMS_TYPE, default="UE")
    is_returned = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.academic_year} - {self.semester_number}"

class RecordReturn(models.Model):
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged'),
    ]
    EXAMS_TYPE = [
        ('Quiz', 'QUIZ'),
        ('Test-1', 'Test-1'),
        ('Test-2', 'Test-2'),
        ('UE', 'UE'),
       
    ]
    academic_year = models.CharField(max_length=9)  # Example: "2024/25"
    semester_number = models.IntegerField(null=True, blank=True)  # 1, 2, or null
    
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: track when saved
    lect_name = models.CharField(max_length=50)
    number_of_booklets = models.IntegerField()
    course = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    return_by = models.CharField(max_length=50)
    return_date = models.DateField()
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES,default='fair')
    additional_notes = models.CharField(max_length=350)
    exam_type = models.CharField(max_length=50, choices=EXAMS_TYPE, default="UE")
    is_returned = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.academic_year} - {self.semester_number}"

