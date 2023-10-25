from django.contrib.auth import get_user

def auth_context(request):
    user = get_user(request)
    return {'authenticated': user.is_authenticated}