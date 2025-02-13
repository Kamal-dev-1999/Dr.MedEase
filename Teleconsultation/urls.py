from django.urls import path
from . import views

app_name = 'teleconsult'

urlpatterns = [
    path('', views.teleconsult_list, name='teleconsult_list'),  # List of teleconsultations
    path('<int:session_id>/', views.teleconsult_detail, name='teleconsult_detail'),  # Detail of a specific session
    path('start/<int:session_id>/', views.start_live_consultation, name='start_live_consultation'),  # Start live consultation
    path('video_call/', views.video_call, name='video_call'),  # Start a new video call
]
