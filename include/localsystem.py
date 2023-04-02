import psutil
import subprocess

# Get disk usage (df)
def getDF():
    cmd = 'df -h | awk \'$NF=="/"{{printf "%d,%d,%s", $3,$2,$5}}\''
    output = subprocess.check_output(cmd, shell=True).decode("utf-8")
    values = output.split(',')
    return values

# Get CPU usage
def getCPU():
    return psutil.cpu_percent()

def getProcList():
    return {p.name(): p.info for p in psutil.process_iter(['pid','name'])}

def processIsRunning(pname=""):
    processes = getProcList()
    if processes.get(pname):
        return True
    else:
        return False