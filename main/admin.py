from django.contrib import admin
from .models import RecordSubmission
from .models import RecordCollection
from .models import RecordReturn

# Register your models here.
admin.site.register(RecordSubmission)
admin.site.register(RecordCollection)
admin.site.register(RecordReturn)

