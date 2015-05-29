import client as cli
import time
import config

while True:
	print("\nLog in...")
	cookies = cli.login(config)
	print("Log in ok!")
	while True:
		print("\nStart a scan >")
		try:
			cli.ipLogout(cookies, config)
		except:
			break
		time.sleep(config.interval)
	print("\n==============================================")