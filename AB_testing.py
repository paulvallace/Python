# project: p4
# submitter: pvallace
# partner: none
# hours: 12

import pandas as pd
from flask import Flask, request, jsonify
import flask
import re
import time
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


app = Flask(__name__)
# df = pd.read_csv("main.csv")

donate_visits = 0
def total_dv():
    global donate_visits
    donate_visits += 1
    return donate_visits

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()
        
    a = html.replace("donate.html", "donate.html?from=A")
    a = a.replace("powderblue", "red")
    b = html.replace("donate.html", "donate.html?from=B")

    total_dv()
    global donate_visits
    global a_count
    global b_count
    if donate_visits <= 10:
        if donate_visits % 2 == 0:
            return a
        else:
            return b
    else:
        if a_count > b_count:
            return a
        else:
            return b
        
a_count = 0
b_count = 0 
@app.route('/donate.html')
def donation():
    with open("donate.html") as f:
        html = f.read()
    global a_count
    global b_count
    routes = request.args
    if "from" in routes:
        value = routes["from"]
        if value == "A":
            a_count += 1
        else:
            b_count += 1
            
    return html


@app.route('/browse.html')
def browser():
    df = pd.read_csv("main.csv")
    return "<h1> All Data<h/h1>" + df.to_html(escape = False)

num_subscribed = 0
@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    if len(re.findall(r"^\w+@\w+\.(\w+\.)?(edu|com|org|net|io|gov)", email)) > 0: # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        num_subscribed += 1
        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")
    return jsonify("Please STOP being so Careless") # 3

ip_dict = {}
ip_list = []
last_visit = 0
@app.route('/browse.json')
def browse_json():
    global last_visit
    global ip_list
    global ip_dict
    
    df = pd.read_csv("main.csv")
    
    if request.remote_addr not in ip_list:
        ip_list.append(request.remote_addr)
        ip_dict[request.remote_addr] = time.time()
        return jsonify(df.to_dict())
    else: 
        if time.time() - ip_dict[request.remote_addr] > 60:
            ip_dict[request.remote_addr] = time.time() 
            return jsonify(df.to_dict())
        else:
            return flask.Response("<b>go away</b>",
                              status=429,
                              headers={"Retry-After": "1"})


@app.route('/visitors.json')
def visit_json():
    global ip_list
    return jsonify(ip_list)

@app.route("/scatterplot.svg")
def scatterplot():
    fig, ax = plt.subplots()
    df = pd.read_csv("main.csv")
    df.plot.scatter(ax= ax, x="AdjD", y = "AdjO")
    ax.set_xlabel("Adjust Offensive Effeciency")
    ax.set_ylabel("Adjust Defensive Effeciency")
    plt.tight_layout()

    
    f = io.StringIO() 
    fig.savefig(f, format="svg")
    plt.close()
    
    return flask.Response(f.getvalue(), headers={"Content-Type": "image/svg+xml"})


@app.route("/plot1.svg")
def plot1():
    df = pd.read_csv("main.csv")
    bins = request.args
    if len(bins) != 0:
        if "bins" in bins:
            value = bins["bins"]
            adjd = df['AdjD']
            fig, ax = plt.subplots()
            adjd.plot.hist(ax=ax, bins =int(value))
    else:
        adjd = df['AdjD']
        fig, ax = plt.subplots()
        adjd.plot.hist(ax=ax, bins =10)
    
    ax.set_xlabel("Adjust Defense Effeciency")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    
    
    f = io.StringIO() 
    fig.savefig(f, format="svg")
    plt.close()
    return flask.Response(f.getvalue(), headers={"Content-Type": "image/svg+xml"})

        
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!
   
 #NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.
