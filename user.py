import uuid
from src.common.database import database


__author__ ='Sacnet'
class User(object):
    def __init__(self, password, _id=None):
        self.email = email
        self.password = password
        self._id=uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data=Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("user", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password==password
        return False
    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user= cls(email, password)
            new_user.save_to_mongo()
            session['email']=email
            return True
        else:
            return False
    def login(self):
        #login valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None
    def get_blogs(self):
        pass
    
    def json(self):
        return{
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }
    def save_to_mongo(self):
        Database.insert("user", self.json())
