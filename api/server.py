import flask
from flask_cors import CORS
import pandas as pd
from kafka import KafkaProducer, KafkaConsumer
import json
import threading
import random
import hashlib
import datetime

class KafkaConsumerThread(threading.Thread):
    def __init__(self, topic_name):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.consumer = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.consumer.subscribe([topic_name])
        self.job_id = None
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            for message in self.consumer:
                if self.stop_event.is_set():
                    self.job_id = message.value
                    break

app = flask.Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello World"

@app.route('/predict/file/', methods=['GET', 'POST'])
def predict_file():
    try:
        file_path = flask.request.files['datafile']
            
        if file_path.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.filename.endswith('.json'):
            df = pd.read_json(file_path)
        elif file_path.filename.endswith('.txt'):
            df = pd.read_csv(file_path, sep='\t')
        else:
            return flask.Response('File type not supported', status=400)

        responseDICT = df.to_dict(orient='records')
        random_id = hashlib.sha1(str(random.randint(1, 1000000)).encode()).hexdigest()
        for tweet in responseDICT:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                'job_id': random_id,
                'type': 'file',
                'text': tweet['text'],
                'df_length' : len(df),
                'timestamp': timestamp
            }
            producer.send('twitter', value=json.dumps(data).encode('utf-8'))
        consumer_thread = KafkaConsumerThread('job_id')
        consumer_thread.start()
        consumer_thread.stop()
        consumer_thread.join()
        response = flask.Response(response=consumer_thread.job_id, status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Access-Control-Allow-Credentials'] = True
        
        return response
    
    except Exception as e:
        return flask.Response(response=str(e), status=500)
    
@app.route('/predict/text/', methods=['GET', 'POST'])
def predict_text():
    try:
        text = flask.request.form['textdata']
        
        print(text)

        random_id = hashlib.sha1(str(random.randint(1, 1000000)).encode()).hexdigest()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            'job_id': random_id,
            'type': 'text',
            'text': text,
            'df_length' : 1,
            'timestamp': timestamp
        }
        producer.send('twitter', value=json.dumps(data).encode('utf-8'))
        consumer_thread = KafkaConsumerThread('job_id')
        consumer_thread.start()
        consumer_thread.stop()
        consumer_thread.join()

        response = flask.Response(response=consumer_thread.job_id, status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Access-Control-Allow-Credentials'] = True

        print(response)
        return response
    
    except Exception as e:
        return flask.Response(response=str(e), status=500)
    
if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    app.run(port=5000)