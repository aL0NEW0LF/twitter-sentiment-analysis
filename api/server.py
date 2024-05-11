import flask
import re
from decouple import config
from flask_cors import CORS
import pandas as pd
import string
from nltk.corpus import stopwords
from kafka import KafkaProducer, KafkaConsumer
import json
import threading

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

def write_row_in_mongo(df):
    mongo_uri = config('MONGOACCESS')

    df.write.format("mongo").mode("append").option("uri", mongo_uri).save()

def processTweet(tweet):
    if isinstance(tweet, (float, int)):
        return str(tweet)
    # remove user handles tagged in the tweet
    tweet = re.sub('@[^\s]+','',tweet)
    # remove words that start with th dollar sign    
    tweet = re.sub(r'\$\w*', '', tweet)
    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*\/\w*', '', tweet)
    tweet = re.sub(r'(?:^|[\s,])([\w-]+\.[a-z]{2,}\S*)\b','',tweet)
    # remove hashtags
    tweet = re.sub(r'#\w*', '', tweet)
    # remove all kinds of punctuations and special characters
    punkt = string.punctuation + r'''`‘’)(+÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”،.”…“–ـ”.°ा'''
    tweet = tweet.translate(str.maketrans('', '', punkt))
    # remove words with 2 or fewer letters
    tweet = re.sub(r'\b\w{1,2}\b', '', tweet)
    # remove HTML special entities (e.g. &amp;)
    tweet = re.sub(r'\&\w*;', '', tweet)
    # remove whitespace (including new line characters)
    tweet = re.sub(r'\s\s+', ' ', tweet)
    # remove stopwords
    tweet = re.sub(r'\b('+ '|'.join(stopword for stopword in stopwords.words('english'))+ r')\b', '', tweet)
    # remove single space remaining at the front of the tweet.
    tweet = tweet.lstrip(' ')
    tweet = tweet.rstrip(' ')
    # remove characters beyond Basic Multilingual Plane (BMP) of Unicode:
    tweet = ''.join(c for c in tweet if c <= '\uffff')
    tweet = re.sub(r'([^\u1F600-\u1F6FF\s])','', tweet)
    # lowercase
    tweet = tweet.lower()
    # remove extra spaces
    tweet = re.sub(r'[\s]{2, }', ' ', tweet)
    return tweet

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
        
        # logging.basicConfig(level=logging.INFO) 
        responseDICT = df.to_dict(orient='records')
        
        for tweet in responseDICT:
            data = {
                'text': tweet['text']
            }
            producer.send('twitter', value=json.dumps(data).encode('utf-8'))
        consumer_thread = KafkaConsumerThread('job_id')
        consumer_thread.start()
        consumer_thread.stop()
        consumer_thread.join()
        print("hamid: ",consumer_thread.job_id)
        response = flask.Response(response=consumer_thread.job_id, status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Access-Control-Allow-Credentials'] = True
        print(response)
        
        return response
    
    except Exception as e:
        return flask.Response(response=str(e), status=500)
    
@app.route('/predict/text/', methods=['GET', 'POST'])
def predict_text():
    try:
        text = flask.request.form['textdata']
        
        print(text)

        df = pd.DataFrame({'message': [text]})

        responseJSON = df.to_json(orient='records')
        
        print(responseJSON)

        response = flask.Response(response=responseJSON, status=200, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Access-Control-Allow-Credentials'] = True

        print(response)
        return response
    
    except Exception as e:
        return flask.Response(response=str(e), status=500)
    
if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    global job_id
    app.run(port=5000)