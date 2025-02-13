from django.apps import AppConfig

class DoctorConfig(AppConfig):
    name = 'Doctor'
    verbose_name = 'Doctor'

    def ready(self):
        """
        The `ready` method is called when the app is ready. It is used to connect signals.
        """
        import Doctor.signals  # Import signals to register them when the app is ready
