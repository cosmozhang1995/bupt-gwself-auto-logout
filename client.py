import hashlib, requests, re, random
from pyquery import PyQuery as pq
import util


headers = {
	"Cache-Control": "max-age=0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Origin": "http://gwself.bupt.edu.cn",
	"X-FirePHP-Version": "0.0.6",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
	"Content-Type": "application/x-www-form-urlencoded",
	# "Referer": "http://gwself.bupt.edu.cn/nav_login",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6",
	"Connection": "keep-alive"
}

def login(config):
	# Fetch nav_login
	res = requests.get("http://gwself.bupt.edu.cn/nav_login", headers = headers)
	cookies = dict(JSESSIONID = res.cookies['JSESSIONID'])
	reg = re.compile(r"var\scheckcode\s?\=\s?\"?(\d+)\"?")
	match = reg.search(res.text)
	if match is None: raise Exception("Login Failed: Cannot find checkcode")
	checkcode = match.group(1)
	if checkcode is None: raise Exception("Login Failed: Cannot find checkcode")

	randomNum = random.random()
	# Send random
	requests.get("http://gwself.bupt.edu.cn/RandomCodeAction.action?randomNum=" + str(randomNum), cookies = cookies, headers = headers)

	# Do login
	md5 = hashlib.md5()
	md5.update(config.password.encode())
	password = md5.hexdigest()
	loginData = {
		"account": config.account,
		"password": password,
		"code": "",
		"checkcode": checkcode,
		"Submit": "Login"
	}
	res = requests.post("http://gwself.bupt.edu.cn/LoginAction.action", data = loginData, cookies = cookies, headers = headers)
	if res.text.find("checkcode1") < 0: raise Exception("Login failed: Remote refused")

	return cookies

def ipLogout(cookies, config):
	res = requests.get("http://gwself.bupt.edu.cn/nav_offLine", headers = headers, cookies = cookies)
	d = pq(res.text)
	tbody = d('#Maint1')
	if len(tbody) == 0:
		raise Exception("Cannot open offline page")
	trs = d('tr')
	trs.pop(0)
	for tr in trs:
		tds = pq(tr)('td')
		ipAddr = re.sub('&\w+;', '', pq(tds[0]).text());
		fldsessionid = re.sub('&\w+;', '', pq(tds[3]).text());
		if util.formatIPv4Addr(ipAddr) in config.rejectedList:
			try:
				res = requests.get("http://gwself.bupt.edu.cn/tooffline?t=" + str(random.random()) + "&fldsessionid=" + fldsessionid, headers = headers, cookies = cookies)
				res = res.json()
				if res["date"] != "success": raise Exception()
				print("SUCCESS logout: ", ipAddr)
			except Exception as e:
				print("ERROR   logout: ", ipAddr)
	return False