from flask import Flask, request
import os
import time
import random


app = Flask(__name__)
RNUMS = {}


@app.route("/")
def hi():
	return "Hi, world!"

@app.route("/reg")
def registration():
	args = request.args
	nums = list(range(10))
	while True:
		rnum = random.choices(nums, 6)
		if rnum not in RNUMS:
			RNUMS[rnum] = {}
			RNUMS[rnum]["com"] = []
			RNUMS[rnum]["ans"] = []
			if info in args:
				RNUMS[rnum]["info"] = info
			break
	return rnum
	
	
@app.route("/getrnums")
def gernums():
	return RNUMS
	

@app.route("/sendcommand")
def sendcommand():
	args = request.args
	rnum = args["rnum"]
	com = args["com"]
	RNUM[rnum]["com"].append(com)
	return 0
	

@app.route("/getcommand")
def getcommand():
	args = request.args
	rnum = args["rnum"]
	while True:
		if len(RNUM[rnum]["com"]) > 0:
			com = RNUM[rnum]["com"].pop(0)
			break
		time.sleep(0.1)
	return com


@app.route("/getanswer")
def getanswer():
	args = request.args
	rnum = args["rnum"]
	while True:
		if len(RNUM[rnum]["ans"]) > 0:
			ans = RNUM[rnum]["ans"].pop(0)
			break
		time.sleep(0.1)
	return ans


@app.route("/sendanswer")
def sendanswer():
	args = request.args
	rnum = args["rnum"]
	ans = args["ans"]
	RNUM[rnum]["ans"].append(ans)
	return 0
	

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
