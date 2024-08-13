from commons import views
from django.urls import path

urlpatterns = [
    path('wiki', views.query),
]