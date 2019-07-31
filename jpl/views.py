from rest_framework import generics
from .models import Company, Jobseeker, Resume, CoverLetter, Job, VisibilityPeriod, JobApplication
from .serializers import CompanySerializer, JobseekerSerializer, TokenSerializer, UserSerializer, ResumeSerializer, CoverLetterSerializer, JobSerializer, VisibilityPeriodSerializer, JobApplicationSerializer
from jpl import notifications, errors, decorators
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import Group, User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.
class ListCompanyView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

# Create company
class CreateCompanyView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def create(self, request, *args, **kwargs):
        try:
            return super(generics.CreateAPIView, self).create(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# get company
class RetrieveCompanyView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def get(self, request, *args, **kwargs):
        try:
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)


# get company by id
class RetrieveCompanyIView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    lookup_field = "usr__id"
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def get(self, request, *args, **kwargs):
        try:
            generics.RetrieveAPIView.queryset = Company.objects.filter(usr__id=kwargs["usr__id"])
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Update company
class UpdateCompanyView(generics.UpdateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def patch(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).partial_update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), job__company__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

    @decorators.authenticate_request
    @decorators.is_es
    def put(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), job__company__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Delete company
class DestroyCompanyView(generics.DestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def destroy(self, request, *args, **kwargs):
        try:
            res = super(generics.DestroyAPIView, self).destroy(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), job__company__email=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

class ListJobseekerView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Jobseeker.objects.all()
    serializer_class = JobseekerSerializer

# Create jobseeker
class CreateJobseekerView(generics.CreateAPIView):
    serializer_class = JobseekerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def create(self, request, *args, **kwargs):
        try:
            return super(generics.CreateAPIView, self).create(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Get jobseeker
class RetrieveJobseekerView(generics.RetrieveAPIView):
    serializer_class = JobseekerSerializer
    queryset = Jobseeker.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def get(self, request, *args, **kwargs):
        try:
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)


# Get jobseeker by id
class RetrieveJobseekerIView(generics.RetrieveAPIView):
    serializer_class = JobseekerSerializer
    lookup_field = 'usr__id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def get(self, request, *args, **kwargs):
        try:
            generics.RetrieveAPIView.queryset = Jobseeker.objects.filter(usr__id=kwargs["usr__id"])
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)


# Update jobseeker
class UpdateJobseekerView(generics.UpdateAPIView):
    serializer_class = JobseekerSerializer
    queryset = Jobseeker.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def patch(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).partial_update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), jobseeker__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

    @decorators.authenticate_request
    @decorators.is_js
    def put(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), jobseeker__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Delete jobseeker
class DestroyJobseekerView(generics.DestroyAPIView):
    serializer_class = JobseekerSerializer
    queryset = Jobseeker.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def destroy(self, request, *args, **kwargs):
        try:
            res = super(generics.DestroyAPIView, self).destroy(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), jobseeker__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

class ListResumeView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()

class ListResumeJSView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = ResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def list(self, request, *args, **kwargs):
        try:
            generics.ListAPIView.queryset = Resume.objects.filter(js=kwargs['jobseeker'])
            return super(generics.ListAPIView, self).list(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Create resume
class CreateResumeView(generics.CreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def create(self, request, *args, **kwargs):
        try:
            return super(generics.CreateAPIView, self).create(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Update resume
class UpdateResumeView(generics.UpdateAPIView):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def put(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), resume__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

    @decorators.authenticate_request
    @decorators.is_js
    def patch(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).partial_update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), resume__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Delete resume
class DestroyResumeView(generics.DestroyAPIView):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def destroy(self, request, *args, **kwargs):
        try:
            res = super(generics.DestroyAPIView, self).destroy(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), resume_id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Get resume
class RetrieveResumeView(generics.RetrieveAPIView):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)


class ListCoverLetterView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = CoverLetterSerializer
    queryset = CoverLetter.objects.all()

# list of jobseeker's coverletters
class ListCoverLetterJSView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = CoverLetterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def list(self, request, *args, **kwargs):
        try:
            generics.ListAPIView.queryset = CoverLetter.objects.filter(js=kwargs['jobseeker'])
            return super(generics.ListAPIView, self).list(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Create cover letter
class CreateCoverLetterView(generics.CreateAPIView):
    serializer_class = CoverLetterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def create(self, request, *args, **kwargs):
        try:
            return super(generics.CreateAPIView, self).create(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Update cover letter
class UpdateCoverLetterView(generics.UpdateAPIView):
    serializer_class = CoverLetterSerializer
    queryset = CoverLetter.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def put(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), coverletter__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

    @decorators.authenticate_request
    @decorators.is_js
    def patch(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).partial_update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), coverletter__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Delete cover letter
class DestroyCoverLetterView(generics.DestroyAPIView):
    serializer_class = CoverLetterSerializer
    queryset = CoverLetter.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def destroy(self, request, *args, **kwargs):
        try:
            res = super(generics.DestroyAPIView, self).destroy(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), coverletter__id=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Get cover letter
class RetrieveCoverLetterView(generics.RetrieveAPIView):
    serializer_class = CoverLetterSerializer
    queryset = CoverLetter.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def get(self, request, *args, **kwargs):
        try:
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)


class ListJobView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# list of a company's jobs
class ListJobsCView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request, *args, **kwargs):
        try:
            generics.ListAPIView.queryset = Job.objects.filter(company=kwargs['id'])
            return super(generics.ListAPIView, self).list(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# list of company's visible jobs
class ListJobsCVView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request, *args, **kwargs):
        try:
            generics.ListAPIView.queryset = Job.objects.filter(~Q(state="Expired"), company=kwargs['id'])
            jqs = []
            for j in generics.ListAPIView.queryset:
                queryset = VisibilityPeriod.objects.filter(job=j.id)
                for o in queryset:
                    if o.startdate >= datetime.today().date() and o.enddate >= datetime.today().date():
                        jqs.append(j)
                        break
            generics.ListAPIView.queryset = jqs
            return super(generics.ListAPIView, self).list(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# list of all visible jobs
class ListJobsAVView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request, *args, **kwargs):
        try:
            generics.ListAPIView.queryset = Job.objects.filter(~Q(state="Expired"))
            jqs = []
            for j in generics.ListAPIView.queryset:
                queryset = VisibilityPeriod.objects.filter(job=j.id)
                for o in queryset:
                    if o.startdate >= datetime.today().date() and o.enddate >= datetime.today().date():
                        jqs.append(j)
                        break
            generics.ListAPIView.queryset = jqs
            return super(generics.ListAPIView, self).list(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# list of filtered jobs
class ListJobsFView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request, *args, **kwargs):
        try:
            vt = request.GET.get('title', '')
            generics.ListAPIView.queryset = []
            vc = request.GET.get('company', '')
            if vt != '' and vc != '':
                generics.ListAPIView.queryset = Job.objects.filter(~Q(state="Expired"), title=vt, company__name=vc)
            elif vt != '':
                generics.ListAPIView.queryset = Job.objects.filter(~Q(state="Expired"), title=vt)
            elif vc != '':
                generics.ListAPIView.queryset = Job.objects.filter(~Q(state="Expired"), company__name=vc)

            jqs = []
            for j in generics.ListAPIView.queryset:
                queryset = VisibilityPeriod.objects.filter(job=j.id)
                for o in queryset:
                    if o.startdate >= datetime.today().date() and o.enddate >= datetime.today().date():
                        jqs.append(j)
                        break
            generics.ListAPIView.queryset = jqs
            return super(generics.ListAPIView, self).list(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Create job
class CreateJobView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def create(self, request, *args, **kwargs):
        try:
            return super(generics.CreateAPIView, self).create(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Update job
class UpdateJobView(generics.UpdateAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def put(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), job=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

    @decorators.authenticate_request
    @decorators.is_es
    def patch(self, request, *args, **kwargs):
        try:
            res = super(generics.UpdateAPIView, self).partial_update(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), job=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Delete job
class DestroyJobView(generics.DestroyAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def destroy(self, request, *args, **kwargs):
        try:
            res = super(generics.DestroyAPIView, self).destroy(request, *args, **kwargs)
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), job=kwargs['id'])
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Get job
class RetrieveJobView(generics.RetrieveAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)


class ListVisibilityPeriodView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = VisibilityPeriod.objects.all()
    serializer_class = VisibilityPeriodSerializer

# get last visibility period for a job
class RetrieveLastVisibilityPeriodView(generics.RetrieveAPIView):
    """
    Provides a get method handler.
    """
    queryset = VisibilityPeriod.objects.all()
    serializer_class = VisibilityPeriodSerializer
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def get(self, request, *args, **kwargs):
        try:
            generics.RetrieveAPIView.queryset = VisibilityPeriod.objects.filter(job=kwargs['id'])
            l = None
            for o in generics.RetrieveAPIView.queryset:
                if l is None:
                    l = o
                else:
                    if o.enddate > l.enddate:
                        l = o
            generics.RetrieveAPIView.queryset = l
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Create visibility period
class CreateVisibilityPeriodView(generics.CreateAPIView):
    serializer_class = VisibilityPeriodSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    @decorators.authenticate_request
    @decorators.is_es
    def create(self, request, *args, **kwargs):
        try:
            dt = datetime.strptime(request.data['startdate'], '%Y-%m-%d')
            d = dt.date()
            queryset = VisibilityPeriod.objects.filter(job=request.data['job'])
            med = None
            for o in queryset:
                if med is None:
                    med = o.enddate
                else:
                    if o.enddate > med:
                        med = o.enddate

            if med is not None and med > d:
                raise Exception(errors.V_SD_B_LED)

            return super(generics.CreateAPIView, self).create(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)


class ListJobApplicationView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

# list of jobseeker's job applications
class ListJobApplicationJSView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = JobApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def list(self, request, *args, **kwargs):
        try:
            generics.ListAPIView.queryset = JobApplication.objects.filter(jobseeker=kwargs['id'])
            return super(generics.ListAPIView, self).list(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# list of job's applications
class ListJobApplicationJView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = JobApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_es
    def list(self, request, *args, **kwargs):
        try:
            generics.ListAPIView.queryset = JobApplication.objects.filter(job=kwargs['id'])
            return super(generics.ListAPIView, self).list(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Create job application
class CreateJobApplicationView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def create(self, request, *args, **kwargs):
        try:
            queryset = Job.objects.filter(~Q(state="Expired"), ~Q(state="RecruitmentInProgress"), id=request.data['job'])
            vpqs = VisibilityPeriod.objects.filter(job=queryset[0].id)
            v = False
            for o in vpqs:
                if o.startdate >= datetime.today().date() and o.enddate >= datetime.today().date():
                    v = True
                    break
            if not v:
                raise Exception(errors.JOB_INVISIBLE)
            return super(generics.CreateAPIView, self).create(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Update job application
class UpdateJobApplicationView(generics.UpdateAPIView):
    serializer_class = JobApplicationSerializer
    queryset = JobApplication.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def put(self, request, *args, **kwargs):
        try:
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), id=kwargs['id'])
            res = super(generics.UpdateAPIView, self).update(request, *args, **kwargs)
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

    @decorators.authenticate_request
    @decorators.is_js
    def patch(self, request, *args, **kwargs):
        try:
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), id=kwargs['id'])
            res = super(generics.UpdateAPIView, self).partial_update(request, *args, **kwargs)
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Delete job application
class DestroyJobApplicationView(generics.DestroyAPIView):
    serializer_class = JobApplicationSerializer
    queryset = JobApplication.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @decorators.authenticate_request
    @decorators.is_js
    def destroy(self, request, *args, **kwargs):
        try:
            queryset = JobApplication.objects.filter(~Q(job__state="Expired"), id=kwargs['id'])
            res = super(generics.DestroyAPIView, self).destroy(request, *args, **kwargs)
            notifications.sendemail()
            return res
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# Get job spplication
class RetrieveJobApplicationView(generics.RetrieveAPIView):
    serializer_class = JobApplicationSerializer
    queryset = JobApplication.objects.all()
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            return super(generics.RetrieveAPIView, self).retrieve(request, *args, **kwargs)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# revenue during a period
class RetrieveRevenueView(generics.RetrieveAPIView):
    """
    Provides a get method handler.
    """
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            qs = VisibilityPeriod.objects.filter(startdate__gte=request.GET.get('startdate'), startdate__lte=request.GET.get('enddate'))
            p = 0
            for o in qs:
                p += o.amountpaid

            return JsonResponse({"revenue" : p})
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)

# revenue from a company
class RetrieveRevenueCView(generics.RetrieveAPIView):
    """
    Provides a get method handler.
    """
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            qs = VisibilityPeriod.objects.filter(job__company__id=kwargs['id'])
            p = 0
            for o in qs:
                p += o.amountpaid
            return JsonResponse({"revenue" : p})
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)


class RegisterJSUsers(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        my_group = Group.objects.get(name='JobSeekers')
        my_group.user_set.add(new_user)
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )

class RegisterEUsers(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        my_group = Group.objects.get(name='Employers')
        my_group.user_set.add(new_user)
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                ),
                "id": user.pk})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
