<script lang="ts">
	import '$src/app.css';

	import Toolsbar from '$lib/components/organisms/toolsbar.svelte';
</script>

<div class="w-full">
	<Toolsbar />
	<div class="mx-4 flex flex-col items-start gap-4">
		<slot />
	</div>
</div>
