<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Label } from '../ui/label';
	import { Button } from '../ui/button';
	import Textarea from '../ui/textarea/textarea.svelte';

	/*async function loadData(event: Event) {
		const formElement = event.target as HTMLFormElement;

		const formData = new FormData(formElement);

		const response = await fetch(formElement.action, {
			method: 'POST',
			body: formData
		});

		const responseData = await response.json();
		globalData.set(responseData);
	}*/
</script>

<form
	method="post"
	action="http://127.0.0.1:5000/predict/text/"
	enctype="multipart/form-data"
	class="flex flex-col gap-4"
>
	<Label>Text</Label>
	<Textarea class="w-96" id="data" name="data" placeholder="Enter text here" required />
	<Button class="" variant="outline" type="submit">Upload data</Button>
</form>
