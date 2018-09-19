from guild import Guild
from constants import Setter


def handle_setup(key):
    Setter.set_api_key(key)


def handle_player_test(uuid):
    uuid = 'should-replace-with-my-key'
    Guild.guid = uuid
    print(Guild.get_guild_members())
    print(Guild.JSON)
