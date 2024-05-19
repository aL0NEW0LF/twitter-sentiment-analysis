<script lang="ts">
	import { page } from '$app/stores';
	import * as Table from '$lib/components/ui/table/index.ts';
	import * as Dialog from '$lib/components/ui/dialog/index.ts';
	import { Button } from '$lib/components/ui/button/index.ts';
	import { Skeleton } from '$lib/components/ui/skeleton/index.js';
	import Spinner from '$lib/components/atoms/spinner.svelte';
	import { Bar } from 'svelte-chartjs';
	import { Chart, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

	Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

	$: job_id = $page.params.jobid;

	async function fetchJobDetails(job_id: string) {
		const response = await fetch(`http://127.0.0.1:5000/jobs/${job_id}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		const jobDetails = await response.json();
		return jobDetails;
	}

	async function fetchPredictionsCount(job_id: string) {
		const response = await fetch(`http://127.0.0.1:5000/jobs/${job_id}/count`, { method: 'POST' });

		const predictions = await response.json();

		const data = {
			labels: ['Irrelevant', 'Negative', 'Neutral', 'Positive'],
			datasets: [
				{
					label: 'Predictions',
					data: predictions,
					backgroundColor: [
						'rgba(255, 255, 255, 1)',
						'rgba(255, 255, 255, 1)',
						'rgba(255, 255, 255, 1)',
						'rgba(255, 255, 255, 1)'
					]
				}
			]
		};

		return data;
	}
</script>

<Dialog.Root>
	<Dialog.Trigger><Button variant="outline">Predictions count</Button></Dialog.Trigger>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header>
			<Dialog.Title>Predictions count</Dialog.Title>
			<Dialog.Description>Here is a chart of the predictions count.</Dialog.Description>
		</Dialog.Header>
		{#await fetchPredictionsCount(job_id)}
			<div class="flex w-full justify-center"><Spinner color="gray" class="w-12" /></div>
		{:then data}
			<Bar {data} />
		{:catch error}
			<p style="color: red">{error.message}</p>
		{/await}
	</Dialog.Content>
</Dialog.Root>

<Table.Root>
	<Table.Caption>A list of your predictions history.</Table.Caption>
	<Table.Header>
		<Table.Row>
			<Table.Head class="w-1/2">text</Table.Head>
			<Table.Head class="w-1/2">probability</Table.Head>
			<Table.Head class="w-40">prediction</Table.Head>
		</Table.Row>
	</Table.Header>
	{#await fetchJobDetails(job_id)}
		<Table.Body>
			<Table.Row>
				<Table.Cell class="w-1/2">
					<Skeleton class="h-4 w-full" />
				</Table.Cell>
				<Table.Cell class="w-1/2">
					<Skeleton class="h-4 w-full" />
				</Table.Cell>
				<Table.Cell class="w-40">
					<Skeleton class="h-4 w-full" />
				</Table.Cell>
			</Table.Row>
		</Table.Body>
	{:then jobDetails}
		<Table.Body>
			{#each jobDetails as jobDetail}
				<Table.Row>
					<Table.Cell class="w-1/2">{jobDetail.text}</Table.Cell>
					<Table.Cell class="w-1/2">
						<p>Irrelevant: {JSON.parse(jobDetail.probability)[0]}</p>
						<p>Negative: {JSON.parse(jobDetail.probability)[1]}</p>
						<p>Neutral: {JSON.parse(jobDetail.probability)[2]}</p>
						<p>Positive: {JSON.parse(jobDetail.probability)[3]}</p>
					</Table.Cell>
					<Table.Cell class="w-40">{jobDetail.prediction}</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</Table.Root>
