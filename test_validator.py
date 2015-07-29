import datetime
import mock
import unittest

from unittest.mock import MagicMock, Mock

from mongo import ValidatorTable
import validator as v

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


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.validator = ValidatorTable()
        self._client = self.validator.client
        self.posts = self.validator.db.posts
        self.old = 'test'
        self.new = 'test'
        self.resp = '200'
        self.posts_count = 10
        self._populate_test_posts()

    def _populate_test_posts(self):
        for x in range(self.posts_count):
            self.validator.insert_log(self.old + str(x), self.resp)

    def tearDown(self):
        self.posts.delete_many({'request': self.old})
        self._client.close()
    
    def test_make_mock_requests(self):
        result = v.make_mock_requests()
        self.assertIsNotNone(result)
        self.assertEqual(self.posts_count, len(result))
    
    def test_compare_responses(self):
        result = v.compare_responses(self.new, self.old)
        self.assertTrue(result)
        result2 = v.compare_responses(self.new, 'something else')
        self.assertFalse(result2)

    def test_mock_request(self):
        pass

if __name__ == '__main__':
    unittest.main()
