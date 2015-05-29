def formatIPv4Addr(addr):
	segs = addr.split('.')
	if len(segs) != 4: return None
	formatted = []
	for seg in segs:
		seg = int(seg)
		try:
			formatted.append(str(int(seg)))
		except:
			return None
	return '.'.join(formatted)