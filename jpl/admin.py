from django.contrib import admin
from .models import Company, Jobseeker, Resume, CoverLetter, JobApplication, Job, VisibilityPeriod

# Register your models here.
admin.site.register(Company)
admin.site.register(Jobseeker)
admin.site.register(Resume)
admin.site.register(CoverLetter)
admin.site.register(JobApplication)
admin.site.register(Job)
admin.site.register(VisibilityPeriod)
