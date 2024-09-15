import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Article:


    dB = "lotus_website"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.header = data['header']
        self.body = data['body']
        self.thumbnail = data['thumbnail'].decode('utf-8') if isinstance(data['thumbnail'], bytes) else data['thumbnail']
        self.sources = [source.strip() for source in data['sources'].split(',')] if data['sources'] else []
        self.tags = [tag.strip() for tag in data['tags'].split(',')] if data['tags'] else []
        self.createdAt = datetime.strptime(data['createdAt'], '%Y-%m-%d %H:%M:%S') if 'createdAt' in data else None
        self.updatedAt = data['updatedAt']
        

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO articles (title, header, body, thumbnail, sources, tags) VALUES (%(title)s, %(header)s, %(body)s, %(thumbnail)s, %(sources)s,%(tags)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM articles;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM articles WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def update(cls, data):
        query = """
            UPDATE articles SET title = %(title)s, header = %(header)s, body = %(body)s, thumbnail = %(thumbnail)s, sources = %(sources)s, tags = %(tags)s
            WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        return result
    

