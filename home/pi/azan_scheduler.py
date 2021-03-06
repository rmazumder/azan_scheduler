import schedule
import time
import json
import os
import logging

from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

logFile = '/tmp/azan_scheduler_log.log'

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)


def fazr():
    app_log.info("Running fazr ")
    os.system("mocp -v 100 --playit /home/pi/azan1.mp3")

def duhr():
    app_log.info("Running Duhr ")
    os.system("mocp -v 100 --playit /home/pi/azan.mp3")

def asr():
    app_log.info("Runing asr")
    os.system("mocp -v 100 --playit /home/pi/azan.mp3")

def magrib():
    app_log.info("Running magrib ")
    os.system("mocp -v 100 --playit /home/pi/azan.mp3")

def isha():
    app_log.info("running isha ")
    os.system("mocp -v 100 --playit /home/pi/azan.mp3")


def updatejob():
    app_log.info("I'm am updating the scheduler ")
    schedule.clear("fazr")
    schedule.clear("isha")
    schedule.clear("duhr")
    schedule.clear("asr")
    schedule.clear("magrib")

    f = open("/home/pi/weather-server/namaztime.data", "r")
    fdata = f.read()
    data =  json.loads(fdata)
    fazrtime = data['data']['timings']['Fajr']
    duhrtime = data['data']['timings']['Dhuhr']
    asrtime = data['data']['timings']['Asr']
    magribtime = data['data']['timings']['Maghrib']
    ishatime = data['data']['timings']['Isha']


    schedule.every().day.at(fazrtime).do(fazr).tag("fazr")
    schedule.every().day.at(duhrtime).do(duhr).tag("duhr")
    schedule.every().day.at(asrtime).do(asr).tag("asr")
    schedule.every().day.at(magribtime).do(magrib).tag("magrib")
    schedule.every().day.at(ishatime).do(isha).tag("isha")    

def job():
    print("I'm working...")

updatejob();
schedule.every(2).hours.do(updatejob)
#schedule.every(10).seconds.do(job)


while True:
    app_log.info("--------------")
    app_log.info(schedule.jobs)

    app_log.info("--------------")
    schedule.run_pending()
    time.sleep(1)
