from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DoctorProfile
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact_number = serializers.CharField(required=True)
    address = serializers.CharField(required=True)

    class Meta:
        model = User  # Use the default User model
        fields = (
            'email', 'username', 'first_name', 'last_name',
            'password', 'confirm_password', 'date_of_birth',
            'gender', 'contact_number', 'address'
        )

    def create(self, validated_data):
        # Extract profile data from validated data
        profile_data = {
            'date_of_birth': validated_data.pop('date_of_birth'),
            'gender': validated_data.pop('gender'),
            'contact_number': validated_data.pop('contact_number'),
            'address': validated_data.pop('address'),
        }

        # Remove password confirmation and get the password
        validated_data.pop('confirm_password')  # Remove password confirmation
        password = validated_data.pop('password')  # Get the password

        # Create the user
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()

        # Create the DoctorProfile instance with the additional data
        DoctorProfile.objects.create(user=user, **profile_data)

        return user

    def validate(self, attrs):
        # Validate that the passwords match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs





from rest_framework import serializers
from .models import DoctorProfile, ProfessionalInformation, WorkDetails, AdditionalInformation, SystemFields

# Doctor Profile Serializer
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = [
            'user', 'email', 'username', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'profile_picture',
            'contact_number', 'address'
        ]

# Professional Information Serializer
class ProfessionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalInformation
        fields = [
            'specialization', 'qualification',
            'years_of_experience', 'medical_license_number',
            'license_issuing_authority', 'license_expiry_date',
            'consultation_fee'
        ]

# Work Details Serializer
class WorkDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDetails
        fields = [
            'current_hospital', 'office_address',
            'consultation_hours', 'working_days', 'teleconsultation'
        ]

# Additional Information Serializer
class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInformation
        fields = [
            'languages_spoken', 'certifications',
            'achievements', 'bio', 'special_notes'
        ]

# System Fields Serializer
class SystemFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemFields
        fields = [
            'created_at', 'updated_at', 'is_active'
        ]
