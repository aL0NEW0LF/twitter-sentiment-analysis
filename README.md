# Twitter-sentiment-analysis

This project is an app backboned by a distributed system that performs sentiment analysis on tweets. The app is built using svelte and flask, and the distributed system is built using Apache Kafka and Apache Spark.

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

To run the backend, navigate to the `api` directory and run the following commands:

```bash
cd api
```

**Windows**

```bash
py -3 -m venv .venv
```

**MacOS/Linus**

```bash
python3 -m venv .venv
```

Then, activate the env:

**Windows**

```bash
.venv\Scripts\activate
```

**MacOS/Linus**

```bash
. .venv/bin/activate
```

You can run the following command to install the dependencies:

```bash
pip3 install -r requirements.txt
```

Then you are good to go.
