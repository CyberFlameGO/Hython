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

    def get_player_info(self):
        """
        Returns with common data on the player in question
        :param self:
        :return:
        """
        JSON = self.JSON
        pi = {}
        pi['uuid'] = self.uuid
        pi['displayName'] = self.get_player_info(self)
        pi['rank'] = self.get_rank(self)
        pi['networkLevel'] = self.find_level(self)
        keys = ['karma', 'firstLogin', 'lastLogin', 'mcVersionRp', 'networkExp', 'socialMedia', 'prefix']
        for item in keys:
            try:
                pi[item] = JSON[item]
            except KeyError:
                print('Key error caught! aborting request!')
                pass
        return pi

    def get_player_name(self):
        """
        Converts a player uuid to a name
        """
        JSON = self.JSON
        return JSON['displayname']

    def find_level(self):
        JSON = self.JSON
        """
        #TODO CREATE SOMETHING TO HANDLE THE XP IN A 
        PROPER MANNER
        :return: 
        """
        try:
            net_xp = JSON['networkExp']
        except e.HypixelAPIException:
            net_xp = 0
            try:
                net_level = JSON['networkLevel']
            except e.HypixelAPIException:
                net_level = 0

    def get_rank(self):
        """
        brings in player ranks for package or monthly data
        :return rank:
        """
        JSON = self.JSON
        rank = {}
        locations = ['packageRank', 'rank', 'newPackageRank', 'monthlyPackageRank']

        for l in locations:
            if l in JSON:
                if JSON[l] == 'none' or 'NONE':
                    continue
                normal_rank = JSON[l].title()
                normal_rank = normal_rank.replace('_', ' ').replace('Mvp', 'MVP').replace('Vip', 'VIP').replace(
                    'Superstar', 'MVP++')  # who own earth names it superstar?!?!?!
                rank['rank'] = normal_rank.replace(' Plus', '+').replace('Youtuber', 'YouTube')

        if 'rank' not in rank:
            rank['rank'] = 'NON'

        return rank
