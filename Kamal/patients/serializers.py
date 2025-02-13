from rest_framework import serializers
from .models import Appointment
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PatientProfile

User = get_user_model()

class PatientSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact_number = serializers.CharField(required=True)
    address = serializers.CharField(required=True)

    class Meta:
        model = User  # Make sure this refers to the correct User model
        fields = (
            'email', 'username', 'first_name', 'last_name',
            'password', 'confirm_password', 'date_of_birth',
            'gender', 'contact_number', 'address'
        )

    def create(self, validated_data):
        # Extract profile-related data
        profile_data = {
            'date_of_birth': validated_data.pop('date_of_birth'),
            'gender': validated_data.pop('gender'),
            'contact_number': validated_data.pop('contact_number'),
            'address': validated_data.pop('address'),
        }

        # Remove password confirmation and extract password
        validated_data.pop('confirm_password')  
        password = validated_data.pop('password')

        # Create user instance
        user = User(**validated_data)
        user.set_password(password)
        user.is_patient = True  # Mark user as a patient
        user.save()

        # Create the PatientProfile instance
        PatientProfile.objects.create(user=user, email=user.email, username=user.username, **profile_data)


        return user

    def validate(self, attrs):
        # Validate password match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs



class PatientLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs


# class AppointmentSerializer(serializers.ModelSerializer):
#     patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)  # Get patient's full name
#     doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)  # Get doctor's full name

#     class Meta:
#         model = Appointment
#         fields = ['id', 'patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'symptoms', 'is_confirmed', 'patient', 'doctor']
#         read_only_fields = ['is_confirmed']  # Keep only `is_confirmed` as read-only

#     def create(self, validated_data):
#         """
#         Overriding the create method to enforce patient assignment.
#         """
#         request = self.context.get('request')
#         validated_data['patient'] = request.user.patient_profile
#         return super().create(validated_data)



class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'symptoms', 'is_confirmed']
        read_only_fields = ['is_confirmed']

    def create(self, validated_data):
        # Automatically set the patient from the request context
        request = self.context.get('request')
        validated_data['patient'] = request.user.patient_profile
        return super().create(validated_data)
