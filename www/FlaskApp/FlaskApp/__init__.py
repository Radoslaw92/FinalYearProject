from flask import Flask, request, render_template, jsonify
#from dbconnect import connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker, Query


app = Flask(__name__)

#this configuration is needed if case of using pre created database
engine = create_engine('mysql://root:password@localhost/energy', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

class Power(Base):
    __table__= Base.metadata.tables['power']

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
