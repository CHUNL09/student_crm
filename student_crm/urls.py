"""student_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', views.mylogin),
    url(r'^crm/dashboard', views.dashboard),
    url(r'^logout/', views.mylogout),
    url(r'^index/', views.admin,name='view_data'),
    url(r'^crm/add', views.add),
    url(r'^crm/del', views.delete,name='delete_data'),
    url(r'^crm/edit', views.edit),
    url(r'^crm/statics', views.statics,name='view_statics'),
]
