<script>
	import logo from '$lib/images/ml2.png';
	import Github from '$lib/icons/github.svelte';
</script>

<div class="h-auto w-auto p-4 gap-4 flex flex-row flex-grow flex-basis-0 items-center">
	<a href="/" class="flex flex-row items-center gap-4"
		><img src={logo} alt="" class="h-20" />
		<p class="text-2xl font-bold h-min whitespace-nowrap">Data Playground</p></a
	>

	<div class="relative w-auto ml-auto">
		<a
			href="https://github.com/aL0NEW0LF/data-playground"
			aria-label="Homepage"
			title="Github repository"
			target="_blank"
		>
			<Github class="fill-white w-min h-8" />
		</a>
	</div>
</div>
