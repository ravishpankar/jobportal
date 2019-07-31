from rest_framework import serializers
from .models import Company, Job, Resume, CoverLetter, Jobseeker, VisibilityPeriod, JobApplication
from django.contrib.auth.models import User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "address", "imgpremises", "phone", "email", "whyus", "desc", "usr")


class JobseekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobseeker
        fields = ("id", "name", "avatar", "phone", "email", "doj", "gender", "salaryexpected", "usr")

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("id", "rd", "js")

class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ("id", "cl", "js")

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("id", "state", "perks", "title", "interviewselectioncriteria", "jobdescription", "jobtags", "joblink", "company")

class VisibilityPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisibilityPeriod
        fields = ("id", "startdate", "enddate", "amountpaid", "job")

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ("id", "jobseeker", "resume", "coverletter", "job")

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
    id = serializers.IntegerField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "email")