import client as cli
import time
import config

while True:
	cookies = None
	loginSuccess = False
	print("\nLog in...")
	while not loginSuccess:
		try:
			cookies = cli.login(config)
			loginSuccess = True
		except:
			print("Login failed. Retry in " + str(config.retryDelay) + " seconds...")
			time.sleep(config.retryDelay)
	print("Log in ok!")
	while True:
		print("\nStart a scan >")
		try:
			cli.ipLogout(cookies, config)
		except:
			break
		time.sleep(config.interval)
	print("\n==============================================")