<template>
	<div>
		<center>
			<b-button v-b-modal.modal-1>Aggiungi Dispositivo</b-button>
		</center>
		<b-modal id="modal-1" title="Aggiungi Dispositivo">
			<b-form @submit="onSubmit" @reset="onReset">
			<b-form-group
				id="input-group-1"
				label="Nome:"
				label-for="input-1"
			>
			<b-form-input id="input-2" v-model="form.namel"></b-form-input>
			</b-form-group>
						<b-form-group
				id="input-group-2"
				label="Descrizione:"
				label-for="input-2"
			>
				<b-form-input id="input-2" v-model="form.descrizione"></b-form-input>
			</b-form-group>

		</b-form>
		</b-modal>
	</div>
</template>

<script>
export default {
	data() {
		return {

			form: {
				name: '',
				description: '',
				pin: '',
				type: ''
			}
		};
	}
};
</script>
