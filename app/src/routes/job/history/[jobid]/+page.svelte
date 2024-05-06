<script>
	import { page } from '$app/stores';

	$: console.log($page.params);
</script>

Job {$page.params.jobid} details
