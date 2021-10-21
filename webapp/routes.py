from datetime import datetime, timedelta
from flask import abort, make_response, render_template
from webapp import app


@app.route('/')
def frontpage():
	result = app.firebase.get('/history', None)
	try:
		now = str(datetime.now())[:10]
		bones = result[now]
	except KeyError:
		yesterday = str(datetime.now()-timedelta(days=1))[:10]
		bones = result[yesterday]
	return render_template("frontpage.html", result=bones)


@app.get("/history")
def history():
	results = app.firebase.get('/history', None)
	return render_template("history.html", results=results)


@app.route('/apidocs')
def api_docs():
	return render_template('apidocs.html')


@app.route('/getnotified')
def getnotified():
	return render_template('getnotified.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.get("/css/<filename>")
def css(filename):
	try:
		with open(str(app.root + "/webapp/static/scss/" + filename[:-4] + ".scss"), "r") as contents:
			compiled = app.scss_compiler.compile_string(contents.read())
			response = make_response(compiled)
			response.mimetype = "text/css"
			return response
	except:
		abort(420)
