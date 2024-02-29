<script lang="ts">
	import Icon from '@iconify/svelte';

	const ALLOWED_FILE_TYPES = ['image/png', 'image/jpeg'];
	let selectedFile: File | null;
	let carPlates: Record<string, string>[] = [];
	let error: string | null;

	async function handleSelect() {
		error = null;
		let input = document.createElement('input');
		input.type = 'file';
		input.multiple = false;
		input.accept = ALLOWED_FILE_TYPES.join(',');

		input.onchange = () => {
			const file = input.files?.[0];
			if (!file) return;
			selectedFile = file;
		};

		input.click();
	}

	async function handleDrop(event: DragEvent) {
		event.preventDefault();
		error = null;

		const files = event.dataTransfer?.files;
		if (!files) return;
		if (files.length > 1) {
			error = 'Only one file is allowed';
			return;
		}

		const file = files[0];
		if (!ALLOWED_FILE_TYPES.includes(file.type)) {
			error = 'Invalid file type. Only JPEG and PNG are allowed.';
			return;
		}

		selectedFile = file;
	}

	async function unselect() {
		selectedFile = null;
		error = null;
		carPlates = [];
	}

	async function handleSubmit() {
		if (!selectedFile) return;
		error = null;

		const formData = new FormData();
		formData.append('file', selectedFile);

		try {
			const response = await fetch('http://127.0.0.1:5000/recognize', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				throw new Error('Failed to recognize the car plate');
			}

			if (response.status === 204) {
				throw new Error('No car plate found');
			}

			const data = await response.json();
			carPlates = data.car_numbers;
		} catch (e) {
			error = 'Failed to recognize the car plate';
		}
	}
</script>

<main class="flex flex-auto flex-col items-center justify-center">
	<button
		on:click={handleSelect}
		on:drop={handleDrop}
		on:dragover|preventDefault
		class:hidden={!!selectedFile}
		class="grid h-44 w-full max-w-96 content-center rounded-md border-2 border-dashed border-gray-500"
	>
		<Icon icon="material-symbols:upload" class="mx-auto text-4xl text-gray-500" />
		Drop image here
		<span class="text-gray-400">- or -</span>
		Click to upload
	</button>

	{#if selectedFile}
		<div class="max-w-screen-lg">
			<div class="overflow-hidden rounded-md text-center">
				<img class="max-h-[36rem]" src={URL.createObjectURL(selectedFile)} alt="selected" />
				<button on:click={unselect} class="w-full bg-red-500 py-1 font-semibold text-white">
					Remove
				</button>
			</div>
			<button on:click={handleSubmit} class="mt-4 w-full rounded-md bg-blue-500 py-2 text-white">
				Submit
			</button>
		</div>
	{/if}
	<div class:hidden={!error} class="mt-4 text-center text-red-500">{error}</div>

	<h2 class:hidden={carPlates}>Detected</h2>

	{#each carPlates as plate}
		<div class="mt-4 rounded-md border-2 border-gray-500 text-center">
			<div class="max-w-96 overflow-hidden rounded-md">
				<img
					src="data:image/jpeg;base64,{plate.image}"
					alt="car plate"
					class="w-full"
				/>
                <span class="text-4xl">{plate.text}</span>
			</div>
		</div>
	{/each}
</main>
