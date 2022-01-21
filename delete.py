# make a request to https://insiderunlocked.herokuapp.com/ every minute
import requests
import time 

while True:
    response = requests.get('https://insiderunlocked.herokuapp.com/')
    print("OK")
    time.sleep(20)