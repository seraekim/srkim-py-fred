import unittest
from fred import api

# api 사용 방법


class MyTest(unittest.TestCase):

    def test_main(self):
        # cate id 입력
        res = api.get_cate(100)
        print(res)
        self.assertEqual(res['categories'], '100')
        # series_id 입력, 메타
        res = api.get_series_meta('2020RATIO011001')
        print(res)
        self.assertEqual(res['id'], 'fred_2020RATIO011001')

        # series_id 입력, observation
        print(api.get_series_observ('2020RATIO011001'))


if __name__ == '__main__':
    unittest.main()
