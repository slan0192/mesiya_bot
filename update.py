#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

import os, sys
import subprocess
import psutil
import time
import cgi

#print("Content-type: text/html;\n")

def checkServerRunning():
	for p in psutil.process_iter():
		if "Python" in p.name() or "python" in p.name():
			if "server.py" in p.cmdline():
				return True
	return False
	
def runServer():
	if checkServerRunning() == False:
		pid = os.fork()
		if pid == 0:
			ndi = open(os.devnull, 'r')
			ndo = open(os.devnull, 'a+')
			nde = open(os.devnull, 'a+')
			os.dup2(ndi.fileno(), sys.stdin.fileno())
			os.dup2(ndo.fileno(), sys.stdout.fileno())
			os.dup2(nde.fileno(), sys.stderr.fileno())
			subprocess.run(['/Library/Frameworks/Python.framework/Versions/3.9/bin/python3', 'server.py'])
			exit()

def runClient(tp):
	pid = os.fork()
	if pid == 0:
		ndi = open(os.devnull, 'r')
		ndo = open(os.devnull, 'a+')
		nde = open(os.devnull, 'a+')
		os.dup2(ndi.fileno(), sys.stdin.fileno())
		os.dup2(ndo.fileno(), sys.stdout.fileno())
		os.dup2(nde.fileno(), sys.stderr.fileno())
		subprocess.run(['/Library/Frameworks/Python.framework/Versions/3.9/bin/python3', 'client.py', tp])
		exit()

runServer()	
form = cgi.FieldStorage()
tp = "meshiya"
if 'type' in form:
	tp = form.getvalue('type')	
runClient(tp)
time.sleep(1)

html = '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja-JP">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <link rel="stylesheet" href="main.css" type="text/css" />
  <script src="ws_client.js"></script>
  <title>Void</title>
</head>
<body>
  <h1 class="title">Void</h1>
  <div class="contents">
  	<div>Updating... Please wait for minutes!</div>
  	<pre id="status"></pre>
  </div>
  <script type="text/javascript">
  	init_ws("{tp}");
  </script>
</body>
</html>
'''.format(tp=tp)

#print("Content-type: text/html;\n")
print(html)
