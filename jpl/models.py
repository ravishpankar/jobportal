from django.db import models
from jpl import errors
from django.contrib.auth.models import User

class Company(models.Model):
    # id
    id = models.BigAutoField(primary_key=True)
    # company name
    name = models.CharField(max_length=255, null=False)
    # address
    address = models.CharField(max_length=255, null=False)
    # premises
    imgpremises = models.ImageField(null=True, blank=True)
    # phone
    phone = models.CharField(max_length=10, null=False)
    # email
    email = models.EmailField(null=False)
    # address
    desc = models.CharField(max_length=1000, null=False)
    # phone
    whyus = models.CharField(max_length=750, null=False)
    # user
    usr = models.OneToOneField(User, on_delete=models.CASCADE, to_field="id")

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(fields=['usr'], name='unique_company'),
        ]

class Jobseeker(models.Model):
    # id
    id = models.BigAutoField(primary_key=True)
    # company name
    name = models.CharField(max_length=50, null=False)
    # premises
    avatar = models.ImageField(null=True, blank=True)
    # phone
    phone = models.CharField(max_length=10, null=False)
    # email
    email = models.EmailField(max_length=255, null=False)
    # date of joining
    doj = models.DateField()
    # gender
    gender = models.CharField(max_length=1, null=False)
    # salary expected
    salaryexpected = models.BigIntegerField()
    # user
    usr = models.OneToOneField(User, on_delete=models.CASCADE, to_field='id')

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(fields=['usr'], name='unique_jobseeker'),
        ]

class Resume(models.Model):
    # id
    id = models.BigAutoField(primary_key=True)
    # resume
    rd = models.FileField(null=True)
    # jobseeker
    js = models.ForeignKey(Jobseeker, on_delete=models.CASCADE, related_name='resume')

class CoverLetter(models.Model):
    # id
    id = models.BigAutoField(primary_key=True)
    # cl
    cl = models.FileField(null=True)
    # jobseeker
    js = models.ForeignKey(Jobseeker, on_delete=models.CASCADE, related_name='cl')

STATE_CHOICES = [
    ('created', 'Created'),
    ('recruitmentinprogress', 'RecruitmentInProgress'),
    ('expired', 'Expired')
]
class Job(models.Model):
    # id
    id = models.BigAutoField(primary_key=True)
    # salary expected
    state = models.CharField(choices=STATE_CHOICES, max_length=50, null=False)
    # perks
    perks = models.CharField(max_length=500, null=False)
    # title
    title = models.CharField(max_length=100, null=False)
    # isc
    interviewselectioncriteria = models.CharField(max_length=500, null=False)
    # jd
    jobdescription = models.CharField(max_length=1000, null=False)
    # gender
    jobtags = models.CharField(max_length=250, null=False)
    # job link
    joblink = models.CharField(max_length=1000, null=True, blank=True)
    # company
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')

class VisibilityPeriod(models.Model):
    # id
    id = models.BigAutoField(primary_key=True)
    # date start
    startdate = models.DateField()
    # date end
    enddate = models.DateField()
    # amount paid
    amountpaid = models.IntegerField()
    # job
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='jobvp')

    def save(self, *args, **kwargs):
        if self.startdate > self.enddate:
            raise errors.JPLException(errors.SD_B_ED, 400)
        if self.amountpaid < 0:
            raise errors.JPLException(errors.AMOUNTINVALID, 400)
        super(VisibilityPeriod, self).save(*args, **kwargs)


class JobApplication(models.Model):
    # id
    id = models.BigAutoField(primary_key=True)
    # job seeker
    jobseeker = models.ForeignKey(Jobseeker, on_delete=models.CASCADE, related_name='jobseeker')
    # resume
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='resume')
    # cover letter
    coverletter = models.ForeignKey(CoverLetter, on_delete=models.CASCADE, related_name='coverletter')
    # job
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='jobja')

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(fields=['job', 'jobseeker'], name='unique_appln'),
        ]

