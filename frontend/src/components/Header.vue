<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">Smart Home Automation</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-text>
          <router-link to="/" class="nav-link">Home</router-link>
        </b-nav-text>
        <b-nav-text v-if="!isAuth">
          <router-link to="/login" class="nav-link">Login</router-link>
        </b-nav-text>
        <b-nav-text v-if="isAuth">
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
        </b-nav-text>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">


        <b-nav-item-dropdown right v-if="isAuth">
          <!-- Using 'button-content' slot -->
          <template slot="button-content"><em>User</em></template>
          <!--<b-dropdown-item href="#">Profile</b-dropdown-item>-->
          <b-dropdown-item href="#" @click="onLogout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>


</div>
</template>

<script>
  import { mapGetters } from 'vuex'
  
  export default {
    computed: {
      ...mapGetters('auth', {
        isAuth: 'isAuthenticated',
      })
    },
    methods: {
      onLogout() {
        this.$store.dispatch('auth/logout');
      }
    }
  }
</script>
