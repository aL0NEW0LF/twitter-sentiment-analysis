# Twitter-sentiment-analysis

This project is an app backboned by a distributed system that performs sentiment analysis on tweets. The app is built using svelte and flask, and the distributed system is built using Apache Kafka and Apache Spark.

## Architecture

![Architecture](https://github.com/aL0NEW0LF/twitter-sentiment-analysis/blob/main/app.png?raw=true)

The system is composed of 3 layers:

### App (User Interface)

The user interface is a web application developed with Svelte that allows users to interact with the system. They can view jobs history and details, as well as initiate new jobs to either predict the sentiment of a single tweet or multiple tweets in a file.

### API (Backend)

The API is a RESTful service developed with Flask that serves as the intermediary between the user interface, the system and the database. It is responsible for handling user requests, processing them and returning the results.

### System (Kafka and Spark)

The system is composed of two main components: the Kafka pipeline and the Spark job. The Kafka pipeline ingests Twitter posts and sends them to the Spark job for processing. The Spark job preprocess, analyzes the data and provides instant sentiment prediction.

After prediction, the results are stored in a mongodb database for future reference, Then is sent back an ID to the user interface for a confirmation. The user can then query the database for the results of the job.

### Docker

The system and API are containerized with Docker to ensure portability and ease of deployment. The containers are orchestrated with Docker Compose to manage the system components and their dependencies.

## Model

The sentiment analysis model is a pre-trained Cross-Validation & Logistic Regression model that is trained on a dataset of more than 63k tweets. The model is used to predict the sentiment of a tweet as either positive, negative, neutral or irrelevant. The model performs with an accuracy of 93%.

## Getting Started

First, clone the repository:

```bash
git clone https://github.com/aL0NEW0LF/twitter-sentiment-analysis
```

### Frontend

To run the frontend, navigate to the `app` directory and run the following commands:

```bash
cd app
```

```bash
pnpm install
```

To start the frontend, run the following command:

```bash
pnpm run dev --open
```

### Backend

To run the backend, you should compose the docker containers with:
```bash
docker-compose -f docker-compose.yml up -d
```

then go to the `TheKafkaShore` container command line to create the kafka topics with:

```bash
kafka-topics --create --topic twitter --bootstrap-server localhost:9092
```

```bash
kafka-topics --create --topic job_id --bootstrap-server localhost:9092
```
Then you are good to go.

# TODO

- [ ] Change saving jéSon schema to mongodb.
- [ ] Add streaming tweet and one by one treatment.
- [ ] Add .env variables to remove hard coded variables.
