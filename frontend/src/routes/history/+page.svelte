<script lang="ts">
	import { onMount } from 'svelte';
	import type { HistoryItem } from '$lib/types';
	
	let history: HistoryItem[] = [];
	let selected: HistoryItem | null = null;
	let loading = true;
	let error = '';

	onMount(async () => {
		try {
			const res = await fetch('/history');
			if (!res.ok) {
				throw new Error(`Request failed: ${res.status}`);
			}
			const contentType = res.headers.get('content-type') ?? '';
			if (contentType.includes('application/json')) {
				history = await res.json();
			} else {
				const text = await res.text();
				try {
					history = JSON.parse(text);
				} catch {
					throw new Error('History endpoint did not return JSON.');
				}
			}
		} catch (err) {
			const message = err instanceof Error ? err.message : 'Failed to load history.';
			error = message;
		} finally {
			loading = false;
		}
	});

	const selectItem = (item: HistoryItem) => {
		window.location.href = `/chat?convo_id=${encodeURIComponent(item.convo_id)}`;
	};
</script>

<div class="relative">
	<h1 class="text-2xl font-bold mb-4">Conversation History</h1>

	{#if loading}
		<p class="text-sm text-gray-500">Loading…</p>
	{:else if error}
		<p class="text-sm text-red-500">{error}</p>
	{:else if history.length === 0}
		<p class="text-sm text-gray-500">No history yet.</p>
	{:else}
		<ul class="space-y-2">
			{#each history as item (item.convo_id)}
				<li>
					<button
						class="w-full text-left rounded-md border px-3 py-2 hover:bg-red-500 hover:text-black focus:outline-none focus:ring"
						on:click={() => selectItem(item)}
					>
						<div class="text-sm text-gray-500">{item.convo_id}</div>
						<div class="text-base">{item.content}</div>
					</button>
				</li>
			{/each}
		</ul>
	{/if}
</div>
