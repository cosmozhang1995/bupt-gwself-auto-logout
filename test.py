import client as cli
import config

cookies = dict(JSESSIONID = "4DFB995ACC267B418469389742C29E7A")
# cookies = cli.login(config)
cli.ipLogout(cookies, config)