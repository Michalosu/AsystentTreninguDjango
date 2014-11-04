from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from trainings import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TrainingAssistant.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls), name='admin_panel'),
    url(r'^upload_file/', views.upload_file, name='upload_file'),
    url(r'^training/(?P<training_id>\d+)/$', views.view_training, name='view_training'),
    url(r'^trainings/', views.trainings, name='trainings'),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
