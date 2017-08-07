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
 

@app.route("/hello/Isabella/", methods = ["GET", "POST"])
def hello():
    return render_template(
        'form.html')

 
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run()
 



