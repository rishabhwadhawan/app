from pymongo import MongoClient
import datetime

class ValidatorTable():

    def __init__(self):
        self.client = MongoClient("0.0.0.0", 27017)
        self.db = self.client['validation']

    def insert_log(self, request, response):
        posts = self.db.posts
        timestamp = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p")
        old_log = posts.find_one({'request': request})
        if old_log is not None:    
            return posts.update_one(old_log, {'$set': {'request': request, 'response': response, 'timestamp': timestamp}}).upserted_id
        else:
            return posts.insert_one({'request': request, 'response': response}).inserted_id

    def delete_one(self, request, response):
        posts = self.db.posts
        return posts.remove({'request': request, 'response': response})

    def get_log(self, request, response):
        posts = self.db.posts
        return posts.find_one({'request': request, 'response': response})

    def see_log(self):
        l = []
        cursor = self.db.posts.find()
        for i in range(cursor.count()):
            l.append(cursor[i])
        return l

    def __str__(self):
        cursor = self.db.posts.find()
        string = " "
        for i in range(cursor.count()):
            string += str(cursor[i]) + "\n"
        return string    
