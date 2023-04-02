from datetime import datetime
import subprocess

def getUptime(pretty=True):
    if PLATFORM == "linux" and pretty == True:
        cmd = 'uptime -p'
    elif PLATFORM == "darwin":
        cmd = "uptime | awk -F '[ ]' '{print $4,$5,$6,$7}'"
    elif pretty == False:
        cmd = "uptime"
    return subprocess.check_output(cmd, shell=True).decode("UTF-8").rstrip('\n,')

def getLocalTime(utc=False):
    if utc is True:
        localTime = datetime.utcnow()
    else:
        localTime = datetime.now()
    nowTime = localTime.strftime("%H:%M:%S")
    timeZone = localTime.astimezone().tzname()
    return (nowTime, timeZone)