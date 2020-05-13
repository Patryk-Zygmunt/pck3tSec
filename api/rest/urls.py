from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest import views

urlpatterns = [
    path('hosts/', views.HostListView.as_view(), name='api-hosts'),
    path('threats/', views.ThreatListView.as_view(), name='api-threats'),
    path('stats/', views.StatsListView.as_view(), name='api-stats'),
    path('blacklist/', views.BlackListView.as_view(), name='api-blacklists'),
    path('blacklist/<int:pk>/', views.BlackListDetailView.as_view(), name='api-blacklist-item'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
