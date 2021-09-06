import datetime as dt
import random
import string
import threading

from rest_framework import status

from .models import Secret

STATUS_200 = status.HTTP_200_OK
STATUS_201 = status.HTTP_201_CREATED
STATUS_400 = status.HTTP_400_BAD_REQUEST
STATUS_403 = status.HTTP_403_FORBIDDEN
STATUS_404 = status.HTTP_404_NOT_FOUND


def generate_slug(size=20, chars=string.ascii_uppercase + string.digits):
    """Generation random slug for field lifetime"""
    return "".join(random.choice(chars) for _ in range(size))


def delete_an_entry():
    """The function of deleting expired secrets"""
    secret = Secret.objects.exclude(time_of_death__gte=dt.datetime.now())
    secret.delete()


thread1 = threading.Thread(target=delete_an_entry())
thread1.start()
threading.Timer(86400, delete_an_entry).start()
