from player import Player
from constants import Setter


def handle_setup(key):
    Setter.set_api_key(key)


def handle_player_test(uuid):
    uuid = 'should-replace-with-my-key'
    Player.uuid = uuid
    print(Player.find_level())
    print(Player.get_player_info())
    print(Player.get_rank())
    print(Player.JSON())