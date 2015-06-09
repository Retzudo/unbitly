import unbitly
import unittest
import json


def get_url(response):
    try:
        data = response.data.decode('utf-8')
        return json.loads(data).get('url')
    except ValueError:
        return None


def get_json(url):
    return json.dumps({
        'url': url
    })


class TestCase(unittest.TestCase):
    def setUp(self):
        self.client = unbitly.app.test_client()

    def test_index(self):
        """Test if the main page works."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_bitly(self):
        """Test various combinations of URLs to decode."""
        # http://bit.ly/ItaROu points to duckduckgo.com
        url = unbitly.follow_bitly('http://bit.ly/ItaROu')
        self.assertEqual(url, 'https://duckduckgo.com/')

        github = 'https://github.com/'
        url = unbitly.follow_bitly(github)
        self.assertEqual(url, github)

        url = unbitly.follow_bitly('http://bit.ly/unbitly-fake-test-url')
        self.assertIsNone(url)

        url = unbitly.follow_bitly('something')
        self.assertIsNone(url)

        url = unbitly.follow_bitly(1234)
        self.assertIsNone(url)

    def test_follow(self):
        response = self.client.post(
            '/follow',
            data=get_json('http://bit.ly/ItaROu'),
            content_type='application/json'
        )
        self.assertEqual(get_url(response), 'https://duckduckgo.com/')

        response = self.client.post(
            '/follow',
            data=get_json('https://github.com/'),
            content_type='application/json'
        )
        self.assertEqual(get_url(response), 'https://github.com/')

        response = self.client.post(
            '/follow',
            data=get_json('http://bit.ly/unbitly-fake-test-url'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            '/follow',
            data=get_json('something'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            '/follow',
            data=get_json(1234),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
