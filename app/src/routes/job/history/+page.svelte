<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.ts';
	import * as Dialog from '$lib/components/ui/dialog/index.ts';
	import ChevronRight from 'lucide-svelte/icons/chevron-right';
	import { Button, buttonVariants } from '$lib/components/ui/button/index.ts';
	import { Input } from '$lib/components/ui/input/index.ts';
	import { Label } from '$lib/components/ui/label/index.ts';
	import { Skeleton } from '$lib/components/ui/skeleton/index.js';
	import { error } from '@sveltejs/kit';
	import type { PageData } from './$types';

	async function fetchHistory() {
		const response = await fetch('http://127.0.0.1:5000/jobs/history', { method: 'POST' });
		const jobs = await response.json();

		console.log(jobs);
		return jobs;
	}
</script>

<Table.Root>
	<Table.Caption>A list of your predictions history.</Table.Caption>
	<Table.Header>
		<Table.Row>
			<Table.Head class="w-96">ID</Table.Head>
			<Table.Head>timestamp</Table.Head>
			<Table.Head>type</Table.Head>
			<Table.Head></Table.Head>
		</Table.Row>
	</Table.Header>
	{#await fetchHistory()}
		<Table.Body>
			<Table.Row>
				<Table.Cell class="w-[32.25%]">
					<Skeleton class="h-4 w-full" />
				</Table.Cell>
				<Table.Cell class="w-[32.25%]">
					<Skeleton class="h-4 w-full" />
				</Table.Cell>
				<Table.Cell class="w-[32.25%]">
					<Skeleton class="h-4 w-full" />
				</Table.Cell>
				<Table.Cell class="w-14">
					<Skeleton class="h-4 w-full" />
				</Table.Cell>
			</Table.Row>
		</Table.Body>
	{:then jobs}
		<Table.Body>
			{#each jobs as job, i (i)}
				<Table.Row>
					<Table.Cell class="w-1/3 font-medium">{job.job_id}</Table.Cell>
					<Table.Cell class="w-1/3">{job.timestamp}</Table.Cell>
					<Table.Cell class="w-1/3">{job.type}</Table.Cell>
					<Table.Cell class="w-14">
						<Button variant="outline" size="icon" href="/job/history/{job.job_id}">
							<ChevronRight class="h-4 w-4" />
						</Button>
					</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</Table.Root>
