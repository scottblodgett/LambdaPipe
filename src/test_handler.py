#python -m pip install requests
#python -m pip install validators

import unittest
import index
import json

class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("Testing response.")

        event = { "url": "https://click.mlsend.com/link/c/YT0xNTI5MjIwMjA4NTA4NTQwNDQ3JmM9azFqNyZlPTE5MjgmYj00MjgwMzE1ODAmZD1oNnMzcjNx.uV-jk5YH6UIg-x6bcetpj_Kp5u0vn38QNBHbZns5PLQ" }
        result = index.url_handler(event, None)
        #result = json.loads(index.url_handler(event, None))
        #print(result["statusCode"])
        #print(result)
        #result = json.dumps(result)

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')

        event = { "url": "www.yahoo.com" }
        result = index.url_handler(event, None)
        #print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        
        event = { "url": "" }
        result = index.url_handler(event, None)
        #print(result)
        self.assertEqual(result['statusCode'], 400)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
      
        event = { "url": "blah" }
        result = index.url_handler(event, None)
        self.assertEqual(result['statusCode'], 400)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        
        print("Unit test complete.")

if __name__ == '__main__':
    unittest.main()