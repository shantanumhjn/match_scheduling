import init_match
import db
import json

def delete_match(match_id):
    db.connect()
    sqls = []
    sqls.append('delete from matches where id = ?')
    sqls.append('delete from teams where match_id = ?')
    sqls.append('delete from games where match_id = ?')
    sqls.append('delete from schedule where match_id = ?')
    for sql in sqls:
        db.execute(sql, (match_id, ))

    db.commit()
    db.close()

def fetch_match_ids(match_name, connect = True):
    sql = '''
        select id, name, create_date from matches where name = ?
    '''
    if connect: db.connect()
    rs = db.fetch(sql, (match_name, ))
    if connect: db.close()
    data = []
    for row in rs:
        match = {}
        match["id"] = row[0]
        match["name"] = row[1]
        match["create_date"] = row[2]
        data.append(match)
    return json.dumps(data)

def insert_teams(match_id, teams):
    sql = "insert into teams (match_id, id, name) values (?, ?, ?)"
    db.connect()
    for team in teams:
        db.execute(sql, (match_id, team["team_id"], team["team_name"]))
    db.commit()
    db.close()

def insert_games(match_id, games):
    sql = '''
        insert into games
            (match_id, id, team1_id, team2_id)
        values (?, ?, ?, ?)
    '''
    db.connect()
    for game in games:
        db.execute(sql, (match_id, game["game_id"], game["teams"][0]["team_id"], game["teams"][1]["team_id"]))
    db.commit()
    db.close()

def insert_schedule(match_id, schedule):
    sql = '''
        insert into schedule
            (match_id, game_id, venue_id, venue_name, slot_id, slot_name)
        values (?, ?, ?, ?, ?, ?)
    '''
    db.connect()

    for game in schedule:
        venue_id = game["venue_id"]
        venue_name = game["venue_name"]
        game_id = game["game_id"]
        slot_id = game["slot_id"]
        slot_name = game["slot_name"]
        db.execute(sql, (match_id, game_id, venue_id, venue_name, slot_id, slot_name))
    db.commit()
    db.close()

def insert_match(match_name):
    sql = '''
        insert into matches (name) values (?)
    '''
    db.connect()
    match_id = db.execute(sql, (match_name, ))
    db.commit()
    db.close()
    return match_id

def write_match_to_db(match_name, match):
    teams = match[0]
    games = match[1]
    match_id = insert_match(match_name)
    insert_teams(match_id, teams)
    insert_games(match_id, games)
    insert_schedule(match_id, games)
    print 'created match with id {}'.format(match_id)

def create_match(match_name, num_teams, num_venues = 1):
    match = init_match.create_match(num_teams, num_venues)
    write_match_to_db(match_name, match)

def del_all():
    sql = 'select id from matches'
    db.connect()
    rs = db.fetch(sql)
    db.close()
    for row in rs:
        delete_match(row[0])

if __name__ == "__main__":
    # delete_match(1)
    # matches = json.loads(fetch_match_ids('test1'))
    # print matches
    # for match in matches:
    #     delete_match(match["id"])
    # print fetch_match_ids('test1')
    del_all()
    create_match('test1', 6, 2)
