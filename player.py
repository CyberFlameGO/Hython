from json_handler import Handler as h
from exceptions import hypthon_exceptions as e


class Player:
    JSON = None
    uuid = ''

    def __init__(self, uuid):
        """
        called when a request is made to seach for a player by UUID
        :param uuid:
        """
        self.uuid = uuid

        if len(uuid) <= 16:
            self.JSON = h.get_json_data('player', uuid=uuid)
            JSON = self.JSON
            self.uuid = self.JSON['uuid']
        elif len(uuid) == 32 or len(uuid) == 36:
            self.JSON = h.get_json_data('player', uuid=uuid)
        else:
            raise e.PlayerNotFoundException
