from flask import Flask, request, render_template, jsonify
#from dbconnect import connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker, Query


app = Flask(__name__)

#this configuration is needed in case of using pre created database
engine = create_engine('mysql://root:password@localhost/energy', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

class Power(Base):
    __table__= Base.metadata.tables['power']

#Set database engine for timer from 
engineFrom = create_engine('mysql://root:password@localhost/light_control', convert_unicode=True, echo=False)
BaseFrom = declarative_base()
BaseFrom.metadata.reflect(engineFrom)

class timeFrom(BaseFrom):
    __table__= BaseFrom.metadata.tables['time_from']

class timeUntil(BaseFrom):
    __table__= BaseFrom.metadata.tables['time_until']

class lightStatus(BaseFrom):
    __table__= BaseFrom.metadata.tables['status']

@app.route('/')
def homepage():
    #result = [5]
    #db_session = scoped_session(sessionmaker(bind=engine))
    #result = db_session.query(Power.volt, Power.current, Power.watt, Power.kwh, Power.wh)
    return render_template("main.html")

#@app.route('/test/')
#def test():
#     #result = [5]
#    db_session = scoped_session(sessionmaker(bind=engine))
#    result = db_session.query(Power.volt, Power.current, Power.watt, Power.kwh, Power.wh)
#    return render_template("test.html", result = result)


@app.route('/dataFrom/')
def dataFrom():
    try:
        statusIntArray = []
        statusStringArray = []
        db_session = scoped_session(sessionmaker(bind=engineFrom))
        resultFrom = db_session.query(timeFrom.light_1, timeFrom.light_2, timeFrom.light_3, timeFrom.light_4, timeFrom.light_5, timeFrom.light_6, timeFrom.light_7, timeFrom.light_8, timeFrom.light_9, timeFrom.light_10, timeFrom.light_11, timeFrom.light_12, timeFrom.light_13)
        #return jsonify(result)
        for r in resultFrom: 
            light1 = r.light_1
            light2 = r.light_2
            light3 = r.light_3
            light4 = r.light_4
            light5 = r.light_5
            light6 = r.light_6
            light7 = r.light_7
            light8 = r.light_8
            light9 = r.light_9
            light10 = r.light_10
            light11 = r.light_11
            light12 = r.light_12
            light13 = r.light_13
        #db_session.close()
        #return jsonify({'light1' : light1, 'light2' : light2, 'light3' : light3, 'light4' : light4, 'light5' : light5, 'light6' : light6, 'light7' : light7,'light8' : light8, 'light9' : light9, 'light10' : light10, 'light11' : light11, 'light12' : light12, 'light13' : light13,})

        resultUntil = db_session.query(timeUntil.light_1, timeUntil.light_2, timeUntil.light_3, timeUntil.light_4, timeUntil.light_5, timeUntil.light_6, timeUntil.light_7, timeUntil.light_8, timeUntil.light_9, timeUntil.light_10, timeUntil.light_11, timeUntil.light_12, timeUntil.light_13)
        for r in resultUntil:
            lightUntil1 = r.light_1
            lightUntil2 = r.light_2
            lightUntil3 = r.light_3
            lightUntil4 = r.light_4
            lightUntil5 = r.light_5
            lightUntil6 = r.light_6
            lightUntil7 = r.light_7
            lightUntil8 = r.light_8
            lightUntil9 = r.light_9
            lightUntil10 = r.light_10
            lightUntil11 = r.light_11
            lightUntil12 = r.light_12
            lightUntil13 = r.light_13

        resultStatus = db_session.query(lightStatus.light_1, lightStatus.light_2, lightStatus.light_3, lightStatus.light_4, lightStatus.light_5, lightStatus.light_6, lightStatus.light_7, lightStatus.light_8, lightStatus.light_9, lightStatus.light_10, lightStatus.light_11, lightStatus.light_12, lightStatus.light_13)
        for r in resultStatus:
            statusIntArray.append(r.light_1)
            statusIntArray.append(r.light_2)            
            statusIntArray.append(r.light_3)
            statusIntArray.append(r.light_4)
            statusIntArray.append(r.light_5)
            statusIntArray.append(r.light_6)
            statusIntArray.append(r.light_7)
            statusIntArray.append(r.light_8)
            statusIntArray.append(r.light_9)
            statusIntArray.append(r.light_10)
            statusIntArray.append(r.light_11)
            statusIntArray.append(r.light_12)
            statusIntArray.append(r.light_13)

        db_session.close()

        for i in xrange(len(statusIntArray)):
            if statusIntArray[i] == '1':
                statusStringArray.append('ON')
            elif statusIntArray[i] == '0':
                statusStringArray.append('OFF')

        return jsonify({'light1' : light1, 'light2' : light2, 'light3' : light3, 'light4' : light4, 'light5' : light5, 'light6' : light6, 'light7' : light7,'light8' : light8, 'light9' : light9, 'light10' : light10, 'light11' : light11, 'light12' : light12, 'light13' : light13, 'lightUntil1' : lightUntil1, 'lightUntil2' : lightUntil2, 'lightUntil3' : lightUntil3, 'lightUntil4' : lightUntil4, 'lightUntil5' : lightUntil5, 'lightUntil6' : lightUntil6, 'lightUntil7' : lightUntil7,'lightUntil8' : lightUntil8, 'lightUntil9' : lightUntil9, 'lightUntil10' : lightUntil10, 'lightUntil11' : lightUntil11, 'lightUntil12' : lightUntil12, 'lightUntil13' : lightUntil13, 'status1' : statusStringArray[0], 'status2' : statusStringArray[1], 'status3' : statusStringArray[2], 'status4' : statusStringArray[3], 'status5' : statusStringArray[4], 'status6' : statusStringArray[5], 'status7' : statusStringArray[6], 'status8' : statusStringArray[7], 'status9' : statusStringArray[8], 'status10' : statusStringArray[9], 'status11' : statusStringArray[10], 'status12' : statusStringArray[11], 'status13' : statusStringArray[12],})
        #return  jsonify(result='siemaneczko')
    except Exception as e:
        return str(e)


@app.route('/interactive/')
def interactive():
	return render_template('interactive.html')


@app.route('/data/')
def data():
    try:
        #result = [5]
        db_session = scoped_session(sessionmaker(bind=engine))
        result = db_session.query(Power.volt, Power.current, Power.watt, Power.kwh, Power.wh, Power.humidity, Power.temperature, Power.on_light, Power.off_light)
        #return jsonify(result)
        for r in result: 
            volt = r.volt
            current = r.current
            watt = r.watt
            kwh = r.kwh
            wh = r.wh
            humidity = r.humidity
            temperature = r.temperature
            onLight = r.on_light
            offLight = r.off_light
	db_session.close()
        return jsonify({'volt' : volt, 'current' : current, 'watt' : watt, 'kwh' : kwh, 'wh' : wh, 'humidity' : humidity, 'temperature' : temperature, 'onLight' : onLight, 'offLight' : offLight})
        #return  jsonify(result='siemaneczko')
    except Exception as e:
        return str(e)



if __name__ == "__main__":

    app.run()
