<script>
	import { page } from '$app/stores';
	import * as Table from '$lib/components/ui/table/index.ts';

	const dummy_tweets = [
		{
			id: 3364,
			company: 'Facebook',
			sentiment: 'Irrelevant',
			tweet:
				'I mentioned on Facebook that I was struggling for motivation to go for a run the other day, which has been translated by Tom’s great auntie as ‘Hayley can’t get out of bed’ and told to his grandma, who now thinks I’m a lazy, terrible person 🤣',
			prediction: 'Irrelevant'
		},
		{
			id: 352,
			company: 'Amazon',
			sentiment: 'Neutral',
			tweet:
				"BBC News - Amazon boss Jeff Bezos rejects claims company acted like a 'drug dealer' bbc.co.uk/news/av/busine…",
			prediction: 'Neutral'
		},
		{
			id: 8312,
			company: 'Microsoft',
			sentiment: 'Negative',
			tweet:
				'@Microsoft Why do I pay for WORD when it functions so poorly on my @SamsungUS Chromebook? 🙄',
			prediction: 'Irrelevant'
		},
		{
			id: 4371,
			company: 'CS-GO',
			sentiment: 'Negative',
			tweet: "CSGO matchmaking is so full of closet hacking, it's a truly awful game.",
			prediction: 'Neutral'
		},
		{
			id: 4433,
			company: 'Google',
			sentiment: 'Neutral',
			tweet:
				'Now the President is slapping Americans in the face that he really did commit an unlawful act after his  acquittal! From Discover on Google vanityfair.com/news/2020/02/t…',
			prediction: 'Neutral'
		},
		{
			id: 6273,
			company: 'FIFA',
			sentiment: 'Negative',
			tweet:
				'Hi @EAHelp I’ve had Madeleine McCann in my cellar for the past 13 years and the little sneaky thing just escaped whilst I was loading up some fifa points, she took my card and I’m having to use my paypal account but it isn’t working, can you help me resolve it please?',
			prediction: 'Negative'
		}
	];

	$: console.log($page.params);
</script>

<div class="flex flex-col gap-4">
	Job {$page.params.jobid} details

	<Table.Root>
		<Table.Caption>Prediction job details.</Table.Caption>
		<Table.Header>
			<Table.Row>
				<Table.Cell class="w-12">ID</Table.Cell>
				<Table.Cell class="w-24">Company</Table.Cell>
				<Table.Cell class="w-24">Sentiment</Table.Cell>
				<Table.Cell>Tweet</Table.Cell>
				<Table.Cell class="w-24">Prediction</Table.Cell>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each dummy_tweets as dummy_tweet, i (i)}
				<Table.Row>
					<Table.Cell class="w-12">{dummy_tweet.id}</Table.Cell>
					<Table.Cell class="w-24">{dummy_tweet.company}</Table.Cell>
					<Table.Cell class="w-24">{dummy_tweet.sentiment}</Table.Cell>
					<Table.Cell>{dummy_tweet.tweet}</Table.Cell>
					<Table.Cell class="w-24">{dummy_tweet.prediction}</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
</div>
