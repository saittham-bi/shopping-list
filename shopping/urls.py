from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste, name='liste'),
    path('gekauft/', views.gekauft_liste, name='gekauft_liste'),
    path('toggle/<int:pk>/', views.toggle_gekauft, name='toggle_gekauft'),
    path('edit/<int:pk>/', views.einkauf_edit, name='einkauf_edit'),
    path('delete/<int:pk>/', views.einkauf_delete, name='einkauf_delete'),
    path('reset/', views.alle_als_offen, name='alle_als_offen'),
    path('clear/', views.gekaufte_loeschen, name='gekaufte_loeschen'),
]
