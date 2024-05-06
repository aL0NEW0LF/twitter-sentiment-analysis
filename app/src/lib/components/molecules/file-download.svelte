<script lang="ts" context="module">
	import { z } from 'zod';
	export const formSchema = z.object({
		fileType: z.string()
	});
	export type FormSchema = typeof formSchema;
</script>

<script lang="ts">
	import { page } from '$app/stores';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '../ui/label';
	import type { SuperValidated } from 'sveltekit-superforms';
	import { Button } from '../ui/button';
	import { globalData } from '$stores/global-data';
	import * as Select from '$lib/components/ui/select';
	import { get } from 'svelte/store';
	import * as Form from '$lib/components/ui/form';
	export let form: SuperValidated<FormSchema> = $page.data.select;

	async function downloadData(event: Event) {
		const formElement = event.target as HTMLFormElement;

		const formData = new FormData(formElement);

		const data = get(globalData);
		if (data.length === null || data.length === 0 || data === undefined) {
			alert('No data to download');
			return;
		}
		formData.append('data', JSON.stringify(data));

		const response = await fetch(formElement.action, {
			method: 'POST',
			body: formData
		});

		const blob = await response.blob();
		console.log(blob);
		const url = window.URL.createObjectURL(blob);
		console.log(url);
		const link = document.createElement('a');
		link.target = '_blank';
		link.href = url;
		link.download = 'data';
		link.click();
	}
</script>

<Form.Root
	{form}
	schema={formSchema}
	let:config
	method="POST"
	action="http://127.0.0.1:5000/process/file/download"
	class="w-2/3 space-y-6"
>
	<Form.Field {config} name="fileType">
		<Form.Item>
			<Form.Label>File download</Form.Label>
			<Form.Select>
				<Form.SelectTrigger class="w-96" placeholder="File type" />
				<Form.SelectContent>
					<Form.SelectItem value="excel">.xlsx</Form.SelectItem>
					<Form.SelectItem value="csv">.csv</Form.SelectItem>
					<Form.SelectItem value="json">.json</Form.SelectItem>
					<Form.SelectItem value="txt">.txt</Form.SelectItem>
					<Form.SelectItem value="pdf">.pdf</Form.SelectItem>
				</Form.SelectContent>
			</Form.Select>
			<Form.Validation />
		</Form.Item>
	</Form.Field>
	<Form.Button class="w-96" variant="outline" type="submit">Download data</Form.Button>
</Form.Root>
