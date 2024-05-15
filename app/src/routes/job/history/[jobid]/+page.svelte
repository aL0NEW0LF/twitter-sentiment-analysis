<script lang="ts">
	import { page } from '$app/stores';
	import * as Table from '$lib/components/ui/table/index.ts';
	import * as Dialog from '$lib/components/ui/dialog/index.ts';
	import ChevronRight from 'lucide-svelte/icons/chevron-right';
	import { Button, buttonVariants } from '$lib/components/ui/button/index.ts';
	import { Input } from '$lib/components/ui/input/index.ts';
	import { Label } from '$lib/components/ui/label/index.ts';
	import { Skeleton } from '$lib/components/ui/skeleton/index.js';
	import { onMount } from 'svelte';

	$: job_id = $page.params.jobid;

	async function fetchJobDetails(job_id: string) {
		const response = await fetch(`http://127.0.0.1:5000/jobs/${job_id}`, {
			method: 'POST'
		});
		const jobDetails = await response.json();
		console.log(jobDetails);
		return jobDetails;
	}
</script>

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
