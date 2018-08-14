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

    try:
        if requestType == 'player':
            uuid_type = 'uuid'
            uuid = kwargs['uuid']
            if len(uuid) <= 16:
                uuid_type = 'name'
    except e.JsonParsingException and e.PlayerNotFoundException:
        pass
