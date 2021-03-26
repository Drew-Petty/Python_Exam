from django.urls import path
from . import views

urlpatterns = [
    path('',views.root ),
    path('register',views.register),
    path('login',views.login),
    path('dashboard',views.main),
    path('logout',views.logout),
    path('newjob',views.newjob),
    path('addjob',views.addjob),
    path('jobs/<int:job_id>',views.viewjob),
    path('destroy/<int:job_id>',views.destroy),
    path('jobs/edit/<int:job_id>',views.edit),
    path('makechange/<int:job_id>',views.makechange),
    path('assign/<int:job_id>',views.assign),
    path('quit/<int:job_id>',views.quit),
]