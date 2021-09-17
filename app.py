import time
import threading
from flask import Flask, request
import requests
import os
import urllib3

app = Flask(__name__)


def generator_chunks_number():
    counter = 0
    end = int(total_length) // (4*1024*1024) + 1
    while counter < end:
        if counter < file_chunks["counter"]:
            counter += 1
            print(file_chunks.keys(), file_chunks["counter"])
            yield counter
        else:
            yield -1


download_link = ""
file_chunks = {"counter": 0}
total_length = 0
file_chunks_number_gen = None


@app.route("/")
def fun():
    return "Ok."


@app.route("/download")
def download():
    global download_link, total_length, file_chunks_number_gen
    if download_status() == "alive":
        return "0"
    restart()
    download_link = request.args["public_key"]
    data = requests.get(download_link, stream=True)
    ret = data.headers
    total_length = int(ret["Content-Length"])
    data.close()
    a = threading.Thread(target=generage_download_file_chunks)
    a.start()
    file_chunks_number_gen = generator_chunks_number()
    return str(ret)


def generage_download_file_chunks():
    global file_chunks
    http = urllib3.PoolManager()
    r = http.urlopen("GET", download_link, preload_content=False)
    r.auto_close = False
    generator = r.stream(4*1024*1024)
    while True:
        if len(file_chunks) < 16+1:
            try:
                file_chunks[file_chunks["counter"] + 1] = next(generator)
                file_chunks["counter"] += 1
            except StopIteration:
                break


@app.route("/await_chunk/<int:count>")
def await_chunk(count):
    global file_chunks
    for _ in range(20):
        a = next(file_chunks_number_gen)
        if a != -1:
            break
        time.sleep(.025)
    if a == -1:
        return "0"
    return f"{a}"


@app.route("/download_chunk/<int:count>")
def download_chunk(count):
    global file_chunks
    res = file_chunks[count]
    del file_chunks[count]
    return res


@app.route("/downloadStatus")
def download_status():
    num = total_length // (4*1024*1024)
    if num > 0:
        num += 1
    if file_chunks["counter"] < num:
        return f"{num}, {file_chunks['counter']}"
    return "dead"


@app.route("/restart")
def restart():
    global download_link, file_chunks, total_length, file_chunks_number_gen
    download_link = ""
    file_chunks = {"counter": 0}
    total_length = 0
    file_chunks_number_gen = None
    return "restart done"


@app.route("/log")
def log():
    return str({"download_link": download_link,
            "file_chunks": file_chunks.keys(),
            "total_length": total_length,
            "file_chunks_number_gen": file_chunks_number_gen})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)