class PlayerNotFoundException(Exception):
    print('An error returned while trying to find that player >> player not found! ')
    pass


class GuildNotFoundException(Exception):
    print('An error returned while trying to find that guild >> guild not valid!')
    pass


class HypixelAPIException(Exception):
    print('API has caught an error, this is not due to Hypthon!')
    pass


class InvalidAPIKeyException(Exception):
    print('Your API key is invalid, check it!')
    pass


class JsonParsingException(Exception):
    print('Error caught while attempting to parse JSON data from the API')
    pass
