import sqlite3
conn = sqlite3.connect("uandes.db")
curr = conn.cursor()


def create_table():
    curr.execute("""DROP TABLE IF EXISTS new_saf_tb""")
    curr.execute("""create table new_saf_tb(
                        id integer primary key autoincrement,
                        user_id integer,
                        course text,
                        title text,
                        tipo text)""")


    curr.execute("""DROP TABLE IF EXISTS unread_saf_tb""")
    curr.execute("""create table unread_saf_tb(
                    id integer primary key autoincrement,
                    user_id integer,
                    course text,
                    date text,
                    content text,
                    title text)""")

    curr.execute("""DROP TABLE IF EXISTS open_activities_saf_tb""")
    curr.execute("""create table open_activities_saf_tb(
                            id integer primary key autoincrement,
                            user_id integer,
                            course text,
                            date text,
                            title text)""")

    curr.execute("""DROP TABLE IF EXISTS current_semester_saf_tb""")
    curr.execute("""create table current_semester_saf_tb(
                                    id integer primary key autoincrement,
                                    user_id integer,
                                    course text)""")

    curr.execute("""DROP TABLE IF EXISTS users""")
    curr.execute("""create table users(
                                            id integer primary key autoincrement,
                                            chat_id text,
                                            name text,
                                            loggedInstagram bool,
                                            loggedSaf bool,
                                            loggedGmail bool,
                                            current_screen text,
                                            pos_instagram integer,
                                            saf_email text,
                                            saf_password text,
                                            gmail_email text,
                                            gmail_password text,
                                            intagram integer)""")


create_table()
