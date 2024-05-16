<script>
	import { Button } from '$lib/components/ui/button';
	import '$src/app.css';
	import './styles.css';

	import logo from '$lib/assets/school.png';
</script>

<svelte:head>
	<title>Twitter Sentiment Analysis</title>
	<meta name="description" content="Twitter Sentiment Analysis" />
</svelte:head>

<section class="flex w-8/12 flex-col items-center justify-center">
	<div class="my-96 flex flex-row items-center justify-center gap-8">
		<div class="flex flex-col items-center justify-center gap-8">
			<div class="w-full text-justify">
				Empower your insights with real-time sentiment analysis! Our Kafka and Spark-powered system
				seamlessly analyzes Twitter posts, providing instant predictions and historical trends at
				your fingertips. Dive into the pulse of social sentiment like never before.
			</div>
			<Button class="" variant="outline" href="/job">Get started</Button>
		</div>
		<div class="">
			<img src={logo} alt="Hero" class="w-96" />
		</div>
	</div>
</section>
