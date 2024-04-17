import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Team:


    dB = "lotus_website"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone_type = data['phone_type']
        self.phone_number = data['phone_number']
        self.position = data['position']
        self.years_of_experience = data['years_of_experience']
        self.reason_for_apply = data['reason_for_apply']
        self.website = data['website']
        self.github = data['github']
        self.behance = data['behance']
        self.other = data['other']
        # self.document = data['document']



    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO teams (first_name, last_name, email, phone_type, phone_number, position, years_of_experience, reason_for_apply, website, github, behance, other) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_type)s, %(phone_number)s, %(position)s, %(years_of_experience)s, %(reason_for_apply)s, %(website)s, %(github)s, %(behance)s, %(other)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM teams;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM teams WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def get_by_email(cls, email):
        query = """
            SELECT * FROM teams WHERE email = %(email)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"email": email})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None