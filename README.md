Azan scheduler.

I wanted to have azan play everythime when it is time. 

Solution: raspberry pi to the rescue

- To play azan in mp3 format use mocp ( sudo apt-get install -y moc )
- run python code to get azan timing. I am runing this script every 2 hours to update the json file
    -http://api.aladhan.com/
    ```python
    ts = int(time.time())
    # adding one day to fix the offset of the api
    ts = ts +(24*60*60)
    response = requests.get("http://api.aladhan.com/v1/timings/"+str(ts)+"?latitude=37.3688&longitude=-122.0363&method=1&latitudeAdjustmentMethod=3")
    data = response.json()
    f=open("/home/pi/weather-server/namaztime.data", "w")
    f.write(json.dumps(data))
    f.close()
    ```
    
- Run python code azan_scheduler.py to read the json file created above and run mocp with azan mp3 file at the right time
- Create a init.d service for azan_scheduler and mocp
    - copy the azan_scheduler and mocp in /etc/init.d
    - sudo chmod +x /etc/init.d/azan_scheduler
    - sudo chmod +x /etc/init.d/mocp
    - sudo update-rc.d azan_scheduler defaults
    - sudo update-rc.d mocp defaults
    - sudo service azan_scheduler start
    - sudo service mocp start
