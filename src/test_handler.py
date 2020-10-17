#python -m pip install requests
#python -m pip install validators

import unittest
import Index
import json

class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("Testing response.")

        url = { "url": "https://click.mlsend.com/link/c/YT0xNTI5MjIwMjA4NTA4NTQwNDQ3JmM9azFqNyZlPTE5MjgmYj00MjgwMzE1ODAmZD1oNnMzcjNx.uV-jk5YH6UIg-x6bcetpj_Kp5u0vn38QNBHbZns5PLQ" }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        #result = json.loads(index.url_handler(event, None))
        #print(result["statusCode"])
        #result = json.dumps(result)
        #print(json.dumps(result))

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')

        url = { "url": "www.yahoo.com" }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        #print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        
        url = { "url": None }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        #print(result)
        self.assertEqual(result['statusCode'], 400)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
      
        url = { "url": "blah" }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        self.assertEqual(result['statusCode'], 400)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
         
        print("Unit test complete.")

if __name__ == '__main__':
    unittest.main()
