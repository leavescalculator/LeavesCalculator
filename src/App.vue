<template>
  <div>
    <div v-if="isAdmin">
      <div class="container"><app-header :username="username" :is-admin="isAdmin"></app-header></div>

      <router-view
        @token-acquired="authSuccess"
        :auth="auth"
        :username="username"
        @logout="logOut"
        :user="user"
        :isAdmin="isAdmin"
      ></router-view>
    </div>
    <div id="app" class="container" v-else>
      <!-- the router outlet, where all matched components would ber viewed -->
      <div class="row">
        <div
          class="col-xs-12 col-sm-8 col-sm-offset-2 col-md-6 col-md-offset-3"
        ><app-header :username="username" :is-admin="isAdmin"></app-header></div>
      </div>

      <div class="row">
        <div class="col-xs-12 col-sm-8 col-sm-offset-2 col-md-6 col-md-offset-3">
          <router-view
            @token-acquired="authSuccess"
            :auth="auth"
            :username="username"
            @logout="logOut"
            :user="user"
            @add-weeks="addWeeks"
            @getEmployee="getEmployee"
          ></router-view>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import Header from "./components/Header";
export default {
  name: 'app',
  data: () => ({
    auth: "",
    username: "",
    isAdmin: false,
    infoError: "",
    user: { },
  }),
  components: {
      appHeader: Header,
  },
  methods: {
    authSuccess(event) {
      this.auth = event[0];
      this.username = event[1];
      this.isAdmin = event[2];
      //do fetch stuff
      this.user = this.getEmployee(this.username);
        //get user/graph
    },
    getEmployee(name) {
      var data = JSON.stringify({ name })

      fetch('http://localhost:8000/database/employee/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': this.auth
        },
        body: name,
      }).then(response => {
        if(!response.ok) {
          throw Error("Failed to retrieve employee.")
        }
        console.log(JSON.stringify(response))
        return response.json()
      }).then(data => {
        this.user = data.employee;
      }).catch(error => {
        this.infoError = error
      });

    },
    logOut() {
      this.auth = '';
      this.username = '';
      this.isAdmin = false;
      this.user = { };
    },
    addWeeks(n) {
      //change weeks here
    }
  },
    computed: {
      isAdminBoard() {
          return this.$route.path === "/admin-dashboard/"
      }
    }
};
</script>
<!-- styling for the component -->
<style>
/*
 *** Had to temporarily comment out parent styling so admin-dashboard would look better.
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
 */
</style>
