from django.urls import path
from django.views.generic import TemplateView

from summarizer import views


urlpatterns = [
    path('my-view/<int:pk>/', views.my_view, name='my_view'),
    path('', views.index, name='index'),
    path('summarize_page', views.summarize_page, name='summarize_page'),
    path('summarize_nepali_page', views.summarize_nepali_page, name='summarize_nepali_page'),
    path('save_summary', views.save_summary, name='save_summary'),
    path('history', views.history, name='history'),
    path('history_topic', views.history_topic, name='history_topic'),
    path('nepali', TemplateView.as_view(template_name='summarizer/nepali.html'), name='nepali'),
    path('download_summary_pdf/<int:summary_id>/', views.download_summary_pdf, name='download_summary_pdf'),
    path('chatbot/',views.chatbot, name='chatbot'),

]
