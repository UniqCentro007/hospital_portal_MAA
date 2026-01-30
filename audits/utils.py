from .models import AuditLog

def log_action(user, action, request=None):
    ip = None
    if request:
        ip = request.META.get('REMOTE_ADDR')

    AuditLog.objects.create(
        user=user,
        action=action,
        ip_address=ip
    )
