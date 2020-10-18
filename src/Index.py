# pip install requests -t ./
import requests, json
import re
import validators
from urllib.parse import urlparse, parse_qsl

def response(msg, status_code):

    url = urlparse(msg["message"])

    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Access-Control-Allow-Origin"] = "*"

    body = {}
    body["url"] = url.scheme + "://" + url.netloc + "/"+ url.path
    body["qs"] = dict(parse_qsl(url.query))
    
    return {
        "statusCode": status_code,
        "isBase64Encoded" : False,
        "headers" : headers,
        "body": json.dumps(body)
    }

def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url


def url_handler(event, context):
    #print('starting now')
    
    try:
        #print("Log stream name:", context.log_stream_name)
        #print("Log group name:",  context.log_group_name)
        #print("Request ID:",context.aws_request_id)
        #print("Mem. limits(MB):", context.memory_limit_in_mb)
        #url1 = event["queryStringParameters"]["url1"]

        qs = event.get('queryStringParameters', None)
        #url = "https://click.mlsend.com/link/c/YT0xNTI5MjIwMjA4NTA4NTQwNDQ3JmM9azFqNyZlPTE5MjgmYj00MjgwMzE1ODAmZD1oNnMzcjNx.uV-jk5YH6UIg-x6bcetpj_Kp5u0vn38QNBHbZns5PLQ"
        if qs is not None and (qs.get('url', None) is not None):
            url = event["queryStringParameters"]["url"]
        else:
            output = response({'message':  'No URL specified' }, 400)
            return (output)
            
        if len(url) > 0:
            url = formaturl(url)
        else:
            return response({'message':  'No URL specified' }, 400)
        
        if not validators.url(url):
            return response({'message':  'Bad Url' }, 400)

        r = requests.get(url, allow_redirects=False)
        output = (r.headers['Location'])
        output = response({'message':  output }, 200)
        return (output)

    except Exception as e:
        json.loads(response({'message': e.message}, 400))
