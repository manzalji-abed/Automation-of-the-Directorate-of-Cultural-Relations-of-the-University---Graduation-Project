from django.contrib.auth.models import User
from app.models import *

class CheckUser(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if User.objects.filter().count() == 0:
            user = User.objects.create_user(
                username='admin',
                first_name='admin',
                last_name='admin',
                password='admin',
                is_superuser= True,
                email=''
            )
            LastPull.objects.create(userId= user)
            UserSynchronization.objects.create(userId= user)
        response = self.get_response(request)

        return response

    
   