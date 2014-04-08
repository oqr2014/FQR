import socket
import time
import mcast

if __name__ == "__main__":
	mcast_cli = mcast.McastClient()
	mcast_cli.run()

