<script lang="ts">
	import * as Menubar from '$lib/components/ui/menubar';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import Textarea from '../ui/textarea/textarea.svelte';
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { Button } from '../ui/button';
	import { Input } from '$lib/components/ui/input';
	import Spinner from '../atoms/spinner.svelte';

	let formLoading = false;
	$: formLoading;
	let TextInputDialogOpen = false;
	$: TextInputDialogOpen;
	let FileUploadDialogOpen = false;
	$: FileUploadDialogOpen;
	let MenuBarOpen = false;
	$: MenuBarOpen;

	async function predictText(event: Event) {
		formLoading = true;
		const formElement = event.target as HTMLFormElement;

		const formData = new FormData(formElement);

		const response = await fetch(formElement.action, {
			method: 'POST',
			body: formData
		});

		const responseData = await response.json();

		formLoading = false;
		TextInputDialogOpen = false;
		MenuBarOpen = false;
		goto(`/job/history/${responseData.job_id}`);
	}

	async function predictFile(event: Event) {
		formLoading = true;
		const formElement = event.target as HTMLFormElement;

		const formData = new FormData(formElement);

		const response = await fetch(formElement.action, {
			method: 'POST',
			body: formData
		});

		const responseData = await response.json();

		formLoading = false;
		FileUploadDialogOpen = false;
		MenuBarOpen = false;
		goto(`/job/history/${responseData.job_id}`);
	}
</script>

<div class="m-fit p-4">
	<Menubar.Root class="w-fit">
		<Menubar.Menu bind:open={MenuBarOpen}>
			<Menubar.Trigger>Options</Menubar.Trigger>
			<Menubar.Content>
				<Menubar.Item href="/">Home</Menubar.Item>
				<Menubar.Item href="/job/history">History</Menubar.Item>
				<Menubar.Sub>
					<Menubar.SubTrigger>Predict</Menubar.SubTrigger>
					<Menubar.SubContent>
						<Dialog.Root bind:open={TextInputDialogOpen}>
							<Dialog.Trigger
								class="hover:bg-accent hover:text-accent-foreground relative flex cursor-pointer select-none items-center rounded-sm fill-white px-2 py-1.5 text-sm outline-none disabled:pointer-events-none disabled:opacity-50"
								>With Text</Dialog.Trigger
							>
							<Dialog.Content class="w-96 fill-white">
								<Dialog.Header>
									<Dialog.Title class="text-white">Predict With Text</Dialog.Title>
								</Dialog.Header>
								{#if formLoading}
									<div class="flex w-full justify-center"><Spinner color="gray" /></div>
								{:else}
									<form
										method="post"
										action="http://127.0.0.1:5000/predict/text/"
										enctype="multipart/form-data"
										class="flex flex-col gap-4"
										on:submit|preventDefault={predictText}
									>
										<Textarea
											class="w-full text-white"
											id="textdata"
											name="textdata"
											placeholder="Enter text here"
											required
										/>
										<Button class="text-white" variant="outline" type="submit">Upload data</Button>
									</form>
								{/if}
							</Dialog.Content>
						</Dialog.Root>
						<Dialog.Root bind:open={FileUploadDialogOpen}>
							<Dialog.Trigger
								class="hover:bg-accent hover:text-accent-foreground relative flex cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none disabled:pointer-events-none disabled:opacity-50"
								>With File</Dialog.Trigger
							>
							<Dialog.Content class="w-96">
								<Dialog.Header>
									<Dialog.Title class="text-white">Predict With File</Dialog.Title>
								</Dialog.Header>
								{#if formLoading}
									<div class="flex w-full justify-center"><Spinner color="gray" /></div>
								{:else}
									<form
										method="post"
										action="http://127.0.0.1:5000/predict/file/"
										enctype="multipart/form-data"
										class="flex flex-col gap-4"
										on:submit|preventDefault={predictFile}
									>
										<Input
											class="w-full text-white"
											id="datafile"
											name="datafile"
											type="file"
											required
										/>
										<Button class="text-white" variant="outline" type="submit">Upload data</Button>
									</form>
								{/if}
							</Dialog.Content>
						</Dialog.Root>
					</Menubar.SubContent>
				</Menubar.Sub>
			</Menubar.Content>
		</Menubar.Menu>
	</Menubar.Root>
</div>
