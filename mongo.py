from pymongo import MongoClient
import datetime

class ValidatorTable():

    def __init__(self):
        self.client = MongoClient("0.0.0.0", 27017)
        self.db = self.client['validation']

    def insert_log(self, logObject):
        posts = self.db.posts
        timestamp = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p")
        old_log = posts.find_one({'log': logObject})
        if old_log is not None:    
            return posts.update_one(old_log, {'$set': {'log': logObject, 'timestamp': timestamp}}).upserted_id
        else:
            return posts.insert_one({'log': logObject, 'timestamp': timestamp}).inserted_id
    """"
    These functions are trivial and part of MongoClient, because remove is deprecated.

    def delete_one(self, logObject):
        posts = self.db.posts
        return posts.remove({'log': logObject})

    def delete_many(self, list_of_logs):
        posts = self.db.posts
        for log in list_of_logs:
            posts.remove({'log': log})
    """
    def get_log(self, logObject):
        posts = self.db.posts
        return posts.find_one({'log': logObject})

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

#    def insert_many_logs(self, list_of_logs):
#        posts = self.db.posts
#        result = posts.insert_many([{'log': i} for i in list_of_logs])
#        return result.inserted_ids

