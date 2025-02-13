from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TeleconsultationSession
from django.utils import timezone
import uuid
from django.conf import settings
import requests  # Make sure requests is installed using pip
def video_call(request):
    room_name = str(uuid.uuid4())  # Generate a unique room name

    # Get the API key from settings
    api_key = settings.VPAAS_API_KEY

    # Call the video service API using the API key
    video_api_url = "https://video-api-service-url.com/start"  # Example API endpoint
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    # Here we use the API to initiate a session (just as an example)
    response = requests.post(video_api_url, headers=headers, json={"roomName": room_name})

    # Check if the request was successful
    if response.status_code == 200:
        video_data = response.json()
        # Assuming the API returns data you need for the video call
        return render(request, 'video_call.html', {'room_name': room_name, 'video_data': video_data})
    else:
        return render(request, 'error.html', {'error': 'Unable to start video call.'})

@login_required
def teleconsult_list(request):
    """View to list all teleconsultations for the logged-in user"""
    sessions = TeleconsultationSession.objects.filter(patient=request.user).order_by('appointment_date')
    return render(request, 'teleconsult/teleconsult_list.html', {'sessions': sessions})

@login_required
def teleconsult_detail(request, session_id):
    """View to show details of a specific teleconsultation session"""
    session = get_object_or_404(TeleconsultationSession, id=session_id, patient=request.user)
    return render(request, 'teleconsult/teleconsult_detail.html', {'session': session})

@login_required
def start_live_consultation(request, session_id):
    """View to initiate a live video consultation"""
    session = get_object_or_404(TeleconsultationSession, id=session_id, patient=request.user)
    
    if session.status == 'upcoming' and session.appointment_date <= timezone.now():
        # Update session status to ongoing
        session.status = 'ongoing'
        session.save()
        
        # Generate a unique room name (using the session id or a UUID for uniqueness)
        room_name = str(uuid.uuid4())  # or use session.id for room name
        
        # Render the live consultation template with the session object and the room name
        return render(request, 'teleconsult/live_consultation.html', {
            'session': session,
            'room_name': room_name,  # Pass the room name for the meeting
            'is_doctor': request.user == session.doctor  # Determine if the user is the doctor
        })
    else:
        return redirect('teleconsult:teleconsult_list')
