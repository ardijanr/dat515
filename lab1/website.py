# Python 3 server example
import time
import redis
import cgi

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

STARTING_BIT = "<body>"
FORM = """
<form method="post">
    <label for="key">Key:</label>
    <input type="text" id="key" name="key">
    <br><br>

    <label for="value">Value:</label>
    <input type="text" id="value" name="value">
    <br><br>

    <input type="submit" value="Submit">
</form>
"""

hostName = "0.0.0.0"
serverPort = 80

def redis_con():
    return redis.Redis(host='redis', port=6379, username='default', password='', decode_responses=True)

def get_html():
    redis_client = redis_con() 

    # Fetch all keys from Redis
    keys = redis_client.keys("*")

    html_list = "<ul>\n"
    for key in keys:
        html_list += f"<li>Key: {key}: Value: {redis_client.get(key)}</li>\n"
    
    return STARTING_BIT + FORM + html_list + "</body>"
    
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(get_html(), "utf-8"))


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)

        user_connection = redis_con()
        user_connection.set(parsed_data.get("key")[0], parsed_data.get("value")[0])

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(get_html(), "utf-8"))

                

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
