<template>
	<div>
		<center>
			<b-button v-b-modal.modal-1>Aggiungi Dispositivo</b-button>

			<template v-for="piano in overview">
				<h3>{{ piano.description }}</h3>
				
				<template v-for="stanza in piano.stanze">
					<div class="mt-3">
															<b-card
										style="max-width: 80%;"
										border-variant="light"
										bg-variant="light"
										text-variant="black"
										:header="stanza.description "
										class="text-center"
										align="center"
									>
										<b-card-text
											>
												
											
									
						
						<b-card-group deck>
							<center>
								<template v-for="attuatore in stanza.attuatori">
									<b-card
										style="max-width: 15rem;"
										bg-variant="default"
										text-variant="black"
										
										class="text-center"
										align="center"
									>
									<b-card-title>
										{{ attuatore.description }}
									</b-card-title>
										<b-card-text
											>
											<b-button squared class="fsloat-right" :variant='["outline-danger","success"][attuatore.status]' @click="toggle(attuatore.id,attuatore.status)">{{["OFF","ON"][attuatore.status]}}</b-button>
											<br><br>
											<b-badge>{{attuatore.type}}</b-badge>
											
												PIN<code> {{attuatore.pin}}</code>
											</b-card-text
										>
									</b-card>
								</template>
							</center>
						</b-card-group>
					</b-card-text>
						</b-card>
					</div>
				</template>
			</template>
		</center>
		<b-modal id="modal-1" title="Aggiungi Dispositivo">
			<b-form @submit="onSubmit">
				<b-form-group
					id="input-group-1"
					label="Nome:"
					label-for="input-1"
				>
					<b-form-input
						id="input-2"
						v-model="form.namel"
					></b-form-input>
				</b-form-group>
				<b-form-group
					id="input-group-2"
					label="Descrizione:"
					label-for="input-2"
				>
					<b-form-input
						id="input-2"
						v-model="form.descrizione"
					></b-form-input>
				</b-form-group>
			</b-form>
		</b-modal>
	</div>
</template>

<script>
import axiosAuth from "@/api/axios-auth";

export default {
	data() {
		return {
			overview: [],
			form: {
				name: "",
				description: "",
				pin: "",
				type: ""
			}
		};
	},
	methods: {
		onSubmit(){
			console.log(this.form)
		},
		toggle(id,status){
			console.log(id,status)
			// Invert!
			// Send 0 to turn on, 1 to turn off
			if (status)
				status = 0
			else
				status = 1
			axiosAuth.get("/publish/"+id+"/"+status)
			this.getStatus()
		},
		getStatus() {
			console.log("status");
			axiosAuth.get("/overview").then(response => {
				// handle success
				this.overview = response.data;
			});
		}
	},
	mounted() {
		console.log("mounted");
		this.getStatus();
	}
};
</script>
