<script>
	import Dropzone from "svelte-file-dropzone";
	import App from "../../client/src/App.svelte";

	let files = {
		accepted: [],
		rejected: [],
	};

	function handleFilesSelect(e) {
		const { acceptedFiles, fileRejections } = e.detail;
		files.accepted = [...files.accepted, ...acceptedFiles];
		files.rejected = [...files.rejected, ...fileRejections];
	}

	function upload() {
		const formData = new FormData();
		formData.append("files", files.accepted[0]);
		for (var i = 0; i < files.accepted.length; i++) {
			formData.append("files", files.accepted[i]);
		}
		const upload = fetch("/file", {
			method: "POST",
			body: formData,
		})
			.then((response) => response.json())
			.then((result) => {
				console.log("Success:", result);
			})
			.catch((error) => {
				console.error("Error:", error);
			});
	}
</script>

<head />
<main>
	<h1>USDZ Converter</h1>

	<body>
		<div class="dropzone">
			<Dropzone
				on:drop={handleFilesSelect}
			/>
			<ol>
				{#each files.accepted as item}
					<li>{item.name}</li>
				{/each}
			</ol>
		</div>

		{#if files.accepted.length > 0}
			<button on:click={upload}>Submit</button>
		{:else}
			<button disabled>Submit</button>
		{/if}
	</body>
	<footer>
		<p>Created by Keenan Gray and Patrick Lynch</p>
	</footer>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #020202;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
	footer {
		position: absolute;
		bottom: 0;
		width: 100%;
		height: 2.5rem;
	}
</style>
