from init_match import *

def verify_games(num_teams, games):
    all_good = True
    message = ""
    total_games = (num_teams*(num_teams - 1))/2
    games_per_team = num_teams - 1
    game_dict = {}
    for game in games:
        team1_id = game["teams"][0]["team_id"]
        team2_id = game["teams"][1]["team_id"]
        if team1_id == team2_id:
            all_good = False
            message += "found a game with same teams %s and %s" %(game["teams"][0], game["teams"][1])
        game_dict[team1_id] = game_dict.get(team1_id, 0) + 1
        game_dict[team2_id] = game_dict.get(team2_id, 0) + 1
        # print game_dict
    # print "number of games: %d" %(len(games), )
    if len(games) != total_games:
        all_good = False
        message += "total games should be %d but found %d\n" %(total_games, len(games))
    for k, v in game_dict.items():
        if v != games_per_team:
            all_good = False
            message += "games for %s should be %d, but found %d\n" %(k, games_per_team, v)
    if all_good:
        print "all good"
    else:
        print "verification failed"
        print message

def verify_schedule(num_teams, schedule):
    all_games = schedule
    schedule = []
    temp = {}
    for game in all_games:
        venue = temp.get(game['venue_id'], [])
        venue.append(game)
        temp[game['venue_id']] = venue

    for k, v in temp.items():
        schedule.append({"venue": k, "games": v})

    all_good = True
    message = ""
    max_games = max([len(a["games"]) for a in schedule])
    for i in range(max_games):
        team_dict = {}
        games = []
        for j in range(len(schedule)):
            # getting all games
            if i < len(schedule[j]["games"]):
                games.append(schedule[j]["games"][i]["teams"])
        for game in games:
            for k in range(2):
                if team_dict.has_key(game[k]["team_id"]):
                    all_good = False
                    message += "Found overlapping game: %r" % (games)
                    break
                else:
                    team_dict[game[k]["team_id"]] = 1
            if not all_good:
                break
        if not all_good:
            break
    if all_good:
        print "all good"
    else:
        print "verification failed"
        print message

def verify_all(min_teams, max_teams):
    for i in range(min_teams, max_teams+1):
        games = create_games(i, create_teams(i))
        print "verifying games with %d teams" %(i, )
        verify_games(i, games)
        max_venues = get_max_venues(i)
        for j in range(1, max_venues+1):
            create_schedule(i, games, j)
            print "verifying schedule with %d venue(s)" %(j, )
            verify_schedule(i, games)

if __name__ == "__main__":
    verify_all(3, 10)
