from player import Player
from guild import Guild
from constants import Setter


def main():
    KEY = Setter.set_api_Key('REPLACE WITH YOUR KEY')
    player = Player.get_player_info('RapidTheNerd')
    print(player)
    level = Player.find_level('RapidTheNerd')
    print(level)
    rank = Player.get_rank('RapidTheNerd')
    guild = Guild.get_guild_members('GUILD ID')


if __name__ == '__main__':
    main()
