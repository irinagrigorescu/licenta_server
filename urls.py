from django.conf.urls.defaults import patterns, include, url

from Enviro import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Enviro_Project.views.home', name='home'),
    # url(r'^Enviro_Project/', include('Enviro_Project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Login User
    url(r'^login/(?P<username>\w+( \w+)*)/(?P<password>\w+)/$', views.login),
    # Register User
    url(r'^register/$', views.register),
    # Get Current Location
    url(r'^current_location/(?P<userId>\d+)/$', views.get_current_location),
    # Get User Profile
    url(r'^get_profile/(?P<userId>\d+)/$', views.get_profile),
    # Get User Spreading Activation Profile
    url(r'^get_sa_profile/(?P<userId>\d+)/$', views.get_sa_profile),
    # Update User Profile
    url(r'^update_profile/$', views.update_profile),
    # Get Booths
    url(r'^get_booths/(?P<userId>\d+)/$', views.get_booths),
    # CheckIn User
    url(r'^checkin/(?P<boothId>\d+)/(?P<userId>\d+)/$', views.checkin),
    # CheckOut User
    url(r'^checkout/(?P<userId>\d+)/$', views.checkout),

    # Admin - generate codes
    url(r'^private/qr/$', views.generate_qr)
)
