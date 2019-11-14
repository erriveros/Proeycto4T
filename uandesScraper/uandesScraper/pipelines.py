# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class UandesscraperPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("uandes.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS unread_saf_tb""")
        self.curr.execute("""create table unread_saf_tb(
                        course text,
                        date text,
                        content text,
                        title text)""")

        self.curr.execute("""DROP TABLE IF EXISTS open_activities_saf_tb""")
        self.curr.execute("""create table open_activities_saf_tb(
                                course text,
                                date text,
                                title text)""")

        self.curr.execute("""DROP TABLE IF EXISTS current_semester_saf_tb""")
        self.curr.execute("""create table current_semester_saf_tb(
                                        course text)""")



    def process_item(self, item, spider):
        self.store_db(item)
        print("Pipeline :" + item['course'][0])
        return item

    def store_db(self, item):
        if item['table'] == 'unread':
            self.curr.execute("""insert into unread_saf_tb values (?,?,?,?)""", (
                item['course'][0],
                item['newsDate'][0],
                item['newsContent'],
                item['newsTitle'][0]
            ))

        elif item['table'] == 'open_activities':
            self.curr.execute("""insert into open_activities_saf_tb values (?,?,?)""", (
                item['course'],
                item['openActivityTitle'],
                item['openActivityDate']
            ))

        elif item['table'] == 'current_semester':
            self.curr.execute("""insert into current_semester_saf_tb values (?)""", (
                item['course'],
            ))
        self.conn.commit()

