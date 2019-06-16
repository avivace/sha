<template>
	<div>
		<center>
			  <b-spinner v-if="loading" label="Spinning"></b-spinner>
			<template v-for="piano in overview">
				<h3>{{ piano.description }}</h3>

				<template v-for="stanza in piano.stanze">
					<div>
						<b-card
							style="max-width: 80%;"
							border-variant="light"
							bg-variant="light"
							text-variant="black"
							:header="stanza.description"
							class="text-center"
							align="center"
						>
							<b-card-text>
								<b-card-group deck>
									<template
										v-for="attuatore in stanza.attuatori"
									>
										<div class="col-md-4">
											<b-card
												style=""
												bg-variant="default"
												text-variant="black"
												class="text-center"
												align="center"
											>
												<b-card-title>
													{{ attuatore.description }}
												</b-card-title>
												<b-card-text>
													<b-button
														squared
														class="fsloat-right"
														:variant="
															[
																'outline-danger',
																'success'
															][attuatore.status]
														"
														@click="
															toggle(
																attuatore.id,
																attuatore.status
															)
														"
														>{{
															["OFF", "ON"][
																attuatore.status
															]
														}}</b-button
													>
													<br /><br />
													<b-badge>{{
														attuatore.type
													}}</b-badge>

													PIN<code>
														{{
															attuatore.pin
														}}</code
													>
												</b-card-text>
											</b-card>
										</div>
									</template>
								</b-card-group>
							</b-card-text>
						</b-card>
					</div>
				</template>
			</template>

			<b-button @click="modal = true">Aggiungi Dispositivo</b-button
			>&nbsp;
			<b-button @click="modalpiano = true">Aggiungi Piano</b-button>&nbsp;
			<b-button @click="modalstanza = true">Aggiungi Camera</b-button>
			<br />
		</center>

		<b-modal v-model="modalstanza" id="modal-3" title="Aggiungi Stanza">
			<b-form @submit="addStanza">
				<b-form-group
					id="input-group-2"
					label="Descrizione:"
					label-for="input-2"
				>
					<b-form-input
						id="input-2"
						v-model="formStanza.description"
					></b-form-input>
				</b-form-group>
			</b-form>
			<b-form-group id="input-group-2" label="Piano:" label-for="input-2">
				<b-form-select
					id="input-2"
					v-model="formStanza.piano_id"
					@change="onChangePiano()"
					:options="
						overview.map(element => {
							return {
								text: element['description'],
								value: element['id']
							};
						})
					"
				></b-form-select>
			</b-form-group>
			<div slot="modal-footer" class="w-100">
				<b-button
					style="margin-left:10px"
					variant="primary"
					class="float-right"
					@click="addStanza"
				>
					Conferma
				</b-button>
				&nbsp;
				<b-button
					style="margin-left:10px"
					variant="outline-primary"
					class="float-right"
					@click="modalstanza = false"
				>
					Annulla
				</b-button>
			</div>
		</b-modal>

		<b-modal v-model="modalpiano" id="modal-2" title="Aggiungi Piano">
			<b-form @submit="onSubmit">
				<b-form-group
					id="input-group-2"
					label="Descrizione:"
					label-for="input-2"
				>
					<b-form-input
						id="input-2"
						v-model="formPiano.description"
					></b-form-input>
				</b-form-group>
			</b-form>
			<div slot="modal-footer" class="w-100">
				<b-button
					style="margin-left:10px"
					variant="primary"
					class="float-right"
					@click="addPiano"
				>
					Conferma
				</b-button>
				&nbsp;
				<b-button
					style="margin-left:10px"
					variant="outline-primary"
					class="float-right"
					@click="modalpiano = false"
				>
					Annulla
				</b-button>
			</div>
		</b-modal>

		<b-modal v-model="modal" id="modal-1" title="Aggiungi Dispositivo">
			<b-form @submit="onSubmit">
				<b-form-group
					id="input-group-1"
					label="PIN:"
					label-for="input-1"
				>
					<b-form-input
						id="input-2"
						v-model="form.pin"
						type="number"
					></b-form-input>
				</b-form-group>
				<b-form-group
					id="input-group-2"
					label="Descrizione:"
					label-for="input-2"
				>
					<b-form-input
						id="input-2"
						v-model="form.description"
					></b-form-input>
				</b-form-group>
				<b-form-group
					id="input-group-2"
					label="Piano:"
					label-for="input-2"
				>
					<b-form-select
						id="input-2"
						v-model="form.piano"
						@change="onChangePiano()"
						:options="
							overview.map(element => {
								return {
									text: element['description'],
									value: element['id']
								};
							})
						"
					></b-form-select>
				</b-form-group>
				<b-form-group
					id="input-group-2"
					label="Stanza:"
					label-for="input-2"
				>
					<b-form-select
						id="input-2"
						v-model="form.stanza"
						:options="stanzaOptions"
					></b-form-select>
				</b-form-group>
			</b-form>
			<div slot="modal-footer" class="w-100">
				<b-button
					style="margin-left:10px"
					variant="primary"
					class="float-right"
					@click="onSubmit"
				>
					Conferma
				</b-button>
				&nbsp;
				<b-button
					style="margin-left:10px"
					variant="outline-primary"
					class="float-right"
					@click="modal = false"
				>
					Annulla
				</b-button>
			</div>
		</b-modal>
	</div>
</template>

<script>
import axiosAuth from "@/api/axios-auth";

export default {
	data() {
		return {
			loading: false,
			modal: false,
			modalstanza: false,
			modalpiano: false,
			stanzaOptions: [],
			overview: [],
			formPiano: {
				description: ""
			},
			formStanza: {
				description: "",
				piano_id: ""
			},
			form: {
				description: "",
				pin: "",
				stanza: "",
				type: "attuatore"
			}
		};
	},
	methods: {
		onChangePiano() {
			self = this;
			this.overview.forEach(piano => {
				if (self.form.piano == piano.id) {
					console.log(piano.stanze);
					self.stanzaOptions = piano.stanze.map(element => {
						return {
							text: element["description"],
							value: element["id"]
						};
					});
				}
			});
		},
		addStanza() {
			axiosAuth.post("/add-stanza", this.formStanza).then(response => {
				this.getStatus();
				this.modalstanza = false;
			})
		},
		addPiano() {
			axiosAuth.post("/add-piano", this.formPiano).then(response => {
				this.getStatus();
				this.modalpiano = false;
			})
		},
		onSubmit() {
			console.log("submitted form");
			this.form.pin = parseInt(this.form.pin);
			axiosAuth.post("/add-device", this.form).then(response => {
				this.getStatus();
				this.modal = false;
			});
		},
		toggle(id, status) {
			console.log(id, status);
			// Invert!
			// Send 0 to turn on, 1 to turn off
			if (status) status = 0;
			else status = 1;
			axiosAuth.get("/publish/" + id + "/" + status).then(() => {
				this.getStatus();
			});
		},
		getStatus() {
			console.log(this.$store)
			this.$store.commit('auth/setLoading', 1)
			console.log("status");
			axiosAuth.get("/overview").then(response => {
				// handle success
				this.overview = response.data;
				this.$store.commit('auth/setLoading', 0)
			});
		}
	},
	mounted() {
		console.log("mounted");
		this.getStatus();
	}
};
</script>
