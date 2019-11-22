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
        :Nodes="nodes"
        @change-user="changeEmployee"
        :addWeeks="addWeeks"
        @getEmployee="getEmployee"
        @stack="storeStack"
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
        <div>
          <router-view
            @token-acquired="authSuccess"
            :auth="auth"
            :username="username"
            @logout="logOut"
            :user="user"
            :addWeeks="addWeeks"
            @getEmployee="getEmployee"
            :Nodes="nodes"
            @stack="storeStack"
          ></router-view>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import Header from "./components/Header";
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import Questions from './assets/nodes.json';

export default {
  name: 'app',
  data: () => ({
    auth: "",
    username: "",
    isAdmin: false,
    infoError: "",
    user: { },
    nodes: {},
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
      console.log("Getting info...");
      this.getEmployee(this.username);
        //get user/graph
    },
    changeEmployee(event) {
      if(this.isAdmin) {
        if(this.getEmployee(event)) {
          console.log("Now using " + event + "'s information.");
        }
      }
      else {
        console.log("Nice try bozo.");
      }
    },
    getEmployee(name) {
      let emp_u = name.toUpperCase();
      console.log(emp_u);
      fetch('http://localhost:8000/database/' + emp_u + '/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': this.auth
        }
      }).then(response => {
        if(!response.ok) {
          throw Error("Failed to retrieve employee.")

        }
        return response.json()
      }).then(data => {
        console.log(data);
        this.user = data;
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
    addWeeks(n, type) {
      //change weeks here
      console.log("ADDING WEEKS: " + type + ": " + n);
      if(this.user.hasOwnProperty("paid_leave_balances")) {
          if(this.user.paid_leave_balances.hasOwnProperty(type)){
              this.user.paid_leave_balances[type] += n;
          }
          else {
              this.user.paid_leave_balances[type] = n;
          }
      }

    },
    storeStack(s) {
        this.user.stack = s;
    }
  },
  computed: {
  },
  mounted() {
    console.log(Questions.Nodes);
    this.nodes = Questions.Nodes;
  }
};
</script>
<style>
  .row {
    margin: 2px;
  }

  .input-group-prepend {
    padding: 0;
  }

  .input-group-text {
    width: inherit;
  }

  .form-control {
    height: auto;
    min-width: 200px;
  }
</style>
