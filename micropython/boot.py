from machine import Pin
from time import sleep
import network
import socket

# #####################
#    DEFINE   DATA    #
wifi_id = 'wifi_name'
password = 'wifi_password'
# ################### #
host = 'localhost' # or another IP address
port = 8080 # example port
# ################### #
# ################### #
led = Pin(4, Pin.OUT)  # LED control
dev = Pin(0, Pin.OUT)  # device control
sig = Pin(13, Pin.IN)  # light signal (read)
# ################### #


def blink(times=1, sleep_time=1):
    '''Uses LED to blink'''
    for i in range(0, times):
        led.on()
        sleep(0.4)
        led.off()
        sleep(0.2)
    if sleep_time:
        sleep(sleep_time)


def in_out():
    '''Blinks a few times to announce beginning/end of program run'''
    blink(3, 2)


def connect_wifi(wifi_id, password):
    '''Connects to wifi (ssid & password above)'''
    blink()
    connection = network.WLAN(network.STA_IF)
    if not connection.isconnected():
        blink(2)
        connection.active(True)
        connection.connect(wifi_id, password)
        if not connection.isconnected():
            blink(10)


def send_request(host, path, port):
    '''Returns formatted data got after GET request'''
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    formatted_data = str(s.recv(500), 'utf-8')
    s.close()
    return formatted_data


count = 0


def run():
    global count

    # inform that program started (LED)
    in_out()

    while True:
        # check if should run
        try:
            # connect to wifi
            connect_wifi(wifi_id, password)

            should_break = send_request(host, 'should_break', port)
            splitted = should_break.split(' ')
            should_break = splitted[-1].strip()

            if should_break == 'True':
                dev.off()
                break

            # check if it's light (calibrate module)
            light_on = True if sig.value() == 0 else False

            if light_on:
                send_request(host, 'light_on', port)
            else:
                send_request(host, 'light_off', port)

            # check if should gate should be closed
            gate_open = send_request(host, 'is_connected', port)
            splitted = gate_open.split(' ')
            gate_open = splitted[-1].strip()

            if gate_open == 'False':
                dev.off()
            else:
                dev.on()

            # wait a bit
            sleep(10)
            # inform that alive
            blink(1)

            count = 0
        except Exception as err:
            if count >= 50:
                print(err)
                print('serwer sie ...')
                dev.off()
                break
            else:
                sleep(10)
                count += 1
                blink()

    # program ends (LED informs)
    in_out()


run()
