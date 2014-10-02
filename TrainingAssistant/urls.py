from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from trainings import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TrainingAssistant.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload_file/', views.upload_file, name='upload_file')
)
