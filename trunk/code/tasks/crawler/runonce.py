import os, sys

def quitIfDuplicate():
	scriptName = os.path.basename(sys.argv[0])

	processes = os.popen('ps ax')

	scriptCount = 0
	for processLine in processes:
		if(processLine.count('python') > 0 and processLine.count(scriptName) > 0):
			scriptCount = scriptCount + 1


	if(scriptCount > 1):
		print "Script is already running, but requested to run only once."
		quit()
