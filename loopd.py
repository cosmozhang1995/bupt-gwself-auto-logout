import sys, os 
import client as cli
import datetime
import time
import config

f = open("./log", "a")

def writeLog(msg):
    content = ""
    if msg == "\n":
        content = "\n"
    else:
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        content = "[" + t + "] " + msg + "\n"
    f.write(content)
    f.flush()

def main():
    while True:
        cookies = None
        loginSuccess = False
        writeLog("Log in...")
        while not loginSuccess:
            try:
                cookies = cli.login(config)
                loginSuccess = True
            except:
                writeLog("Login failed. Retry in " + str(config.retryDelay) + " seconds...")
                time.sleep(config.retryDelay)
        writeLog("Log in ok!")
        while True:
            writeLog("Start a scan...")
            try:
                cli.ipLogout(cookies, config)
            except:
                break
            time.sleep(config.interval)
        # writeLog("==============================================")

if __name__ == "__main__":  
    # do the UNIX double-fork magic, see Stevens' "Advanced   
    # Programming in the UNIX Environment" for details (ISBN 0201563177)  
    pid = None
    try:   
        pid = os.fork()   
        if pid > 0:  
            # exit first parent  
            sys.exit(0)   
    except OSError, e:   
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)   
        sys.exit(1)  
    # decouple from parent environment  
    os.chdir("/")   
    os.setsid()   
    os.umask(0)   
    # do second fork  
    try:   
        pid = os.fork()   
        if pid > 0:  
            # exit from second parent, print eventual PID before  
            print "Daemon PID %d" % pid   
            writeLog("\n") 
            writeLog("Daemon start at PID: %d" % pid) 
            sys.exit(0)   
    except OSError, e:   
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)   
        sys.exit(1)   
    # start the daemon main loop 
    main()