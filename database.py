import psycopg2 # postgreSQL
import os # working with files (the DB file)
import datetime

db_connection = None
db_cursor = None

def init_db():
    global db_connection
    global db_cursor

    db_connection = psycopg2.connect( # postgreSQL connection info
        host="", # EDIT ME
        database="", # EDIT ME
        user="", # EDIT ME
        password="" # EDIT ME
        )
    db_cursor = db_connection.cursor()


    try:
        db_cursor.execute('''
            CREATE TABLE targets_messages
            (id integer GENERATED ALWAYS AS IDENTITY,
            message text,
            is_correct boolean,
            is_allowed boolean,
            spelling_mistakes_count integer,
            lang_probabilities text,
            time_unix integer)
            ''')  # TODO: maybe change the date to date type

    except psycopg2.errors.DuplicateTable:
        pass
    finally:
        db_connection.commit()

def execute_targets_messages_table_query(message: str, is_correct: bool, is_allowed: bool, spelling_mistakes_count: int, lang_probabilities: str, time_unix: int):
    global db_cursor
    db_cursor.execute('''
        INSERT
        INTO targets_messages
        (message, is_correct, is_allowed, spelling_mistakes_count, lang_probabilities, time_unix)
        VALUES(%s, %s, %s, %s, %s, %s)
        ''',
        (message, is_correct, is_allowed, spelling_mistakes_count, lang_probabilities, time_unix))

    db_connection.commit()

def last_incorrect_targets_message_was_not_so_long_ago():
    global db_connection, db_cursor
    threshold_in_sec = 30

    db_cursor = db_connection.cursor()

    db_cursor.execute('''
        SELECT *
        FROM targets_messages
        WHERE is_correct = false OR is_correct IS NULL
        ORDER BY time_unix
        DESC
        LIMIT 1
        ''')

    last_targets_incorrect_record = db_cursor.fetchone()

    if last_targets_incorrect_record == None:
        return False

    last_targets_incorrect_message_time_unix = last_targets_incorrect_record[-1]
    # TODO: look for a way to make accessing time_unix column index-independent
    # (like last_targets_incorrect_record["time_unix"])

    if int(datetime.datetime.now().timestamp()) - last_targets_incorrect_message_time_unix > threshold_in_sec: # TODO: find a better way to access time
        return False
    else:
        return True