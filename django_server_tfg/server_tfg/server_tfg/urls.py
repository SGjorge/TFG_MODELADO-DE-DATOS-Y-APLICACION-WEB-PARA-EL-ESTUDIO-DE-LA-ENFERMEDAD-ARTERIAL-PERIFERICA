"""server_tfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_URL_CSS}),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_URL_IMAGES}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_URL_JS}),
    url(r'^csv/(.*)$', 'serverapps.views.downloadCsv'),
    url(r'^test/(.*)$', 'serverapps.views.downloadMedicalTest'),
    url(r'^formSingupPatient(.*)$', 'serverapps.views.formSingupPatient'),
    url(r'^formSearchPatient(.*)$', 'serverapps.views.formSearchPatient'),
    url(r'^formCalculateRisk(.*)$', 'serverapps.views.formCalculateRisk'),
    url(r'^formDeleteUser(.*)$', 'serverapps.views.formDeleteUser'),
    url(r'^restartUsers(.*)$', 'serverapps.views.formRestartUsers'),
    url(r'^uploadTest/(.*)$', 'serverapps.views.formUpdateTest'),
    url(r'^$', 'serverapps.views.index'),
]
