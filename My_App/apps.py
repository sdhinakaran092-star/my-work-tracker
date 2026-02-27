from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'My_App'

    def ready(self):
        from django.contrib.auth.models import User
        try:
            if not User.objects.filter(username="dhina").exists():
                User.objects.create_superuser(
                    "dhina",              # your username
                    "dhinakaran092@gmail.com",    # your email
                    "Dhina@9585"          # your password
                )
        except:
            pass