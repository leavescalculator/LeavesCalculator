<template>
  <div id="login">
    <div v-if="username">
        <p>Signed in as <b>{{ username }}</b></p>

      <router-link v-if="isAdmin" v-bind:to="'/admin-dashboard'">
        Admin Dashboard
      </router-link>
      <br v-if="isAdmin" />

      <button @click="signOut">Sign out</button>
    </div>
    <form v-if="(auth === '')" onsubmit="return false">
      <div class="input-group">
        <p>Login:</p>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">Username</span>
          </div>
          <input type="text" class="form-control" name="username" id="username" />
        </div>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">Password</span>
          </div>
          <input type="password" class="form-control" name="password" id="password" />
        </div>
      </div>
      <br>
        <button class="btn btn-success" @click.prevent="sendCredentials">Submit</button>
        <p style="color:red;">{{ loginError }}</p>
    </form>

    <div id="includedContent"></div>
</div>
</template>

<script>
export default {
  name: 'login',
  data: () => ({
    loginError: '',
    isAdmin: false
  }),
  props: ['auth', 'username'],
  methods: {
    sendCredentials() {
      var username = document.getElementById('username').value
      var password = document.getElementById('password').value
      var data = JSON.stringify({ username, password })

      fetch('http://localhost:8000/api-token-auth/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: data,
      }).then(response => {
          if(!response.ok) {
              throw Error("Login failed.")
          }
          return response.json()
      }).then(data => {
          console.log(JSON.stringify(data))
          this.isAdmin = data.is_admin;
          this.$emit('token-acquired', ['Token ' + data["token"], username, this.isAdmin]);
      }).catch(error => {
          this.loginError = error
      });
    },
    signOut() {
      this.$emit('logout', 0);
      this.loginError = '';
      this.isAdmin = false;
    }
  }
}
</script>
<!-- styling for the component -->
<style>
#login {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
