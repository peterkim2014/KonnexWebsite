import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Blog:


    dB = "lotus_website"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.header = data['header']
        self.body = data['body']
        self.thumbnail = data['thumbnail']
        self.tags = data['tags']
        

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO blogs (title, header, body, thumbnail, tags) VALUES (%(title)s, %(header)s, %(body)s, %(thumbnail)s, %(tags)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM blogs;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM blogs WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def update(cls, data):
        query = """
            UPDATE blogs SET title = %(title)s, header = %(header)s, body = %(body)s, thumbnail = %(thumbnail)s, tags = %(tags)s
            WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        return result
    

