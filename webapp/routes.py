from datetime import datetime, timedelta
from flask import abort, make_response, redirect, render_template, url_for
from webapp import app
from pandas import DataFrame, read_csv
from statsmodels.tsa.arima.model import ARIMA
import numpy


@app.route('/')
def frontpage():
	# if app.forecast is None:
	# 	return redirect("/update")

	result = app.firebase.get('/history', None)
	try:
		now = str(datetime.now())[:10]
		bones = result[now]
	except KeyError:
		yesterday = str(datetime.now()-timedelta(days=1))[:10]
		bones = result[yesterday]
	return render_template("frontpage.html", result=bones, forecast=app.forecast)


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


@app.route('/update')
def update():
	results = app.firebase.get('/history', None)

	y = []
	for date in results.keys():
		if results[date]["status"] == "bones":
			y.append(1)
		else:
			y.append(0)

	x = list(range(0, len(y)))

	lookup = {}
	sample_len = 3

	for i in range(0, len(y) - sample_len):
		# print(f"{i + 2}/{len(y)}")
		try:
			test = lookup[str(y[i:i + sample_len])]
			lookup[str(y[i:i + sample_len])] = (test + 2 * y[i + sample_len]) / 3
		except KeyError:
			lookup[str(y[i:i + sample_len])] = y[i + sample_len]

	try:
		forecast = lookup[str(y[-sample_len:])]
	except KeyError:
		forecast = 0.3

	if round(forecast) < 0.5:
		result = "nobones"
		confidence = 1 - forecast
	else:
		result = "bones"
		confidence = forecast

	app.forecast = {"forecastResult": result, "confidence": confidence*0.95}

	# old algorithm
	# bool_stream = []
	# for date in results.keys():
	# 	bool_stream.append(int(results[date]["status"] == "bones"))
	#
	# bool_stream.append(1)
	# series = DataFrame(bool_stream)
	#
	# X = series.values
	# # fit model
	# model = ARIMA(X)
	# model_fit = model.fit()
	# # print summary of fit model
	#
	# forecast = model_fit.forecast()[0]
	# key = {0: "nobones", 1: "bones"}
	# if round(forecast) == 0:
	# 	confidence = 1-forecast
	# else:
	# 	confidence = forecast
	#
	# app.forecast = {"forecastResult": key[round(forecast)], "confidence": confidence}
	# print(app.forecast)
	return redirect("/")


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
