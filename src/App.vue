<template>
  <div>
    <div v-if="isAdmin">
      <div class="container">
        <app-header :username="username" :is-admin="isAdmin"></app-header>
      </div>

      <router-view
        @token-acquired="authSuccess"
        :auth="auth"
        :username="username"
        @logout="logOut"
        :user="user"
        :isAdmin="isAdmin"
        :Nodes="nodes"
        @change-user="changeEmployee"
      ></router-view>
    </div>
    <div id="app" class="container" v-else>
      <!-- the router outlet, where all matched components would ber viewed -->
      <div class="row">
        <div class="col-xs-12 col-sm-8 col-sm-offset-2 col-md-6 col-md-offset-3">
          <app-header :username="username" :is-admin="isAdmin"></app-header>
        </div>
      </div>

      <div class="row">
        <div>
          <router-view
            @token-acquired="authSuccess"
            :auth="auth"
            :username="username"
            @logout="logOut"
            :user="user"
            @add-weeks="addWeeks"
            @getEmployee="getEmployee"
            :Nodes="nodes"
          ></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "./components/Header";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import Questions from "./assets/nodes.json";

export default {
  name: "app",
  data: () => ({
    auth: "",
    username: "",
    isAdmin: false,
    infoError: "",
    user: {},
    nodes: {}
  }),
  components: {
    appHeader: Header
  },
  methods: {
    authSuccess(event) {
      this.auth = event[0];
      this.username = event[1];
      this.isAdmin = event[2];
      //do fetch stuff
      console.log("Getting info...");
      this.getEmployee(this.username);
      //get user/graph
    },
    changeEmployee(event) {
      if (this.isAdmin) {
        if (this.getEmployee(event)) {
          console.log("Now using " + event + "'s information.");
        }
      } else {
        console.log("Nice try bozo.");
      }
    },
    getEmployee(name) {
      var data = JSON.stringify({ name });
      var emp_u = name.toUpperCase();
      console.log(emp_u);
      fetch("http://localhost:8000/database/" + emp_u + "/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: this.auth
        }
      })
        .then(response => {
          if (!response.ok) {
            throw Error("Failed to retrieve employee.");
          }
          return response.json();
        })
        .then(data => {
          console.log(data);
          this.user = data;
        })
        .catch(error => {
          this.infoError = error;
        });
    },
    logOut() {
      this.auth = "";
      this.username = "";
      this.isAdmin = false;
      this.user = {};
    },
    addWeeks(n) {
      //change weeks here
    },
    getActiveGraph() {
      fetch("http://localhost:8000/database/getactivegraph/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: this.auth
        }
      })
        .then(response => {
          console.log("request good");
          response.json().then(data => {
            this.nodes = data.graph_data;
          });
        })
        .catch(function(error) {
          console.log("Request failed", error);
        });
    }
  },
  computed: {},
  mounted() {
    this.getActiveGraph();
    //console.log(Questions.Nodes);
    //this.nodes = Questions.Nodes;
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
