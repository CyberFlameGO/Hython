from exceptions import hypthon_exceptions as e
import constants as c
import grequests as g


def get_json_data(request_type, **kwargs):
    """
    handles getting data from the api
    :param request_type:
    :param kwargs:
    :return:
    """
    end = ''
    try:
        if request_type == 'key':
            key = kwargs['key']
    except e.JsonParsingException and e.InvalidAPIKeyException:
        pass

    try:
        if request_type == 'player':
            uuid_type = 'uuid'
            uuid = kwargs['uuid']
            if len(uuid) <= 16:
                uuid_type = 'name'
    except e.JsonParsingException and e.PlayerNotFoundException:
        pass

    for name, val in kwargs.items():
        if request_type == 'player' and name == 'uuid':
            name = uuid_type
        end = '&' + name + '=' + val
    all_url = c.API_URL + request_type + '?key=' + key + end
