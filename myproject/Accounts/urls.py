from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url



#app_name = 'Accounts'

urlpatterns=[
     path('',views.landingpage,name='landingpage'),
     path('register/',views.register, name='register'),
     path('customer_register/',views.customer_register.as_view(), name='customer_register'),
     path('manager_register/',views.manager_register.as_view(), name='manager_register'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('homepage/',views.homepage, name='homepage'),
     path('post/',views.post,name='post'),
     path('edit/<int:key>/',views.edit, name='edit'),
     path('delete/<int:key>/<int:key1>/',views.delete, name='delete'),
     path('upload/',views.upload,name='upload')
]


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)