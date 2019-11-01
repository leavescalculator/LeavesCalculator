<template>
  <div id="app">
  <!-- the router outlet, where all matched components would ber viewed -->
  <router-link v-bind:to="'/'">Login</router-link>
  <router-link v-bind:to="'/questions'">Questions</router-link>
  <router-link v-bind:to="'/report'">Report</router-link>
  <router-view @token-aquired="authSuccess" 
    :auth='auth' 
    :username='username'
    @logout='logOut'></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
  data: () => ({
      auth: '',
      username: '',
  }),
  methods: {
    authSuccess(event) {
      this.auth = event[0];
      this.username = event[1];
    },
    logOut() {
      this.auth = '';
      this.username = '';
    },
  }
}
</script>
<!-- styling for the component -->
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
