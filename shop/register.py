from django.contrib.auth import authenticate
from .models import UserProfile
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not UserProfile.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = UserProfile.objects.filter(email=email)
    
    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.getenv('SOCIAL_SECRET'))

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        user = UserProfile.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        print(email)
        print(os.environ.get('SOCIAL_SECRET'))
        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        print(new_user)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }