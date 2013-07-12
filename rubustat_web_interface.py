#!/usr/bin/python
import pywapi
import subprocess
import rubustat_daemon

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

ZIP = 37216

#start the daemon in the background
subprocess.Popen("./rubustat_daemon.py", shell=True)

def getWeather():
    result = pywapi.get_weather_from_yahoo( str(ZIP), units = 'imperial' )
    string = result['html_description']
    string = string.replace("\n", "")
    string = string.replace("(provided by <a href=\"http://www.weather.com\" >The Weather Channel</a>)<br/>", "")
    string = string.replace("<br /><a href=\"http://us.rd.yahoo.com/dailynews/rss/weather/Nashville__TN/*http://weather.yahoo.com/forecast/USTN0357_f.html\">Full Forecast at Yahoo! Weather</a><BR/><BR/>", "")
    return string

@app.route('/')
def my_form():
    f = open("set_temp", "r")
    targetTemp = f.readline()
    f.close()
    weatherString = getWeather()
    indoor_temp = rubustat_daemon.getIndoorTemp()
    return render_template("form.html", targetTemp = targetTemp, weatherString = weatherString)

@app.route("/", methods=['POST'])
def my_form_post():

    text = request.form['text']
    newTargetTemp = text.upper()
    f = open("set_temp", "w")
    f.write(newTargetTemp)
    f.close()
    flash("New temperature of " + newTargetTemp + " set!")
    return redirect(url_for('my_form'))

if __name__ == "__main__":
    app.run()