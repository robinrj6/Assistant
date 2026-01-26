<script>
	import { onMount } from 'svelte';

	/** @type {string} */
	let startMsg = '';
	let errorMsg = '';

	async function hello() {
		try {
			const response = await fetch('/chat');
			const data = await response.json();
			if (data.error) {
				errorMsg = data.error;
				startMsg = 'Error: ' + data.error;
			} else {
				startMsg = data.message ?? 'No message';
			}
		} catch (err) {
			errorMsg = err instanceof Error ? err.message : 'Unknown error';
			startMsg = 'Error: ' + errorMsg;
		}
	}

	onMount(() => {
	    hello();
	});
</script>

<p>
    {startMsg}
</p>

<style>
    p {
        font-size: 1.2em;
        color: red;
    }
</style>