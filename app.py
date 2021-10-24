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
        if "info" in args:
            RNUMS[rnum]["info"] = args["info"]


def clean():
    if RNUMS:
        for rnum in RNUMS.keys():
            if time.time() - RNUMS[rnum]["timeout"] > 40:
                del RNUMS[rnum]


@app.route("/getrnums")
def getrnums():
    clean()
    return RNUMS


@app.route("/gtrn")
def gtrn():
    clean()
    if RNUMS:
        return str(list(RNUMS.keys()))
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
    start = time.time()
    args = request.args
    rnum = args["rnum"]
    if rnum not in RNUMS:
        login(rnum)
    RNUMS[rnum]["timeout"] = time.time()
    while True:
        if time.time() - start > 20:
            return "0"
        if len(RNUMS[rnum]["com"]) > 0:
            com = RNUMS[rnum]["com"].pop(0)
            break
        time.sleep(0.1)
    return com


@app.route("/getanswer")
def getanswer():
    start = time.time()
    args = request.args
    rnum = args["rnum"]
    while True:
        if time.time() - start > 20:
            return "0"
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
    RNUMS[rnum]["timeout"] = time.time()
    RNUMS[rnum]["ans"].append(ans)
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
