<template>
	<div class="row">
		{{ status }}
		<div class="col-md-6 offset-md-3 col-xl-4 offset-xl-4">
			<form>
				<div class="form-group">
					<label>Username</label>
					<input
						v-model="username"
						type="text"
						class="form-control"
						placeholder="Username"
					/>
				</div>
				<div class="form-group">
					<label>Password</label>
					<input
						v-model="password"
						type="password"
						class="form-control"
						placeholder="Password"
					/>
				</div>
				<div v-if="invalidCredentials" class="form-group">
					<b-alert show variant="danger"
						>Autenticazione non riuscita</b-alert
					>
				</div>
				<small
					><a style="color:#007bff" @click="signupModal = true"
						>Registrati</a
					>
					-
					<a style="color:#007bff" @click="forgotPswModal = true"
						>Password dimenticata?</a
					></small
				><br /><br />
				<button
					type="submit"
					@click.prevent="onSubmit"
					class="btn btn-primary"
				>
					Login
				</button>
				
			</form>
		</div>

		<b-modal v-model="signupModal" id="modal-1" title="Registrati">
			<b-form @submit="onSubmit">
				<b-form-group
					id="input-group-2"
					label="Email:"
					label-for="input-2"
				>
					<b-form-input
						id="input-2"
						v-model="signupForm.email"
					></b-form-input>
				</b-form-group>
				<b-form-group
					id="input-group-2"
					label="Cellulare:"
					label-for="input-2"
				>
					<b-form-input
						id="input-2"
						v-model="signupForm.cellulare"
					></b-form-input>
				</b-form-group>
				<b-form-group
					id="input-group-2"
					label="Username:"
					label-for="input-2"
				>
					<b-form-input
						id="input-2"
						v-model="signupForm.username"
					></b-form-input>
				</b-form-group>
			</b-form>
			<div slot="modal-footer" class="w-100">
				<b-button
					style="margin-left:10px"
					variant="primary"
					class="float-right"
					@click="signup"
				>
					Conferma
				</b-button>
				&nbsp;
				<b-button
					style="margin-left:10px"
					variant="outline-primary"
					class="float-right"
					@click="signupModal = false"
				>
					Annulla
				</b-button>
			</div>
		</b-modal>

		<b-modal
			v-model="forgotPswModal"
			id="modal-1"
			title="Recupera credenziali"
		>
			<b-form @submit="onSubmit">
				<b-form-group
					id="input-group-2"
					label="Email o cellulare"
					label-for="input-2"
				>
					<b-form-input
						id="input-2"
						v-model="forgotPswForm.email"
					></b-form-input>
				</b-form-group>
			</b-form>
			<div slot="modal-footer" class="w-100">
				<b-button
					style="margin-left:10px"
					variant="primary"
					class="float-right"
					@click="forgotPsw"
				>
					Conferma
				</b-button>
				&nbsp;
				<b-button
					style="margin-left:10px"
					variant="outline-primary"
					class="float-right"
					@click="forgotPswModal = false"
				>
					Annulla
				</b-button>
			</div>
		</b-modal>
	</div>
</template>

<script>
import axios from "axios";
import sha512 from "js-sha512";
import { mapGetters } from "vuex";

export default {
	computed: {
		...mapGetters("auth", {
			status: "authStatus"
		})
	},
	data() {
		return {
			signupModal: false,
			forgotPswModal: false,
			signupForm: {
				email: ""
			},
			forgotPswForm: {
				email: ""
			},
			username: "",
			password: "",
			invalidCredentials: false
		};
	},
	methods: {
		forgotPsw() {
			console.log("Stubbed method, mailer disabled");
		},
		signup() {
			console.log("Stubbed method, mailer disabled");
		},
		onSubmit() {
			let formData = {
				username: this.username,
				password: sha512(this.password + "1234780asa231")
			};

			this.$store.dispatch("auth/login", formData).then(response => {
				this.$router.push("/dashboard");
				this.invalidCredentials = localStorage.getItem("token") == "error";
			});
		}
	}
};
</script>
