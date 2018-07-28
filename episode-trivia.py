import decimal
import os
import random
import re
import subprocess

EPISODES_PATH = '/home/adelfino/Desktop/Dropbox/videos/series/the_simpsons'
#EPISODES_PATH = r'C:\Users\adelfino\Desktop\Personal\the_simpsons'

OPTIONS_TO_SHOW = 3
CLIP_DURATION = 10
MARGIN = 60

decimal.getcontext().prec = 6

def get_video_duration(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams',
                             'v:0', '-show_entries', 'stream=duration', '-of',
                             'default=noprint_wrappers=1:nokey=1', path],
                             capture_output=True)

    return decimal.Decimal(str(result.stdout, encoding='utf-8').rstrip())

def play_video_clip(path, start, duration):
    subprocess.run(['vlc',  '--no-video-title-show',
                    '--meta-title=NO CHEATING', '--play-and-exit',
                    f'--run-time={duration}', f'--start-time={start}',
                    '--fullscreen', path], stderr=subprocess.DEVNULL)

players = {}
seasons = {}

exclusion_list = [
    'S02E03',
    'S03E07',
    'S04E05',
    'S05E05',
    'S06E06',
    'S07E06',
    'S08E01',

    'S04E18',
    'S06E03',
    'S06E25',
    'S07E01',
    'S07E10',
    'S07E21',
    'S08E24',
]

for filename in os.listdir(EPISODES_PATH):
    if all(map(lambda episode: episode not in filename, exclusion_list)):
        season = re.search('S([0-9]{2})E[0-9]{2}', filename).group(1)
        season = int(season.lstrip('0'))

        filepath = os.path.join(EPISODES_PATH, filename)
        duration = get_video_duration(filepath)

        seasons.setdefault(season, list()).append([filepath, duration])

seasons_len = len(seasons)

while True:
    player_name = input('Player: ')

    if not player_name:
        break

    if player_name in players:
        print('Two players cannot have the same name.')
        continue

    players[player_name] = 0

print()

while True:
    try:
        rounds = int(input('Rounds: '))
        break
    except ValueError:
        pass

print()

for round in range(1, rounds + 1):
    print(f'Round {round} of {rounds}')

    for player in players:
        print(f'Your turn, {player}! Press Enter when ready')
        input()

        season = random.randint(1, seasons_len)

        selected_episodes = random.sample(seasons[season], OPTIONS_TO_SHOW)
        chosen_episode = random.choice(selected_episodes)

        play_video_clip(chosen_episode[0], chosen_episode[1] / 6 + random.randint(-MARGIN, MARGIN), CLIP_DURATION)

        for choice in selected_episodes:
            play_video_clip(choice[0], choice[1] - choice[1] / 6 + random.randint(-MARGIN, MARGIN), CLIP_DURATION)

        while True:
            choice = input('Choice: ')

            try:
                choice = int(choice)
            except ValueError:
                pass
            else:
                if 1 <= choice <= OPTIONS_TO_SHOW:
                    break

        if selected_episodes[choice - 1] == chosen_episode:
            players[player] += 1

print()

if len(players) > 1:
    maximum_score = max(players.values())

    if maximum_score == 0:
        print('We have a bunch of losers!')
    else:
        players = sorted(players.items(), key=lambda item: item[1], reverse=True)
        winners = []

        for player, score in players.items():
            if score < maximum_score:
                break

            winners.append(player)

        if len(winners) == 1:
            print('We have a winner!')
            print(f'Congratulations, {winners[0]}! 🥇🏆🎺🎆')
        else:
            print('We have a draw!')

            for winner in winners:
                print(f'Well done, {winner}!')

    print()

    for player, score in players.items():
        print(player, score, sep=': ')
else:
    print('You scored', players.popitem()[1], sep=': ')

input()