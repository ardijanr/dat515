# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import redis
import mysql.connector



hostName = "0.0.0.0"
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        user_connection = redis.Redis(host='redis', port=6379, username='default', password='', decode_responses=True)
        user_connection.ping()


        # mydb = mysql.connector.connect(
        # host="mysql",
        # user="root",
        # password=""
        # )

        # print(mydb) 

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("</body>HELLO WORLD</html>", "utf-8"))
        
        
    def get_DATA():
        pass

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")