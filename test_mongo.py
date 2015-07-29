import datetime
import mock
import unittest

from unittest.mock import MagicMock, Mock

from mongo import ValidatorTable


# http://blog.xelnor.net/python-mocking-datetime/
real_datetime_class = datetime.datetime

def mock_datetime_now(target, dt):
    class DatetimeSubclassMeta(type):
        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_datetime_class)

    class BaseMockedDatetime(real_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

    # Python2 & Python3 compatible metaclass
    MockedDatetime = DatetimeSubclassMeta('datetime', (BaseMockedDatetime,), {})

    return mock.patch.object(dt, 'datetime', MockedDatetime)


class TestValidatorTable(unittest.TestCase):

    def setUp(self):
        self.validator = ValidatorTable()
        self._client = self.validator.client
        self.posts = self.validator.db.posts
        self.log_content = "test"
        self.resp = "200"
        self.tester = {'request': self.log_content}

    def tearDown(self):
        self.posts.delete_many(self.tester)
        self._client.close()
    
    def test_insert_log(self):
        target = datetime.datetime(2015, 1, 1)
        timestamp = target.strftime("%d %B %Y %I:%M:%S%p")
        with mock_datetime_now(target, datetime):
            pid = self.validator.insert_log(self.log_content, self.resp)

        new_obj = self.posts.find_one(pid)
        self.assertEqual(self.log_content, new_obj['request'])
        self.assertEqual(timestamp, new_obj['timestamp'])

        pid = self.validator.insert_log(self.log_content)
        self.assertIsNone(pid)


if __name__ == '__main__':
    unittest.main()
