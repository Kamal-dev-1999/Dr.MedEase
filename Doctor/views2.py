# View to display doctor details
class DoctorDetailAPIView(View):
    def get(self, request, doctor_id):
        doctor = DoctorProfile.objects.filter(id=doctor_id, user=request.user).first()  # Fetch the doctor's profile
        if not doctor:  # Check if the profile exists
            messages.error(request, "Doctor profile not found.")  # Show an error message
            return redirect('doctor-list-create')  # Redirect to the doctor list

        # Fetch related information (professional, work, additional)
        professional_info = ProfessionalInformation.objects.filter(doctor_account=doctor).first()
        work_info = WorkDetails.objects.filter(doctor_account=doctor).first()
        additional_info = AdditionalInformation.objects.filter(doctor_account=doctor).first()

        # Check if the profile is incomplete
        incomplete_profile = not all([
            doctor.first_name, doctor.last_name, doctor.contact_number, 
            professional_info and professional_info.specialization
        ])

        doctor_serializer = DoctorProfileSerializer(doctor)  # Serialize the doctor data

        return render(request, 'doctor/profile.html', {
            'doctor': doctor_serializer.data,  # Doctor's serialized data
            'professional_info': professional_info,  # Professional details
            'work_info': work_info,  # Work details
            'additional_info': additional_info,  # Additional information
            'form_mode': incomplete_profile,  # Flag for incomplete profile
            'serializer': doctor_serializer if incomplete_profile else None,  # Form serializer
        })

# API view to handle professional information
class ProfessionalInfoAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfessionalInformationSerializer  # Serializer for professional information
    template_name = 'doctor/professional_information_form.html'  # Path to the template

    def get_queryset(self):
        doctor_profile = DoctorProfile.objects.filter(user=self.request.user).first()  # Get logged-in user's profile
        if doctor_profile:
            return ProfessionalInformation.objects.filter(doctor_account=doctor_profile)  # Return related info
        return ProfessionalInformation.objects.none()  # Return empty if no profile

    def get(self, request, *args, **kwargs):
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()  # Fetch doctor's profile
        professional_info = ProfessionalInformation.objects.filter(doctor_account=doctor_profile).first()  # Fetch professional info
        serializer = self.get_serializer(professional_info) if professional_info else self.get_serializer()  # Serialize data
        return render(request, self.template_name, {
            'professional_info': serializer.data,  # Serialized data
            'doctor_id': doctor_profile.id if doctor_profile else None,  # Doctor ID
        })

    def post(self, request, *args, **kwargs):
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()  # Fetch doctor's profile
        if not doctor_profile:
            return Response({"error": "Doctor profile not found."}, status=status.HTTP_404_NOT_FOUND)  # Error if not found

        professional_info = ProfessionalInformation.objects.filter(doctor_account=doctor_profile).first()  # Fetch existing data
        serializer = self.get_serializer(professional_info, data=request.data) if professional_info else self.get_serializer(data=request.data)  # Create or update

        if serializer.is_valid():  # Validate data
            serializer.save(doctor_account=doctor_profile)  # Save data
            return redirect(reverse_lazy('Doctor:home'))  # Redirect to home page

        return render(request, self.template_name, {  # Render errors
            'professional_info': serializer.errors,
            'doctor_id': doctor_profile.id if doctor_profile else None,
            'serializer': serializer
        })


class WorkDetailsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = WorkDetailsSerializer
    template_name = 'doctor/work_details.html'

    def get_queryset(self):
        # Get the logged-in user's doctor profile
        doctor_profile = DoctorProfile.objects.filter(user=self.request.user).first()
        if doctor_profile:
            # Filter the work details based on the doctor's profile
            return WorkDetails.objects.filter(doctor_account=doctor_profile)
        # Return an empty queryset if no doctor profile is found
        return WorkDetails.objects.none()

    def get(self, request, *args, **kwargs):
        # Retrieve the doctor's profile for the logged-in user
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        
        if not doctor_profile:
            # Log and render a template with no work details if no profile is found
            print("No doctor profile found for user:", request.user)
            return render(request, self.template_name, {
                'work_info': None,
                'doctor_id': None,
            })

        # Log the retrieved doctor profile
        print("Doctor Profile found:", doctor_profile)

        # Check if work details exist for the doctor profile
        work_info = WorkDetails.objects.filter(doctor_account=doctor_profile).first()
        
        if work_info is None:
            # Log the absence of work details and create an empty serializer
            print("No work details found for doctor profile:", doctor_profile)
            serializer = self.get_serializer()
        else:
            # Log the presence of work details and serialize them
            print("Work details found:", work_info)
            serializer = self.get_serializer(work_info)

        # Log the serialized data for debugging
        print("Serializer data:", serializer.data)

        # Render the work details page with the serialized data
        return render(request, self.template_name, {
            'work_info': serializer.data,
            'doctor_id': doctor_profile.id if doctor_profile else None,
        })

    def post(self, request, *args, **kwargs):
        # Retrieve the doctor's profile for the logged-in user
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        if not doctor_profile:
            # Return an error response if no doctor profile is found
            print("Doctor profile not found for user:", request.user)
            return Response({"error": "Doctor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if work details already exist for the doctor profile
        work_info = WorkDetails.objects.filter(doctor_account=doctor_profile).first()
        
        if work_info:
            # Update the existing work details
            serializer = self.get_serializer(work_info, data=request.data)
        else:
            # Create new work details
            serializer = self.get_serializer(data=request.data)

        # Validate the serializer data
        if serializer.is_valid():
            # Save the data and associate it with the doctor profile
            serializer.save(doctor_account=doctor_profile)
            print("Work details saved successfully.")
            # Redirect to the doctor's home page
            return redirect(reverse_lazy('Doctor:home'))

        # Log validation errors for debugging
        print("Validation errors:", serializer.errors)

        # Re-render the form with errors and retain user input
        return render(request, self.template_name, {
            'work_info': serializer.errors,
            'doctor_id': doctor_profile.id,
            'serializer': serializer
        })


class AdditionalInformationAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = AdditionalInformationSerializer
    template_name = 'doctor/additional_information.html'

    def get_queryset(self):
        # Get the logged-in user's doctor profile
        doctor_profile = DoctorProfile.objects.filter(user=self.request.user).first()
        if doctor_profile:
            # Filter the additional information based on the doctor's profile
            return AdditionalInformation.objects.filter(doctor_account=doctor_profile)
        # Return an empty queryset if no doctor profile is found
        return AdditionalInformation.objects.none()

    def get(self, request, *args, **kwargs):
        # Retrieve the doctor's profile for the logged-in user
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        # Check if additional information exists for the doctor profile
        additional_info = AdditionalInformation.objects.filter(doctor_account=doctor_profile).first()

        if additional_info is None:
            # Create an empty serializer if no additional information is found
            serializer = self.get_serializer()
        else:
            # Serialize the existing additional information
            serializer = self.get_serializer(additional_info)

        # Render the additional information page with the serialized data
        return render(request, self.template_name, {
            'additional_info': serializer.data,
            'doctor_id': doctor_profile.id if doctor_profile else None,
        })

    def post(self, request, *args, **kwargs):
        # Retrieve the doctor's profile for the logged-in user
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        if not doctor_profile:
            # Return an error response if no doctor profile is found
            return Response({"error": "Doctor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if additional information already exists for the doctor profile
        additional_info = AdditionalInformation.objects.filter(doctor_account=doctor_profile).first()
        
        if additional_info:
            # Update the existing additional information
            serializer = self.get_serializer(additional_info, data=request.data)
        else:
            # Create new additional information
            serializer = self.get_serializer(data=request.data)

        # Validate the serializer data
        if serializer.is_valid():
            # Save the data and associate it with the doctor profile
            serializer.save(doctor_account=doctor_profile)
            messages.success(request, "Additional information saved successfully.")
            # Redirect to the doctor's home page
            return redirect('Doctor:home')

        # Log validation errors for debugging
        print(serializer.errors)

        # Re-render the form with errors and retain user input
        return render(request, self.template_name, {
            'additional_info': serializer.errors,
            'doctor_id': doctor_profile.id if doctor_profile else None,
            'serializer': serializer
        })


class SystemFieldsAPIView(generics.RetrieveUpdateAPIView):
    queryset = SystemFields.objects.all()
    serializer_class = SystemFieldsSerializer
