from argparse import ArgumentParser
import requests
import time

parser = ArgumentParser()
parser.add_argument("--url")
args = parser.parse_args()
url = args.url


###Connect every 30 seconds for 120 seconds
time_end = time.time() + 120
while time.time() < time_end:
    for i in range(101):
        device = 'sensor' + str(i)
        r = requests.post(url, data = {'device':device})
        print(str(r.status_code) + r.text)
        time.sleep(0.5)
    time.sleep(30)

###Stop connecting for 120 seconds
time.sleep(120)

###Only half of devices connect for 120 seconds
time_end = time.time() + 120
while time.time() < time_end:
    for i in range(101):
        if i % 2 == 0:
            device = 'sensor' + str(i)
            r = requests.post(url, data = {'device':device})
            print(str(r.status_code) + r.text)
            time.sleep(0.5)
    time.sleep(30)

###Connect every 30 seconds for 120 seconds
time_end = time.time() + 120
while time.time() < time_end:
    for i in range(101):
        device = 'sensor' + str(i)
        r = requests.post(url, data = {'device':device})
        print(str(r.status_code) + r.text)
        time.sleep(0.5)
    time.sleep(30)
