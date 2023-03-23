
from datetime import datetime
from flask import Flask, render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  


class Sensor(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Integer)
    hum = db.Column(db.Integer)
    soil = db.Column(db.Integer)
    ir = db.Column(db.Integer)
    ultrasonic = db.Column(db.Integer)
    cdate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.cdate}"


app.app_context().push()
db.create_all()

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        temp = request.args.get('temp')
        hum = request.args.get('hum')
        soil = request.args.get('soil')
        ir = request.args.get('ir')
        ultrasonic = request.args.get('ultrasonic')

        if temp or hum:
            data = Sensor(temp=temp, hum=hum, soil=soil,
                          ir=ir, ultrasonic=ultrasonic)
            db.session.add(data)
            db.session.commit()
            return 'Inserted'
    data = Sensor.query.all()[::-1][:10]
    temp = []
    hum = []
    soil = []
    ir = []
    ultrasonic = []
    date = []
    for x in data:
        temp.append(x.temp)
        hum.append(x.hum)
        soil.append(x.soil)
        ir.append(x.ir)
        ultrasonic.append(x.ultrasonic)
        date.append(x.cdate)
    live = {"temp": data[-1].temp, "hum": data[-1].hum, "soil": data[-1].soil,
            "ir": data[-1].ir, "ultrasonic": data[-1].ultrasonic}
    return render_template('index.html', data=data, live=live, date=date, temp=temp, hum=hum, soil=soil, ir=ir, ultrasonic=ultrasonic)

@app.route('/json', methods=['GET'])
def json_format():
    if request.method == 'GET':
        temp = request.args.get('temp')
        hum = request.args.get('hum')
        soil = request.args.get('soil')
        ir = request.args.get('ir')
        ultrasonic = request.args.get('ultrasonic')

        if temp or hum:
            data = Sensor(temp=temp, hum=hum, soil=soil,
                          ir=ir, ultrasonic=ultrasonic)
            db.session.add(data)
            db.session.commit()
            return 'Inserted'
    data = Sensor.query.all()[::-1][:10]
    temp = []
    hum = []
    soil = []
    ir = []
    ultrasonic = []
    date = []
    for x in data:
        temp.append(x.temp)
        hum.append(x.hum)
        soil.append(x.soil)
        ir.append(x.ir)
        ultrasonic.append(x.ultrasonic)
        date.append(x.cdate)
    live = {"Temperature": data[-1].temp, "Humidity": data[-1].hum, "Soil moisture": data[-1].soil, "Ultrasonic": data[-1].ultrasonic}

    response = jsonify({"date": date[::-1], "live": live,  "temp": temp[::-1], "hum": hum[::-1],
                        "soil": soil[::-1], "ir": ir[::-1], "ultrasonic": ultrasonic[::-1], })


    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route('/add')
def add():
    return render_template('submit.html')


if __name__ == '__main__':
    app.run(debug=True,host="192.168.162.31", port=8000)   