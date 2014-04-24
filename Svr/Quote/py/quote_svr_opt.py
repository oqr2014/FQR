#!/usr/bin/python
#############################################
# quote server for options
#############################################
from quote_svr import * 

if __name__ == "__main__":
	try: 
		svr = QuoteSvr(PORT_=22086, MCAST_ADDR_="224.168.2.10", MCAST_PORT_=1601)
		svr.run()
	except KeyboardInterrupt:
		sys.exit(0)
