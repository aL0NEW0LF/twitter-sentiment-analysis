""" 
import re
import findspark
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from decouple import config


def write_row_in_mongo(df):
    mongo_uri = config('MONGOACCESS')

    df.write.format("mongo").mode("append").option("uri", mongo_uri).save()


if __name__ == "__main__":
    findspark.init()

    # Path to the pre-trained model
    path_to_model = r''

    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("TwitterSentimentAnalysis") \
        .config("spark.mongodb.input.uri",
                config('MONGOACCESS')) \
        .config("spark.mongodb.output.uri",
                config('MONGOACCESS')) \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
        .getOrCreate()

    # Spark Context
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')

    # Schema for the incoming data
    schema = StructType([StructField("message", StringType())])

    # Read the data from kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "twitter") \
        .option("startingOffsets", "latest") \
        .option("header", "true") \
        .load() \
        .selectExpr("CAST(value AS STRING) as message")

    df = df \
        .withColumn("value", from_json("message", schema))

    # Pre-processing the data
    pre_process = udf(
        lambda x: re.sub(r'[^A-Za-z\n ]|(http\S+)|(www.\S+)', '', x.lower().strip()).split(), ArrayType(StringType())
    )
    df = df.withColumn("cleaned_data", pre_process(df.message)).dropna()

    # Load the pre-trained model
    pipeline_model = PipelineModel.load(path_to_model)
    # Make predictions
    prediction = pipeline_model.transform(df)
    # Select the columns of interest
    prediction = prediction.select(prediction.message, prediction.prediction)

    # Load prediction in Mongo
    query = prediction.writeStream.queryName("tweets") \
        .foreachBatch(write_row_in_mongo).start()
    query.awaitTermination() 
"""

import flask
import re
import findspark
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from decouple import config
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

def write_row_in_mongo(df):
    mongo_uri = config('MONGOACCESS')

    df.write.format("mongo").mode("append").option("uri", mongo_uri).save()


@app.route('/')
def home():
    return "Hello World"

@app.route('/predict-file', methods=['GET', 'POST'])
def predict_file():
    try:
        file_path = flask.request.files['datafile']
        
        print(file_path.filename)

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
    
@app.route('/predict-text', methods=['GET', 'POST'])
def predict_text():
    try:
        text = flask.request.form['text']
        
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