from flask import Flask, flash, redirect, render_template, request, session, abort
import get_AWSInfo
app = Flask(__name__)

@app.route("/")
def index():
    return "Flask App!"

# @app.route("/hello")
# def hello():
#     return "Hello World!"

@app.route("/members")
def members():
    return "Members"


@app.route("/hello/Isabella/", methods = ["GET", "POST"])
def hello():
    return render_template(
        'form.html')
    

@app.route("/hello/Isabella/response/", methods = ["GET", "POST"])
def response():

    choice=request.form['userChoice']
    environment=request.form['env']
    ssid=request.form['SSID']

    ## call the backend python script


    return render_template('response.html', choice=choice, environment=environment, ssid=ssid)


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run()




