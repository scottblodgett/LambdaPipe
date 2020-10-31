import unittest
import Index

class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("Testing response.")

        url = { "url": "https://reinvent.awsevents.com/?trk=em_a134p000006BlQmAAK&trkCampaign=AWS_reInvent_2020&sc_channel=em&sc_campaign=GLOBAL_STRAT_T1_reinvent_DG1_20201130&sc_medium=em_312010&sc_outcome=Strategic_Events&sc_content=AWS_Event" }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')

        url = { "url": "https://matrix.ntreis.net/Matrix/Public/Portal.aspx?p=DE-293744888-482&k=1676089Xb4DX&eml=c2Vhbi5yYXlAdXJiYW5sZWFzaW5nLmNvbQ==" }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        #print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        
        url = { "url": "https://click.convertkit-mail4.com/xmud9q4qrws6hkm6q7cg/e0hph7hnxx2g60c8/aHR0cHM6Ly9mcy5ibG9nLzIwMjAvMTAvd2h5LXJlYWQv" }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        #print(result) 
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')

        url = { "url": "https://click.mlsend.com/link/c/YT0xNTI5MjIwMjA4NTA4NTQwNDQ3JmM9azFqNyZlPTE5MjgmYj00MjgwMzE1ODAmZD1oNnMzcjNx.uV-jk5YH6UIg-x6bcetpj_Kp5u0vn38QNBHbZns5PLQ" }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')

        url = { "url": "www.yahoo.com" }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        
        url = { "url": None }
        qs = { "queryStringParameters" : url }
        result = Index.url_handler(qs, None)
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
