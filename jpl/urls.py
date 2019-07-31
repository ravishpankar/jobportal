from django.urls import path
from rest_framework_jwt.views import verify_jwt_token

from .views import ListCompanyView, RetrieveCompanyView, RetrieveCompanyIView, CreateCompanyView, UpdateCompanyView, DestroyCompanyView, \
    CreateJobseekerView, RetrieveJobseekerView, RegisterEUsers, RetrieveJobseekerIView, UpdateJobseekerView, DestroyJobseekerView,  ListJobseekerView, \
    ListResumeView, ListResumeJSView, CreateResumeView, RetrieveResumeView, DestroyResumeView, \
    UpdateResumeView, ListCoverLetterView, ListCoverLetterJSView, CreateCoverLetterView, RetrieveCoverLetterView, \
    UpdateCoverLetterView, DestroyCoverLetterView, ListJobView, ListJobsCView, ListJobsCVView, ListJobsAVView, CreateJobView, ListJobsFView, \
    RetrieveJobView, UpdateJobView, DestroyJobView, ListVisibilityPeriodView, CreateVisibilityPeriodView, \
    RetrieveLastVisibilityPeriodView, ListJobApplicationView, ListJobApplicationJSView, CreateJobApplicationView, ListJobApplicationJView, RetrieveJobApplicationView,\
    UpdateJobApplicationView, DestroyJobApplicationView, RegisterJSUsers, LoginView, RetrieveRevenueView, RetrieveRevenueCView


urlpatterns = [
    path('jsuser/', RegisterJSUsers.as_view(), name="js-create"),
    path('euser/', RegisterEUsers.as_view(), name="e-create"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('companies/', ListCompanyView.as_view(), name="companies-all"),
    path('company/', CreateCompanyView.as_view(), name="company-create"),
    path('company/<int:id>', RetrieveCompanyView.as_view(), name="company-get"),
    path('ucompany/<int:usr__id>', RetrieveCompanyIView.as_view(), name="company-getbid"),
    path('ccompany/<int:id>', UpdateCompanyView.as_view(), name="company-update"),
    path('dcompany/<int:id>', DestroyCompanyView.as_view(), name="company-delete"),
    path('jobseekers/', ListJobseekerView.as_view(), name="jobseekers-all"),
    path('jobseeker/', CreateJobseekerView.as_view(), name="jobseeker-create"),
    path('jobseeker/<int:id>', RetrieveJobseekerView.as_view(), name="jobseeker-get"),
    path('ujobseeker/<int:usr__id>', RetrieveJobseekerIView.as_view(), name="jobseeker-getbid"),
    path('cjobseeker/<int:id>', UpdateJobseekerView.as_view(), name="jobseeker-update"),
    path('djobseeker/<int:id>', DestroyJobseekerView.as_view(), name="jobseeker-delete"),
    path('resumes/', ListResumeView.as_view(), name="resumes-all"),
    path('resumes/<int:jobseeker>', ListResumeJSView.as_view(), name="resumes-jsall"),
    path('resume/', CreateResumeView.as_view(), name="resume-create"),
    path('resume/<int:id>', RetrieveResumeView.as_view(), name="resume-get"),
    path('cresume/<int:id>', UpdateResumeView.as_view(), name="resume-update"),
    path('dresume/<int:id>', DestroyResumeView.as_view(), name="resume-delete"),
    path('coverletters/', ListCoverLetterView.as_view(), name="coverletters-all"),
    path('coverletters/<int:jobseeker>', ListCoverLetterJSView.as_view(), name="coverletters-jsall"),
    path('coverletter/', CreateCoverLetterView.as_view(), name="coverletter-create"),
    path('coverletter/<int:id>', RetrieveCoverLetterView.as_view(), name="coverletter-get"),
    path('ccoverletter/<int:id>', UpdateCoverLetterView.as_view(), name="coverletter-update"),
    path('dcoverletter/<int:id>', DestroyCoverLetterView.as_view(), name="coverletter-delete"),
    path('jobs/', ListJobView.as_view(), name="jobs-all"),
    path('jobs/<int:id>/', ListJobsCView.as_view(), name="jobs-call"),
    path('vjobs/<int:id>/', ListJobsCVView.as_view(), name="jobs-cvall"),
    path('avjobs/', ListJobsAVView.as_view(), name="jobs-vall"),
    path('fjobs/', ListJobsFView.as_view(), name="jobs-fall"),
    path('job/', CreateJobView.as_view(), name="job-create"),
    path('job/<int:id>', RetrieveJobView.as_view(), name="job-get"),
    path('cjob/<int:id>', UpdateJobView.as_view(), name="job-update"),
    path('djob/<int:id>', DestroyJobView.as_view(), name="job-delete"),
    path('jobapplications/', ListJobApplicationView.as_view(), name="jobapplications-all"),
    path('jobapplications/<int:id>', ListJobApplicationJSView.as_view(), name="jobapplications-jsall"),
    path('jjobapplications/<int:id>', ListJobApplicationJView.as_view(), name="jobapplications-jall"),
    path('jobapplication/', CreateJobApplicationView.as_view(), name="jobapplication-create"),
    path('jobapplication/<int:id>', RetrieveJobApplicationView.as_view(), name="jobapplication-get"),
    path('cjobapplication/<int:id>', UpdateJobApplicationView.as_view(), name="jobapplication-update"),
    path('djobapplication/<int:id>', DestroyJobApplicationView.as_view(), name="jobapplication-delete"),
    path('visibilityperiods/', ListVisibilityPeriodView.as_view(), name="visibilityperiods-all"),
    path('visibilityperiod/', CreateVisibilityPeriodView.as_view(), name="visibilityperiod-create"),
    path('lvisibilityperiod/<int:id>', RetrieveLastVisibilityPeriodView.as_view(), name="lastvisibilityperiod-get"),
    path('revenue/', RetrieveRevenueView.as_view(), name="revenue-get"),
    path('revenue/<int:id>', RetrieveRevenueCView.as_view(), name="revenuec-get"),
]
