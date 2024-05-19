from flask import Response, request, Flask
from flask_cors import CORS
import pandas as pd
from kafka import KafkaProducer, KafkaConsumer
import json
import threading
import random
import hashlib
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
    
def parse_job_details(details):
    parsed_details = []
    job_details_str = details[0]["job_details"]
    for job in job_details_str:
        parsed_job = json.loads(job)
        parsed_job['probability'] = json.loads(parsed_job['probability'])
        parsed_details.append(parsed_job)
    return parsed_details

class KafkaConsumerThread(threading.Thread):
    def __init__(self, topic_name):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.consumer = KafkaConsumer(
            bootstrap_servers='TheKafkaShore:9092',
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

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello World"

@app.route('/predict/file/', methods=['GET', 'POST'])
def predict_file():
    try:
        file_path = request.files['datafile']
            
        if file_path.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.filename.endswith('.json'):
            df = pd.read_json(file_path)
        elif file_path.filename.endswith('.txt'):
            df = pd.read_csv(file_path, sep='\t')
        else:
            return Response('File type not supported', status=400)

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
        response = Response(response=JSONEncoder().encode({"job_id" : consumer_thread.job_id}), status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Access-Control-Allow-Credentials'] = True
        
        return response
    
    except Exception as e:
        return Response(response=str(e), status=500)
    
@app.route('/predict/text/', methods=['GET', 'POST'])
def predict_text():
    try:
        text = request.form['textdata']
        
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

        response = Response(response=JSONEncoder().encode({"job_id" : consumer_thread.job_id}), status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Access-Control-Allow-Credentials'] = True

        print(response)
        return response
    
    except Exception as e:
        return Response(response=str(e), status=500)
    
@app.route('/jobs/<job_id>', methods=['POST'])
def get_job(job_id):
    try:
        client = MongoClient('mongodb://host.docker.internal:27017/', server_api=ServerApi('1'))
        db = client['TwitterSentimentAnalysis']
        collection = db['jobs']
        result = collection.find({"job_id": job_id}, {"_id": 0, "job_id": 0, "type": 0, "timestamp": 0})
        responseJSON = []
        for i in result:
            responseJSON.append(i)
        
        response = Response(response=JSONEncoder().encode(responseJSON), status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Credentials'] = True

        return response
    
    except Exception as e:
        return Response(response=str(e), status=500)
    
    finally:
        client.close()

@app.route('/jobs/<job_id>/count', methods=['POST'])
def get_job_count(job_id):
    try:
        client = MongoClient('mongodb://host.docker.internal:27017/', server_api=ServerApi('1'))
        db = client['TwitterSentimentAnalysis']
        collection = db['jobs']
        result = collection.find({"job_id": job_id}, {"_id": 0, "job_id": 0, "type": 0, "timestamp": 0})
        
        # prediction values count
        positive = 0
        negative = 0
        neutral = 0
        irrelevant = 0

        for i in result:
            if i['prediction'] == 'Positive':
                positive += 1
            elif i['prediction'] == 'Negative':
                negative += 1
            elif i['prediction'] == 'Neutral':
                neutral += 1
            else:
                irrelevant += 1

        responseJSON = [irrelevant, negative, neutral, positive]

        print(JSONEncoder().encode(responseJSON))
        response = Response(response=JSONEncoder().encode(responseJSON), status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Credentials'] = True

        return response
    
    except Exception as e:
        return Response(response=str(e), status=500)
    
    finally:
        client.close()

@app.route('/jobs/history', methods=['POST'])
def get_job_history():
    try:
        client = MongoClient('mongodb://host.docker.internal:27017/', server_api=ServerApi('1'))
        db = client['TwitterSentimentAnalysis']
        collection = db['jobs']
        result = collection.distinct('job_id')
        responseJSON = []

        for i in result:
            responseJSON.append(collection.find_one({'job_id': i}, {'_id':0, 'job_id': 1, 'type': 1, 'timestamp': 1}))

        print(responseJSON)
        response = Response(response=JSONEncoder().encode(responseJSON), status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Credentials'] = True

        return response
    
    except Exception as e:
        return Response(response=str(e), status=500)
    
    finally:
        client.close()

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='TheKafkaShore:9092')
    app.run(debug=True, port=5000, host='0.0.0.0')
