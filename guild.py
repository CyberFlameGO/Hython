from exceptions import hypthon_exceptions as e
from json_handler import Handler as h
import constants as c
import grequests as g


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
        :return all:
        """
        stock_roles = ['MEMBER', 'OFFICER', 'GUILDMASTER']
        member_dict = self.JSON['members']
        all = {}

        for role in stock_roles:
            all[role] = []

        total_urls = []
        order = []
        list = []

        for member in member_dict:
            order.append(member['rank'])
            total_urls.append(c.UUID_RESOLVER + member['uuid']['name'])

        for u in total_urls:
            requests = g.get(u)
            responses = g.map(requests)

            count = 0

            for index, user in enumerate(total_urls):
                try:
                   if user.startswith(c.UUID_RESOLVER):
                        total_urls[index] = responses[count].json()['name']
                        count += 1
                except AttributeError:
                    print('Attribute error caught, aborting request!')
                    pass

                for name in total_urls:
                    try:
                        member = {'role': order[count], 'name': name}
                    except KeyError:
                        member = {'role': order[count], 'name': 'Unknown rank!'}
                    list.append(member)
                    count += 1

                    for member in list:
                        list = all[member['role']]
                        list.append(member['name'])
        return all
