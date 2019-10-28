from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('chart_data', views.chart_data, name='chart_data'),
    path('line_chart', views.line_chart, name='line_chart'),
    path('pie_chart_leaderboard', views.pie_chart_leaderboard, name='pie_chart_leaderboard'),
    path('line_chart_leaderboard', views.line_chart_leaderboard, name='line_chart_leaderboard'),
    path('pie_chart_insight', views.pie_chart_insight, name='pie_chart_insight'),
    path('line_chart_insight', views.line_chart_insight, name='line_chart_insight'),
]