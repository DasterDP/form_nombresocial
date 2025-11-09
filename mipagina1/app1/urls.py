from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('', views.home, name='home'),
    path('formulario/', views.formulario, name='formulario'),
    path('exito/<int:pk>/', views.exito, name='exito'),
    path('send-pdf/', views.send_pdf_view, name='send_pdf'),
]