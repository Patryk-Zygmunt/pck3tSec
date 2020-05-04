from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest import views

urlpatterns = [
    path('hosts/', views.HostListView.as_view()),
    path('threats/', views.ThreatListView.as_view()),
    path('stats/', views.StatsListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)