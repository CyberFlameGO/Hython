from exceptions import hypthon_exceptions as e
import constants as c
import grequests as g


class Handler:

    @staticmethod
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

        for u in all_url:
            requests = g.get(u)
            responses = g.imap(requests)

            for r in responses:
                response = r.json()
                if response['success'] is False:
                    raise e.HypixelAPIException
                if request_type == 'player':
                    if response['player'] is None:
                        raise e.PlayerNotFoundException
        try:
            return response[request_type]
        except e.HypixelAPIException:
            return response
