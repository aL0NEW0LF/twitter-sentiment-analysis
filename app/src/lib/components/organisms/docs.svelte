<script>
	import app from '$lib/assets/app.png';
</script>

<svelte:head>
	<title>Twitter Sentiment Analysis</title>
	<meta name="description" content="Data Playground" />
</svelte:head>

<section class="pb-8">
	<h1 class="py-8 text-4xl font-black">Architecture</h1>
	<p class="text-justify">
		Our system is powered by a Kafka and Spark pipeline that ingests Twitter posts in real-time. The
		data is processed and analyzed to provide instant predictions. The system architecture is as
		follows:
	</p>
	<img src={app} alt="architecture" class="py-4" />
	<p class="text-justify">The system is composed of 3 layers:</p>
	<h2 class="py-8 text-2xl font-black">App (User Interface)</h2>
	<p class="text-justify">
		The user interface is a web application developed with Svelte that allows users to interact with
		the system. They can view jobs history and details, as well as initiate new jobs to either
		predict the sentiment of a single tweet or multiple tweets in a file.
	</p>
	<h2 class="py-8 text-2xl font-black">API (Backend)</h2>
	<p class="text-justify">
		The API is a RESTful service developed with Flask that serves as the intermediary between the
		user interface, the system and the database. It is responsible for handling user requests,
		processing them and returning the results.
	</p>
	<h2 class="py-8 text-2xl font-black">System (Kafka and Spark)</h2>
	<p class="text-justify">
		The system is composed of two main components: the Kafka pipeline and the Spark job. The Kafka
		pipeline ingests Twitter posts and sends them to the Spark job for processing. The Spark job
		preprocess, analyzes the data and provides instant sentiment prediction.
	</p>
	<p class="text-justify">
		After prediction, the results are stored in a mongodb database for future reference, Then is
		sent back an ID to the user interface for a confirmation. The user can then query the database
		for the results of the job.
	</p>
	<h2 class="py-8 text-2xl font-black">Docker</h2>
	<p class="text-justify">
		The system and API are containerized with Docker to ensure portability and ease of deployment.
		The containers are orchestrated with Docker Compose to manage the system components and their
		dependencies.
	</p>
	<h1 class="py-8 text-4xl font-black">Model</h1>
	<p class="text-justify">
		The sentiment analysis model is a pre-trained Cross-Validation & Logistic Regression model that
		is trained on a dataset of more than 63k tweets. The model is used to predict the sentiment of a
		tweet as either positive, negative, neutral or irrelevant. The model performs with an accuracy
		of 93%.
	</p>
</section>
