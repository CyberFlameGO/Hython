from exceptions import hypthon_exceptions as e
from json_handler import Handler as h


class Guild:
    """
    handles anything guild related
    """

    JSON = None
    guid = None

    def __init__(self, guid):
        """
        Basic guild setup, requires the guild ID
        :param guid:
        """
        try:
            if len(guid) == 24:
                self.guid = guid
                self.JSON = h.get_json_data('guild', guid)
        except e.HypixelAPIException:
            pass

    def get_guild_members(self):
        """
        Returns a list of guild members
        #TODO ADD PROPER SUPPORT FOR CUSTOM RANKS
        :return:
        """
        stock_roles = ['MEMBER', 'OFFICER', 'GUILDMASTER']
        member_dict = self.JSON['members']
        all = {}

        for role in stock_roles:
            all[role] = []