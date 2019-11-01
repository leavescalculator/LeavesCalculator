<template>
  <div id="app" class="container">
    <!-- the router outlet, where all matched components would ber viewed -->
    <div class="row">
      <div
        class="col-xs-12 col-sm-8 col-sm-offset-2 col-md-6 col-md-offset-3"
      ><app-header :username="username"></app-header></div>
    </div>

    <div class="row">
      <div class="col-xs-12 col-sm-8 col-sm-offset-2 col-md-6 col-md-offset-3">
        <router-view
          @token-acquired="authSuccess"
          :auth="auth"
          :username="username"
          @logout="logOut"
        ></router-view>
      </div>
    </div>

    <button @click="goToHello">Hello</button>
  </div>
</template>

<script>
import Header from "./components/Header";
export default {
  name: "app",
  data: () => ({
    auth: "",
    username: ""
  }),
  components: {
      appHeader: Header,
  },
  methods: {
    authSuccess(event) {
      this.auth = event[0];
      this.username = event[1];
    },
    logOut() {
      this.auth = "";
      this.username = "";
    },
    goToHello() {
      fetch("http://localhost:8000/hello/", {
        method: "GET",
        headers: {
          Authorization: this.auth
        }
      })
        .then(response => {
          if (!response.ok) {
            throw Error("Login failed.");
          }
          return response.json();
        })
        .then(data => {
          console.log(JSON.stringify(data));
        });
    }
  }
};
</script>
<!-- styling for the component -->
<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
