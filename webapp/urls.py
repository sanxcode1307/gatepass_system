from django.urls import path
from webapp import views

urlpatterns = [

    

    path("", views.home, name="home"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("apply_gatepass/", views.apply_gatepass, name="apply_gatepass"),
    path("success/", views.success, name="success"),
    path("warden_dashboard/", views.warden_dashboard, name="warden_dashboard"),
    path("approve_gatepass/<int:pk>/", views.approve_gatepass, name="approve_gatepass"),
    path("reject_gatepass/<int:pk>/", views.reject_gatepass, name="reject_gatepass"),
    path('close_gatepass/<int:pk>/', views.close_gatepass, name='close_gatepass'),
    path("warden_login/", views.warden_login, name="warden_login"),
    
   
   
   
   
   
   
   
  
  
  

  
    
    
    
    
    
    
]

