<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.ts';
	import * as Dialog from '$lib/components/ui/dialog/index.ts';
	import ChevronRight from 'lucide-svelte/icons/chevron-right';
	import { Button, buttonVariants } from '$lib/components/ui/button/index.ts';
	import { Input } from '$lib/components/ui/input/index.ts';
	import { Label } from '$lib/components/ui/label/index.ts';
	const invoices = [
		{
			id: 1,
			timestamp: '2021-10-01 12:00:00',
			type: 'text'
		},
		{
			id: 2,
			timestamp: '2021-10-01 12:00:00',
			type: 'file'
		},
		{
			id: 3,
			timestamp: '2021-10-01 12:00:00',
			type: 'text'
		},
		{
			id: 4,
			timestamp: '2021-10-01 12:00:00',
			type: 'file'
		},
		{
			id: 5,
			timestamp: '2021-10-01 12:00:00',
			type: 'text'
		},
		{
			id: 6,
			timestamp: '2021-10-01 12:00:00',
			type: 'file'
		},
		{
			id: 7,
			timestamp: '2021-10-01 12:00:00',
			type: 'text'
		},
		{
			id: 8,
			timestamp: '2021-10-01 12:00:00',
			type: 'file'
		},
		{
			id: 9,
			timestamp: '2021-10-01 12:00:00',
			type: 'text'
		},
		{
			id: 10,
			timestamp: '2021-10-01 12:00:00',
			type: 'file'
		},
		{
			id: 11,
			timestamp: '2021-10-01 12:00:00',
			type: 'text'
		},
		{
			id: 12,
			timestamp: '2021-10-01 12:00:00',
			type: 'file'
		},
		{
			id: 13,
			timestamp: '2021-10-01 12:00:00',
			type: 'text'
		},
		{
			id: 14,
			timestamp: '2021-10-01 12:00:00',
			type: 'file'
		},
		{
			id: 15,
			timestamp: '2021-10-01 12:00:00',
			type: 'text'
		},
		{
			id: 16,
			timestamp: '2021-10-01 12:00:00',
			type: 'file'
		}
	];
</script>

<Table.Root>
	<Table.Caption>A list of your predictions history.</Table.Caption>
	<Table.Header>
		<Table.Row>
			<Table.Head class="w-72">ID</Table.Head>
			<Table.Head>timestamp</Table.Head>
			<Table.Head>type</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each invoices as invoice, i (i)}
			<Table.Row>
				<Table.Cell class="w-72 font-medium">{invoice.id}</Table.Cell>
				<Table.Cell>{invoice.timestamp}</Table.Cell>
				<Table.Cell>{invoice.type}</Table.Cell>
				<Table.Cell class="w-10">
					<Button variant="outline" size="icon" href="/job/history/{invoice.id}">
						<ChevronRight class="h-4 w-4" />
					</Button>
				</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>
