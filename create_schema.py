import db

def create_schema():
    all_sqls = []

    matches_sql = """
    create table if not exists matches (
        id          integer primary key,
        name        text,
        create_date date default (datetime('now','localtime'))
    )
    """

    teams_sql = '''
    create table if not exists teams (
        match_id    integer,
        id          text,
        name        text,
        primary key (match_id, id)
    )
    '''

    games_sql = '''
    create table if not exists games (
        match_id    integer,
        id          text,
        team1_id    text,
        team2_id    text,
        team1_score integer default 0,
        team2_score integer default 0,
        primary key (match_id, id)
    )
    '''

    schedule_sql = '''
    create table if not exists schedule (
        match_id    integer,
        game_id     text,
        venue_id    text,
        venue_name  text,
        slot_id     text,
        slot_name   text,
        primary key (match_id, venue_id, game_id)
    )
    '''

    all_sqls.append(matches_sql)
    all_sqls.append(teams_sql)
    all_sqls.append(games_sql)
    all_sqls.append(schedule_sql)

    db.connect()
    db.excecute_all(all_sqls)
    db.close()

if __name__ == "__main__":
    create_schema()
