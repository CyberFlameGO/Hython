import constants as c
import random
from exceptions import hypthon_exceptions as e

def get_json_data(requestType, **kwargs):
    """
    handles getting data from the api
    :param requestType:
    :param kwargs:
    :return:
    """
    end = ''
    try:
        if requestType == 'key':
            key = kwargs['key']

    except e.JsonParsingException and e.InvalidAPIKeyException:
        pass
