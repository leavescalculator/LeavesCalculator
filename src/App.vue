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
  {{ auth }}

  <button @click="goToHello">Hello</button>
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
    goToHello() {
      let token = 'Token ' + this.auth["token"];
      console.log(this.auth["token"]);
      fetch('http://localhost:8000/hello/', {
          method: 'GET',
          headers: {
              'Authorization': token
          },
      }).then(response => {
          if(!response.ok) {
              throw Error("Login failed.")
          }
          return response.json()
      }).then(data => {
          console.log(JSON.stringify(data))
          this.$emit('token-aquired', [JSON.stringify(data), username])
      }).catch(error => {
          this.loginError = error
      });
    }
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