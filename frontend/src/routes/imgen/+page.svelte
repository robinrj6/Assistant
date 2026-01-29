<script lang="ts">
	import { Spinner } from "flowbite-svelte";
	let messages: string[] = [];
	let loading = false;
	let controlnet = false;
	let generatedImagePath: string | null = null;
	
	async function fetchImgGen(formData: FormData) {
		loading = true;
		generatedImagePath = null;
		messages = [...messages, '󱟄 :'+ formData.get('prompt')];
		const res = await fetch('/imgen', {
			method: 'POST',
			body: formData
		});

		const data = await res.json();
		
		if (data.error) {
			messages = [...messages, '󱚣 > Error: ' + data.error];
		} else if (data.file_path) {
			generatedImagePath = data.file_path;
			messages = [...messages, '󱚣 > Image generated!'];
		}
		
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
		{#if generatedImagePath}
			<div class="mt-4">
				<img src={`/api/image?path=${encodeURIComponent(generatedImagePath)}`} alt="Generated" class="max-w-[80vw] rounded-md" />
			</div>
		{/if}
	</div>

	<form class="fixed inset-x-0 bottom-0 flex gap-2 p-4" onsubmit={(e) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        formData.set('seed', '123456789');
        formData.set('steps', '20');
        formData.set('guidance_scale', '7.5');
        formData.set('use_controlnet', controlnet.toString());
        fetchImgGen(formData);
        e.currentTarget.reset();
    }} method="POST">
        <div class="flex flex-col w-full gap-y-4">
            <div>
                <label for="controlnet">With Conditioning image?</label>
                <input type="checkbox" name="controlnet" id="controlnet" bind:checked={controlnet} />
            </div>
			{#if controlnet}
				<div>
					<label for="Cimage">Upload Conditioning Image:</label>
					<input type="file" name="Cimage" id="Cimage" accept="image/*" />
				</div>  
			{/if}
            <textarea id="prompt" name="prompt" placeholder="Type your prompt here..." style="width: 80vw; height: 10rem; background-color: #3d0109;"></textarea>
        </div>
		<input type="submit" value="Send" class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 cursor-pointer w-[20vw]" />
        </form>
</div>

