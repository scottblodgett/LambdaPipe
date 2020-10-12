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

    data = {}
    data["url"] = url.scheme + "//" + url.path[0:]
    data["statusCode"] = status_code
    data["qs"] = dict(parse_qsl(url.query))
    data["headers"] = headers

    #print(data)
    return (json.dumps(data))


def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url

print('Loading function')

def url_handler(event, context):
    try:
        #print("Log stream name:", context.log_stream_name)
        #print("Log group name:",  context.log_group_name)
        #print("Request ID:",context.aws_request_id)
        #print("Mem. limits(MB):", context.memory_limit_in_mb)
        #url1 = event["queryStringParameters"]["url1"]
        if 'url' in event:
            url = event["url"]
        else:
            return response({'message': 'No URL specified' }, 400)
            
        #print(url)    
        if len(url) > 0:
            url = formaturl(url)
        else:
            return response({'message': 'No URL specified' }, 400)
            
        if not validators.url(url):
            return response({'message': 'Invalid url' }, 400)

        r = requests.get(url, allow_redirects=False)
        output = (r.headers['Location'])
        return response({'message': output }, 200)
    except Exception as e:
        return response({'message': e.message}, 400)