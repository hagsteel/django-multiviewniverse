from django.conf.urls import patterns, include, url

from django.contrib import admin
from app.views import HomeView, CreatePersonPetView, UpdatePersonPetView

admin.autodiscover()



urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^create/$', CreatePersonPetView.as_view(), name='create'),
    url(r'^update/(?P<person_pk>[\w]+)/(?P<pet_pk>[\w]+)/$', UpdatePersonPetView.as_view(), name='update'),

    url(r'^admin/', include(admin.site.urls)),
)
