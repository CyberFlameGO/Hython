class PlayerNotFoundException(Exception):
    print('An error returned while trying to find that player >> player not found! ')


class GuildNotFoundException(Exception):
    print('An error returned while trying to find that guild >> guild not valid!')


class HypixelAPIException(Exception):
    print('API has caught an error, this is not due to Hypthon!')
