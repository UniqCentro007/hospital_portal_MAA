from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import AuditLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action="User logged in",
        ip_address=request.META.get('REMOTE_ADDR')
    )
