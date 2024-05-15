from kafka import KafkaProducer
import logging
import json
import pandas as pd
import re
import string
from nltk.corpus import stopwords
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.ml import PipelineModel
import time
import threading

def write_row_in_mongo(df):
    # mongo_uri = "mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]"
    mongo_uri = "mongodb+srv://samatshi:2vL3J8ENgOpb69f0@cluster.gjv97ym.mongodb.net/TwitterSentimentAnalysis.jobs?retryWrites=true&w=majority&appName=Cluster"
    df.write.format("mongo").mode("append").option("uri", mongo_uri).save()

def processTweet(tweet):
    
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
def correct_label(label):
    if label == 0:
        return 'Irrelevant'
    elif label == 1:
        return 'Negative'
    elif label == 2:
        return 'Neutral'
    else:
        return 'Positive'
def process(df,epoch_id):
    
    global processed
    global df_len
    
    if df.isEmpty():
        return
    print(df.show())
    if df_len == 0:
        df_len = int(df.select('df_length').first()[0])
        
    df = df.drop('message')
    pdf = df.toPandas()
    l1 = len(pdf)
    pdf['clean_text'] = pdf['text'].apply(processTweet)
    pdf.drop_duplicates(subset=['clean_text'],inplace=True)
    pdf.drop(['df_length'],axis=1,inplace=True)
    pdf.drop(['text'],axis=1,inplace=True)
    pdf.rename(columns={"clean_text": "text"},inplace=True)
    pdf.dropna(subset=['text'], inplace=True)
    pdf.drop(pdf[pdf['text'] == ''].index, inplace = True)
    pdf.drop(pdf[pdf['text'] == ' '].index, inplace = True)
    pdf.drop(pdf[pdf['text'] == 'nan'].index, inplace = True)
    l2 = len(pdf)
    
    ln = l1 - l2
    processed += l2
    df_len -= ln
    
    spark_df = spark.createDataFrame(pdf)
    
    # Load the pipline model and pre-trained model
    pipeline = PipelineModel.load(path_to_model + 'pipelineFit')
    cvModel = CrossValidatorModel.load(path_to_model + 'cvModel')
    
    # Fit the pipeline to validation documents.
    preprocessed_dataset = pipeline.transform(spark_df)
    # predictions
    predictions = cvModel.transform(preprocessed_dataset)
    
    predictions = predictions.withColumn('prediction', predictions['prediction'].cast('int'))
    correct_label_udf = udf(correct_label, StringType())
    predictions = predictions.withColumn('prediction', correct_label_udf(predictions['prediction']))
    
    if df_len == processed:
        df_len = 0
        processed = 0
    logging.basicConfig(level=logging.INFO)
    # Start a new thread that checks the query status
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    threading.Thread(target=check_query_status, args=(query, producer, predictions, processed, df_len)).start()
    
def check_query_status(query, producer, df, processed, df_len):
    while query.status['isDataAvailable']:
        time.sleep(1)
    random_id = df.select('job_id').first()[0]
    df = df.select('job_id', 'type', 'timestamp', 'text', 'probability', 'prediction')
    df = df.withColumn("probability", df["probability"].cast('string'))
    write_row_in_mongo(df)
    if df_len == processed:
        producer.send('job_id', value=json.dumps(random_id).encode('utf-8'))
        df_len = 0
        processed = 0
        
if __name__ == '__main__':
    findspark.init()
    
    # Path to the pre-trained model
    path_to_model = r'api/modeling/saved-models/'

    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("TwitterSentimentAnalysis") \
        .config("spark.mongodb.input.uri", "mongodb+srv://samatshi:2vL3J8ENgOpb69f0@cluster.gjv97ym.mongodb.net/TwitterSentimentAnalysis.jobs?retryWrites=true&w=majority&appName=Cluster") \
        .config("spark.mongodb.output.uri", "mongodb+srv://samatshi:2vL3J8ENgOpb69f0@cluster.gjv97ym.mongodb.net/TwitterSentimentAnalysis.jobs?retryWrites=true&w=majority&appName=Cluster") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .getOrCreate()

    # Spark Context
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')
    
    # Schema for the incoming data
    schema = StructType([
        StructField("job_id", StringType()),
        StructField("type", StringType()),
        StructField("text", StringType()),
        StructField("df_length", IntegerType()),
        StructField("timestamp", StringType())
    ])

    # Read the data from kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "twitter") \
        .option("maxOffsetsPerTrigger", "1000000") \
        .option("startingOffsets", "latest") \
        .option("header", "true") \
        .load() \
        .selectExpr("CAST(value AS STRING) as message")
    
    df = df \
        .withColumn("data", from_json("message", schema)) \
        .select(col("data.*"))
        
    df_len = 0
    processed = 0
    
    query = df \
        .writeStream \
        .foreachBatch(process) \
        .start()
    
    query.awaitTermination()
    