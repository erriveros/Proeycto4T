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
                        news text,
                        href text)""")
    def process_item(self, item, spider):
        self.store_db(item)
        print("Pipeline :" + item['news'][0])
        return item

    def store_db(self, item):
        self.curr.execute("""insert into unread_saf_tb values (?,?)""", (
            item['news'][0],
            item['href'][0]
        ))
        self.conn.commit()

