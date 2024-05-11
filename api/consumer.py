from kafka import KafkaProducer
import logging
import json
import pandas as pd
import re
import string
from nltk.corpus import stopwords
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from pyspark.sql.functions import udf
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.ml import PipelineModel
import random
import hashlib

def processTweet(tweet):
    tweet = tweet.asDict().get('text')
    if isinstance(tweet, (float, int)):
        tweet = str(tweet)
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

def process(df,epoch_id):
    if df.isEmpty():
        return
    
    df = df.drop('message')
    # Convert DataFrame to Pandas DataFrame
    pdf = df.toPandas()

    pdf['clean_text'] = pdf['text'].apply(processTweet)
    pdf.drop_duplicates(subset=['clean_text'],inplace=True)
    pdf.drop(['text'],axis=1,inplace=True)
    pdf.rename(columns={"clean_text": "text"},inplace=True)
    pdf.dropna(inplace=True)
    pdf.drop(pdf[pdf['text'] == ''].index, inplace = True)
    pdf.drop(pdf[pdf['text'] == ' '].index, inplace = True)
    pdf.drop(pdf[pdf['text'] == 'nan'].index, inplace = True)
    
    spark_df = spark.createDataFrame(pdf)
    
    # Load the pipline model and pre-trained model
    pipeline = PipelineModel.load(path_to_model + 'pipelineFit')
    cvModel = CrossValidatorModel.load(path_to_model + 'cvModel')
    
    # Fit the pipeline to validation documents.
    preprocessed_dataset = pipeline.transform(spark_df)
    # predictions
    predictions = cvModel.transform(preprocessed_dataset)
    
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    response = predictions.toPandas().to_dict(orient='records')
    
    logging.basicConfig(level=logging.INFO)
    # producer = KafkaProducer(bootstrap_servers='localhost:9092')
    # random_id = hashlib.sha1(str(random.randint(1, 1000000)).encode()).hexdigest()
    # producer.send('job_id', value=json.dumps(random_id).encode('utf-8'))
    print('waaaaaaa \n\n\n\n\n',epoch_id,'\n\n\n\n\n')
    print('waaaaaaa \n\n\n\n\n',len(response),'\n\n\n\n\n')
if __name__ == '__main__':
    findspark.init()
    
    # Path to the pre-trained model
    path_to_model = r'api/modeling/saved-models/'

    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("TwitterSentimentAnalysis") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
        .getOrCreate()
        # .config("spark.mongodb.input.uri",
        #         config('MONGOACCESS')) \
        # .config("spark.mongodb.output.uri",
        #         config('MONGOACCESS')) \
        # .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \

    # Spark Context
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')
    
    # Schema for the incoming data
    schema = StructType([StructField("text", StringType())])
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
        .withColumn("text", from_json("message", schema))

    
    query = df \
        .writeStream \
        .foreachBatch(process) \
        .start()

    query.awaitTermination()
    
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    random_id = hashlib.sha1(str(random.randint(1, 1000000)).encode()).hexdigest()
    producer.send('job_id', value=json.dumps(random_id).encode('utf-8'))