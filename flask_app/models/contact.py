import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Contact:


    dB = "lotus_website"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.subject = data['subject']
        self.email = data['email']
        self.body = data['body']
        



    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO contacts (name, subject, email, body, marketingID) VALUES (%(name)s, %(subject)s, %(email)s, %(body)s, %(marketingID)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM contacts;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM contacts WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def get_by_email(cls, email):
        query = """
            SELECT * FROM contacts WHERE email = %(email)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"email": email})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None
    

    @staticmethod
    def validate_inputs(data):
        errors = []

        # Validate first name
        if len(data['name']) < 2 or any(char.isdigit() for char in data['name']):
            errors.append("First name should be greater than 1 character and contain no numbers")

        # Validate email
        valid_domains = ['yahoo.com', 'gmail.com', 'hotmail.com', 'icloud.com', 'outlook.com']
        if '@' not in data['email'] or not any(domain in data['email'] for domain in valid_domains):
            errors.append("Invalid email format or domain")

        # Validate last name
        if len(data['body']) < 2:
            errors.append("Body should be filled.")

        return errors