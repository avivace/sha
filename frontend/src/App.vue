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