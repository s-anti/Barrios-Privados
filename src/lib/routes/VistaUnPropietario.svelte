<script>
	let editando = false;
	let eliminando = false;
	let agregandoLote = false;
	let agregandoGasto = false;
	let viendoConsumo = false;
	import EditarPropietario from "../../assets/Forms/EditarPropietario.svelte";
	import PropAgregarLote from "../../assets/Forms/PropAgregarLote.svelte";
	import Modal from "../../assets/Modal.svelte";
	import { dataAhora } from "../../store";
	import { tablasInfo } from "../../store";
	export let params = {};
	import Tabla from "../../assets/Tabla.svelte";
	import ModalConsumos from "../../assets/ModalConsumos.svelte";
	let idEditando = null;
	import { _ } from "svelte-i18n";
	import PropAgregarGasto from "../../assets/Forms/PropAgregarGasto.svelte";
	let dataxd = null;

	const fetchData = async () => {
		console.log("Lmaman data");

		const response = await fetch(
			`http://127.0.0.1:5000/propietarios_lotes/${params.id}`
		);
		const data = await response.json();
		console.log("recibimo,s", data);
		idEditando = data[0][0][0].prop_id;
		dataxd = data;
		dataAhora.set(data);
		return data;
	};

	const enviar = async () => {
		const response = await fetch(
			`http://127.0.0.1:5000/eliminar/propietarios/${$dataAhora[0][0][0].prop_id}`
		);
		const data = response.json();
		data.then((d) => {
			tablasInfo.update((valores) => {
				return {
					...valores,
					propietarios: d,
				};
			});
		});
		window.location.href = "/#/propietarios";
	};

	let columnasLote = {
		id: "lote",
		fechaCompra: "fecha",
		"": "eliminar",
	};

	let columnasGastos = {
		lote: "lote",
		supCub: "metros",
		habitantes: null,
		vehiculos: null,
		luz: "luz",
		agua: "agua",
		gas: "gas",
		mes: "fecha",
	};

	const fetchGastos = async () => {
		const response = await fetch(
			`http://127.0.0.1:5000/prop_lote_mes/${params.id}`
		);
		const data = await response.json();
		console.log("recibimo,s", data);

		return data;
	};

	const funcElimLote = async (idLote) => {
		const response = await fetch(
			`http://127.0.0.1:5000/prop_vende_lote/${params.id}/${idLote}`
		);
		const data = await response.json();
		dataxd = data;
		dataAhora.set(data);
		return data;
	};
</script>

{#await fetchData()}
	<h1>{$_("cargando")}</h1>
{:then data}
	<div class=" p-4">
		<div class=" bg-slate-500 p-4 rounded-lg flex gap-2">
			<div class="bg-slate-600 p-8 rounded-lg">
				<h1 class="text-2xl font-bold pb-4">{$_("propietario")}</h1>

				<div
					class="flex justify-between bg-slate-700 m-2 p-2 rounded-md w-full"
				>
					<p>ID:</p>
					<p>{$dataAhora[0][0][0].prop_id}</p>
				</div>
				<div
					class="flex justify-between bg-slate-700 m-2 p-2 rounded-md w-full"
				>
					<p>{$_("nombre")}:</p>
					<p>{$dataAhora[0][0][1].prop_nombre}</p>
				</div>
				<div
					class="flex justify-between bg-slate-700 m-2 p-2 rounded-md w-full"
				>
					<p>{$_("apellido")}:</p>
					<p>{$dataAhora[0][0][2].prop_apellido}</p>
				</div>

				<div class="flex items-center justify-center p-2">
					<button
						class="mx-3"
						on:click={() => {
							editando = true;
						}}
					>
						<span
							class="p-2 bg-slate-300 rounded-full text-black material-icons-round"
							>edit</span
						>
					</button>

					<button class="mx-3" on:click={() => (eliminando = true)}
						><span
							class="material-icons-round p-2 bg-red-500 rounded-full text-black"
							>close</span
						></button
					>
				</div>
				<div class="flex items-center pt-4 justify-center">
					<button
						on:click={() => (viendoConsumo = true)}
						class="rounded-lg p-2 bg-slate-500">{$_("consumos")}</button
					>
				</div>
			</div>
			<div class="flex flex-col gap-2">
				<div class="bg-slate-600 p-4 rounded-lg">
					<div class="flex items-center justify-between">
						<h1 class="text-2xl font-bold">{$_("lotes")}</h1>
						<button
							on:click={() => (agregandoLote = true)}
							class="flex items-center mb-2 p-2 bg-slate-300 text-black rounded-full"
							><span class="material-icons-round">add</span></button
						>
					</div>

					<Tabla
						columnas={columnasLote}
						funcElim={funcElimLote}
						data={$dataAhora[1]}
					/>
				</div>
				{#await fetchGastos() then dataCons}
					<div class="bg-slate-600 p-4 rounded-lg">
						<div class="flex items-center justify-between">
							<h1 class="text-2xl font-bold">{$_("consumos")}</h1>

							<button
								on:click={() => (agregandoGasto = true)}
								class="flex items-center mb-2 p-2 bg-slate-300 text-black rounded-full"
								><span class="material-icons-round">add</span></button
							>
						</div>
						<Tabla columnas={columnasGastos} data={dataCons} />
					</div>
				{/await}
			</div>
		</div>
	</div>
{/await}
{#if editando}
	<EditarPropietario cerrar={() => (editando = false)} {idEditando} />
{/if}
{#if agregandoLote}
	<PropAgregarLote
		nombre={dataxd[0][0][1].prop_nombre + " " + dataxd[0][0][2].prop_apellido}
		id={idEditando}
		cerrar={() => (agregandoLote = false)}
	/>
{/if}

{#if eliminando}
	<Modal cerrar={() => (eliminando = false)}>
		<div slot="contenido">
			<p>{$_("elimProp")}</p>
			<p>{$_("seguro")}</p>

			<form
				on:submit|preventDefault={enviar}
				class="flex items-center justify-center"
			>
				<button
					class="bg-lime-200 p-2 m-2 rounded-lg"
					on:click={() => (eliminando = false)}
					>{$_("cancelar")}
				</button>

				<button class="bg-red-500 p-2 m-2 font-black rounded-lg" type="submit"
					>{$_("eliminar")}
				</button>
			</form>
		</div>
	</Modal>
{/if}
{#if viendoConsumo}
	<ModalConsumos cerrar={() => (viendoConsumo = false)} id={idEditando} />
{/if}
{#if agregandoGasto}
	<PropAgregarGasto
		id={idEditando}
		nombre={dataxd[0][0][1].prop_nombre + " " + dataxd[0][0][2].prop_apellido}
		cerrar={() => {
			fetchData();
			agregandoGasto = false;
		}}
	/>
{/if}
