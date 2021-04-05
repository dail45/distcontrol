import time

from flask import Flask, request
import requests
import os

app = Flask(__name__)
flagUpLoad = True
flagDownLoad = False
countfiles = 0
file = b""

@app.route('/upload', methods=['POST'])
def upload():
    global file, flagDownLoad
    file = request.data
    flagDownLoad = True
    return file

@app.route('/download')
def download():
    return file

@app.route('/accessupload/<int:count>', methods=['GET'])
def get_access_upload(count):
    global countfiles, flagUpLoad
    count1 = 0
    while count1 < 2000:
        if flagUpLoad:
            countfiles = count
            flagUpLoad = not flagUpLoad
            return "1"
        count1 += 1
        time.sleep(0.005)
    return "0"

@app.route('/accessdownload')
def get_access_download():
    global flagDownLoad, flagUpLoad
    count1 = 0
    while count1 < 2000:
        if flagDownLoad:
            flagDownLoad = not flagDownLoad
            return {"status": 1, "count": countfiles}
        count1 += 1
        time.sleep(0.005)
    flagUpLoad = True
    return {"status": 0}


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)