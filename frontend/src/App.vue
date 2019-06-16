<template>
  <div id="app">
    <app-header/>
    <router-view/>
  </div>
</template>

<script>
  import Header from '@/components/Header.vue'

  export default {
    created() {
      this.$store.dispatch('auth/autoLogin');
    },
    components: {
      AppHeader: Header,
    },
    
  }
</script>

<style>
body {
  font-family: 'Rubik';
  font-weight: 400
}
.h1 .h2 .h3 h1 h2 h3{
  font-weight: 400
}
</style>}
