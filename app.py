from flask import Flask, flash, redirect, render_template, request, session, abort
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


@app.route("/form/fillOut/", methods = ["GET", "POST"])
def hello():
    return render_template('Formv2.html')


@app.route("/form/response/", methods = ["GET", "POST"])
def response():
    choice=request.form['userChoice']
    environment=request.form['env']
    ssid=request.form['SSID']
    return render_template('Responsev2.html', choice=choice, environment=environment, ssid=ssid)



if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run()





