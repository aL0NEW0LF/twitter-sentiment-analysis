<script lang="ts">
	import * as Menubar from '$lib/components/ui/menubar';
</script>

<div class="m-fit p-4">
	<Menubar.Root class="w-fit">
		<Menubar.Menu>
			<Menubar.Trigger>Options</Menubar.Trigger>
			<Menubar.Content>
				<Menubar.Sub>
					<Menubar.SubTrigger>Predict</Menubar.SubTrigger>
					<Menubar.SubContent>
						<Menubar.Item href="/job/text">With Text</Menubar.Item>
						<Menubar.Item href="/job/file">With File</Menubar.Item>
					</Menubar.SubContent>
				</Menubar.Sub>
				<Menubar.Item href="/job/history">History</Menubar.Item>
			</Menubar.Content>
		</Menubar.Menu>
	</Menubar.Root>
</div>
