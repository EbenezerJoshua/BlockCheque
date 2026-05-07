from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="root_index"),
    path("index.html", views.index, name="index"),
    path("UserLogin.html", views.UserLogin, name="UserLogin"),	      
    path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
    path("RegisterAction", views.RegisterAction, name="RegisterAction"),
    path("Register.html", views.Register, name="Register"),
    path("BankLogin.html", views.BankLogin, name="BankLogin"),	      
    path("BankLoginAction", views.BankLoginAction, name="BankLoginAction"),
  path("GenerateCheque.html", views.GenerateCheque, name="GenerateCheque"),	      
    path("GenerateChequeAction", views.GenerateChequeAction, name="GenerateChequeAction"),
  path("BankDashboard", views.BankDashboard, name="BankDashboard"),
  path("ClearCheque", views.ClearCheque, name="ClearCheque"),
  path("ViewStatus", views.ViewStatus, name="ViewStatus"),
]
