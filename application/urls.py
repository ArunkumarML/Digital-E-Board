from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('new-application/', views.NewApplication.as_view()),
    path('application-list/',views.ApplicationList.as_view()),
    path('applicant/',views.ApplicationDetails.as_view()),
    path('chart-data/',views.GraphData.as_view()),
    path('create-form/', views.application_form),
    path('applications/',views.application_list),
    path('state/',views.StateList.as_view()),
    path('district/',views.DistrictList.as_view()),
    path('pincode/',views.PincodeList.as_view())
]
