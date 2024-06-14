from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from django.contrib.messages.views import SuccessMessageMixin

from accounts.forms import LoginPatientForm, RegisterPatientForm, LoginDoctorForm, RegisterDoctorForm, \
    RegisterAdminForm, LoginAdminForm
from mysite.mixins import NextUrlMixin, RequestFormAttachMixin, DocNextUrlMixin, PatientNextUrlMixin, AdminNextUrlMixin


class LoginPatientView(SuccessMessageMixin, PatientNextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginPatientForm
    success_url = '/home/patient_home/'
    template_name = 'accounts/login_patient.html'
    default_next = '/home/patient_home/'
    success_message = "Login Successful"

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class LoginDoctorView(SuccessMessageMixin, DocNextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginDoctorForm
    success_url = '/home/doctor_home/'
    template_name = 'accounts/login_doctor.html'
    default_next = '/home/doctor_home/'
    success_message = "Login Successful"


    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class LoginAdminView(SuccessMessageMixin, AdminNextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginAdminForm
    success_url = '/home/admin_home/'
    template_name = 'accounts/login_admin.html'
    default_next = '/home/admin_home/'
    success_message = "Login Successful"


    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class RegisterPatientView(SuccessMessageMixin, CreateView):
    form_class = RegisterPatientForm
    template_name = 'accounts/register_patient.html'
    success_url = '/accounts/login_patient/'
    success_message = "Created successfully"


class RegisterDoctorView(SuccessMessageMixin, CreateView):
    form_class = RegisterDoctorForm
    template_name = 'accounts/register_doctor.html'
    success_url = '/accounts/login_doctor/'
    success_message = "Created successfully"

class RegisterAdminView(SuccessMessageMixin, CreateView):
    form_class = RegisterAdminForm
    template_name = 'accounts/register_admin.html'
    success_url = '/accounts/login_admin/'
    success_message = "Created successfully"



def logout_patient_view(request):
    logout(request)
    return redirect('/')


def logout_doctor_view(request):
    logout(request)
    return redirect('/')

