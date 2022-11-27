import os
import jwt
import random
import string
from datetime import datetime, timedelta, timezone
from .http_code import HTTP_200_OK, HTTP_201_CREATED


def generate_response(data=None, message=None, status=400):

    if status == HTTP_200_OK or status == HTTP_201_CREATED:
        status_bool = True
    else:
        status_bool = False

    return {
        "data": data,
        "message": modify_slz_error(message, status_bool),
        "status": status_bool,
    }, status


def modify_slz_error(message, status):

    final_error = list()
    if message:
        if type(message) == str:
            if not status:
                final_error.append({"error": message})
            else:
                final_error = message
        elif type(message) == list:
            final_error = message
        else:
            for key, value in message.items():
                final_error.append({"error": str(key) + ": " + str(value[0])})
    else:
        final_error = None
    return final_error




def get_reference():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(16))
    return result_str

