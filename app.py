import threading

from flask import Flask, request
import os
import time
import random

app = Flask(__name__)
RNUMS = {}


@app.route("/")
def hi():
    return "Hi, world!"


def timeoutkill(rnum):
    while True:
        if RNUMS[rnum]["type"] == "STAY":
            if time.time() - RNUMS[rnum]["timeout"] > 40:
                del RNUMS[rnum]
                break


@app.route("/reg")
def registration():
    args = request.args
    nums = list(map(str, range(10)))
    while True:
        rnum = str(int("".join(random.sample(nums, 4))))
        if rnum not in RNUMS:
            RNUMS[rnum] = {}
            RNUMS[rnum]["com"] = []
            RNUMS[rnum]["ans"] = []
            RNUMS[rnum]["timeout"] = time.time()
            RNUMS[rnum]["type"] = "STAY"
            th = threading.Thread(target=timeoutkill, args=(rnum, ))
            th.start()
            if "info" in args:
                RNUMS[rnum]["info"] = args["info"]
            break
    return rnum


def login(rnum):
    args = request.args
    if rnum not in RNUMS:
        RNUMS[rnum] = {}
        RNUMS[rnum]["com"] = []
        RNUMS[rnum]["ans"] = []
        RNUMS[rnum]["timeout"] = time.time()
        RNUMS[rnum]["type"] = "STAY"
        th = threading.Thread(target=timeoutkill, args=(rnum,))
        th.start()
        if "info" in args:
            RNUMS[rnum]["info"] = args["info"]


@app.route("/getrnums")
def getrnums():
    return RNUMS


@app.route("/gtrn")
def gtrn():
    res = []
    if RNUMS:
        for k, v in RNUMS.items():
            res.append(k)
        return str(res)
    return {}


@app.route("/sendcommand")
def sendcommand():
    args = request.args
    rnum = args["rnum"]
    com = args["com"]
    RNUMS[rnum]["com"].append(com)
    return "0"


@app.route("/getcommand")
def getcommand():
    args = request.args
    rnum = args["rnum"]
    if rnum not in RNUMS:
        login(rnum)
    RNUMS[rnum]["timeout"] = time.time()
    while True:
        if len(RNUMS[rnum]["com"]) > 0:
            com = RNUMS[rnum]["com"].pop(0)
            RNUMS[rnum]["type"] = "WORK"
            break
        time.sleep(0.1)
    return com


@app.route("/getanswer")
def getanswer():
    args = request.args
    rnum = args["rnum"]
    while True:
        if len(RNUMS[rnum]["ans"]) > 0:
            ans = RNUMS[rnum]["ans"].pop(0)
            break
        time.sleep(0.1)
    return ans


@app.route("/sendanswer")
def sendanswer():
    args = request.args
    rnum = args["rnum"]
    ans = args["ans"]
    RNUMS[rnum]["ans"].append(ans)
    RNUMS[rnum]["type"] = "STAY"
    return "0"


@app.route("/restart")
def restart():
    global RNUMS
    RNUMS = {}
    

@app.route("/log/<rnum>")
def getlog(rnum):
    r = RNUMS[rnum]
    return r


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
