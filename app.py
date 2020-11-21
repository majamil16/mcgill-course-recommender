from flask import Flask, request, render_template
import os
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"


@app.route("/home")
def homepage():
	return "Home"

# The form to enter your courses
@app.route("/form")
def form():
		return render_template('form.html')

# Calls the actual scraper 
@app.route(".")
def scrape():
	return


@app.route('/data/', methods = ['POST', 'GET'])
def data():
	if request.method == "GET":
		return f"go to the /form to complete the form."
	if request.method == "POST":
		form_data = request.form
		return render_template("rec.html", form_data = form_data)

# after you hit submit you are taken here...
@app.route('/rec')
def rec():
		return render_template('rec.html') 

@app.route("/calculator")	
def numbers():
	a = request.args.get('a')
	b = request.args.get('b')
	result = int(a)+int(b)
	return f"Result is:{result}"


if __name__ == "__main__":
	app.run(port=int(os.getenv('PORT', 4444)))
