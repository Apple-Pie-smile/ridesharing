"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('base/',views.base),
    path('driver/',views.driver),
    path('driverUpdate/',views.driverUpdate),
    path('rideRequest/',views.rideRequest),
    path('sharerSearch/',views.sharerSearch),
    path('sharerConfirm/<int:id>/<int:num>',views.sharerConfirm, name = 'sharerConfirm'),
    path('driverSearch/',views.driverSearch),
    path('driverConfirm/<int:id>', views.driverConfirm, name = 'driverConfirm'),
    path('ownerView/',views.ownerView),
    path('rideDetail/<int:id>', views.rideDetail, name = 'rideDetail'),
    path('rideOwnerEdit/<int:id>', views.rideOwnerEdit, name = 'rideOwnerEdit'),
    path('rideOwnerEdit_hasS/<int:id>', views.rideOwnerEdit_hasS, name = 'rideOwnerEdit_hasS'),
    path('rideOwnerEdit_noS/<int:id>', views.rideOwnerEdit_noS, name = 'rideOwnerEdit_noS'),
    path('rideOwnerCancel/<int:id>', views.rideOwnerCancel, name = 'rideOwnerCancel'),
    path('sharerView/',views.sharerView),
    path('sharerDetail/<int:id>', views.sharerDetail, name = 'sharerDetail'),
    #path('sharerEdit/<int:id>', views.sharerEdit, name = 'sharerEdit'),
    path('sharerCancel/<int:id>', views.sharerCancel, name = 'sharerCancel'),
    path('driverView/',views.driverView),
    path('driverDetail/<int:id>', views.driverDetail, name = 'driverDetail'),
    path('driverCancel/<int:id>', views.driverCancel, name = 'driverCancel'),
    path('driverComplete/<int:id>', views.driverComplete, name = 'driverComplete'),
]