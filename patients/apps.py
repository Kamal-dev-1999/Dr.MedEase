from django.apps import AppConfig

class PatientsConfig(AppConfig):
    name = 'patients'
    verbose_name = 'Patients'

    def ready(self):
        """
        The `ready` method is called when the app is ready. It is used to connect signals.
        """
        import patients.signals  # Import signals to register them when the app is ready
