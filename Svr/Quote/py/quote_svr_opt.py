#!/usr/bin/python
#############################################
# quote server for options
#############################################
from quote_svr import * 

if __name__ == "__main__":
	try: 
		svr = QuoteSvr(quotes = "OPTIONS")
		svr.run()
	except KeyboardInterrupt:
		sys.exit(0)
