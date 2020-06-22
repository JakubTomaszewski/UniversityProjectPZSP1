from http.server import HTTPServer, BaseHTTPRequestHandler
from sun_tracker import get_location_info, check_after_sunset, display_city_info, get_sun_info
from astral.geocoder import database
import datetime


notification = 'False'
is_connected = 'False'
should_break= 'False'

# Getting locational info
city = get_location_info(database(), 'Warsaw')

# Getting info about the sun today
sun = get_sun_info(city, datetime.date.today())

now = datetime.datetime.now()
hour_now = now.hour
hour_ss = sun['sunset'].hour
hour_sr = sun['sunrise'].hour
status = check_after_sunset(hour_sr, hour_ss, hour_now)
status = True


class Server(BaseHTTPRequestHandler):

    def do_GET(self):

        global notification, status, is_connected, should_break

        if self.path == '/':
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(open('index.html').read(), 'utf-8'))

        # LIGHT ON
        if self.path.endswith('/light_on'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Light on status page'.encode())

            # If after sunrise set notification to True
            if status:
                notification = 'True'

        # LIGHT OFF
        if self.path.endswith('/light_off'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Light off status page'.encode())
            notification = 'False'

        # SENDING NOTIFICATION
        if self.path.endswith('/notification'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            if self.headers['Wifi-Connected'] == 'true':
                is_connected = 'True'
            else:
                is_connected = 'False'
            self.wfile.write(notification.encode())

        # CHECK IF CONNECTED
        if self.path.endswith('/is_connected'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.send_header('is_connected', is_connected)
            self.end_headers()
            #self.wfile.write(is_connected.encode())

        if self.path.endswith('/should_break'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.send_header('should_break', should_break)
            self.end_headers()

        if self.path.endswith('/stop'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            should_break = 'True'
            self.end_headers()


def run(server_class=HTTPServer, handler_class=Server):
    server_address = ('localhost', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
