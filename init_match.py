def get_max_venues(num_teams):
    return int(num_teams/2)

def get_venues_slots(games):
    venue = 0
    slot = 0
    for game in games:
        slot = max(slot, game.get("slot_id", 0))
        venue = max(venue, game.get("venue_id", 0))
    return (venue, slot)

def print_schedule_summary(num_teams, schedule):
    (venues, slots) = get_venues_slots(schedule)
    # print venues, slots

    each_line = "{:20}"+"{:10}"*slots
    summary = []
    for i in range(num_teams):
        summary.append(['-']*slots)

    team_names = ['']*num_teams
    for game in games:
        slot = game["slot_id"] - 1
        team1 = game["teams"][0]["team_id"] - 1
        team2 = game["teams"][1]["team_id"] - 1
        team_names[team1] = game["teams"][0]["team_name"]
        team_names[team2] = game["teams"][1]["team_name"]
        summary[team1][slot] = game["venue_name"]
        summary[team2][slot] = game["venue_name"]

    print each_line.format('', *["slot" + str(i+1) for i in range(slots)])
    for i in range(len(summary)):
        line = summary[i]
        print each_line.format(team_names[i], *line)

def print_schedule_summary2(num_teams, schedule):
    (venues, slots) = get_venues_slots(schedule)
    each_line = "{:20}" + "{:30}" * venues
    summary = []
    for i in range(slots):
        summary.append(['-']*venues)

    for i in range(len(schedule)):
        game = schedule[i]
        vid = game["venue_id"] - 1
        sid = game["slot_id"] - 1
        summary[sid][vid] = game["teams"][0]["team_name"] + " vs " + game["teams"][1]["team_name"]

    print each_line.format('', *["venue" + str(i+1) for i in range(venues)])
    for i in range(len(summary)):
        print each_line.format('slot' + str(i+1), *summary[i])

# schedule is array of venues
# each venue is an array of games
# each game is an array with 2 elements, the 2 teams
def create_schedule(num_teams, games, num_venues):
    max_venues = get_max_venues(num_teams)
    if num_venues > max_venues: num_venues = max_venues

    # adding venue and slot info to the existing games object
    for i in range(len(games)):
        venue = i % num_venues
        slot = int(i / num_venues)
        games[i]["venue_id"] = venue + 1
        games[i]["venue_name"] = "venue{}".format(venue + 1)
        games[i]["slot_id"] = slot + 1
        games[i]["slot_name"] = "slot{}".format(slot + 1)

# games will be an array of arrays
# each element array will contain 2 elements, the 2 teams
def create_games(num_teams, teams):
    games = []
    counter = 0
    rounds = num_teams - 1
    if num_teams % 2 == 1:
        rounds += 1
        teams.append({"team_id": num_teams+1, "team_name": "dummy"})
    # print rounds
    # print teams
    total_teams = len(teams)
    for i in range(rounds):
        # print teams
        for j in range(total_teams/2):
            team1 = teams[j]
            team2 = teams[total_teams-1-j]
            if team1["team_name"] != 'dummy' and team2["team_name"] != 'dummy':
                counter += 1
                games.append({"game_id": counter, "teams": [teams[j], teams[total_teams-1-j]]})
        teams.insert(1, teams.pop(total_teams-1))
    # print games
    # print "number of games: %d" %(len(games), )
    return games

def create_teams(num_teams):
    return [{"team_id": i+1, "team_name": "team{}".format(i+1)} for i in range(num_teams)]

def create_match(num_teams, num_venues = 1):
    teams = create_teams(num_teams)
    games = create_games(num_teams, teams)
    create_schedule(num_teams, games, num_venues)
    return (teams, games)

if __name__ == "__main__":
    num_teams = 4
    num_venues = 2
    (teams, games) = create_match(num_teams, num_venues)
    import json
    # print json.dumps(teams, indent = 2)
    # print json.dumps(games, indent = 2)
    # print json.dumps(games, indent = 2)
    print_schedule_summary(num_teams, games)
    print
    print_schedule_summary2(num_teams, games)

    create_schedule(num_teams, games, 1)
    # print json.dumps(games, indent = 2)
    print
    print
    print_schedule_summary(num_teams, games)
    print
    print_schedule_summary2(num_teams, games)
    # verify(7, games)
    # print
    # create_games(2)
