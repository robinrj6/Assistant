<script lang="ts">
	import { Spinner } from "flowbite-svelte";


	let messages: string[] = [];
	let loading = false;
	let convoId: string | null = null;
	
	async function fetchChat(prompt: string) {
		if (!prompt.trim()) return;
		loading = true;
		messages = prompt !== 'hello!' ? [...messages,'󱟄 : '+ prompt] : [];
		let currentMsg = '';
		
		const requestBody: any = { prompt };
		if (convoId) {
			requestBody.convo_id = convoId;
		}
		const bodyStr = JSON.stringify(requestBody);
		
		const res = await fetch('/chat', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: bodyStr
		});

		if (!res.body) { loading = false; return; }

		const reader = res.body.getReader();
		const decoder = new TextDecoder();
		let buffer = '';

		while (true) {
			const { done, value } = await reader.read();
			if (done) break;

			buffer += decoder.decode(value, { stream: true });
			const parts = buffer.split('\n');
			buffer = parts.pop() ?? '';

			for (const part of parts) {
				const trimmed = part.trim();
				if (!trimmed) continue;
				const obj = JSON.parse(trimmed);
				// Handle convo_id on first message
				if (obj.convo_id) {
					convoId = obj.convo_id;
				} else if (obj.response) {
					currentMsg += obj.response;
				}
			}
		}

		// Flush any remaining buffered data
		if (buffer.trim()) {
			const obj = JSON.parse(buffer.trim());
			if (obj.convo_id) {
				convoId = obj.convo_id;
			} else if (obj.response) {
				currentMsg += obj.response;
			}
		}
		
		// Add the complete response as a new message
		messages =  [...messages, '󱚣 > '+currentMsg];
		loading = false;
	}
</script>

<div class="relative">
	{#if loading}
		<div class="pointer-events-none absolute inset-0 flex items-start justify-center pt-4 z-50">
			<Spinner type="pulse" />		
		</div>	
	{/if}

	<div class="messages-container overflow-y-scroll mb-24 p-4 max-h-[70vh]">
		{#each messages as msg, i (i)}
			<p class="text-[1.2rem] text-red-500 ">{msg}</p>
		{/each}
	</div>

	<div class="fixed inset-x-0 bottom-0 flex items-center justify-center gap-5 p-4">
		<button class="border-2 p-4 hover:bg-red"
			on:click={() => {
				window.location.reload();
			}}>New Chat</button>
		<textarea id="messageInput" placeholder="Type your message..." style="width: 80%; height: 10rem; background-color: #3d0109;"></textarea>
		<button class="border-2 p-4 hover:bg-red"
			on:click={() => {
				const input = document.getElementById('messageInput') as HTMLTextAreaElement;
				fetchChat(input.value);
				input.value = '';
			}}>Send</button>
	</div>
</div>

