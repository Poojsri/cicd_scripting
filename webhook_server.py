from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['cicd']
webhooks_collection = db['webhooks']

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        # Parse GitHub event
        try:
            event = json.loads(body)
            print("Received event:", event['repository']['full_name'])

            # Store the event in MongoDB
            webhooks_collection.insert_one(event)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Webhook received and stored')
        except Exception as e:
            print("Error processing webhook:", e)
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON')

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting webhook server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()