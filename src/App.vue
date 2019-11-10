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
        <div>
          <router-view
            @token-acquired="authSuccess"
            :auth="auth"
            :username="username"
            @logout="logOut"
            :user="user"
            @add-weeks="addWeeks"
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
export default {
  name: 'app',
  data: () => ({
    auth: "",
    username: "",
    isAdmin: false,
      user: {
    "employee_id": 800001,
    "odin_username": "DBROOKS",
    "psu_id": "900717619",
    "first_name": "Dorothea",
    "last_name": "Brooks",
    "email": [
        "hrc-tech-team-group@pdx.edu",
        "leaves@pdx.edu"
    ],
    "hire_date": "2010-10-04",
    "fte": 1.0,
    "employee_classification": "",
    "month_lookback_12": "1356.38000000000",
    "month_lookback_6": "524.900000000000",
    "fmla_eligibility": "T",
    "ofla_eligibility": "B",
    "deductions_eligibility": [
        "AAUP",
        "LST",
        "LTD",
        "SEIU",
        "PXS"
    ],
    "paid_leave_balances": [
        {
            "leave_code": "ASIC",
            "balance": 68
        },
        {
            "leave_code": "AVAC",
            "balance": 26.11
        },
        {
            "leave_code": "FLSA",
            "balance": 0
        },
        {
            "leave_code": "XOTH",
            "balance": 0
        },
        {
            "leave_code": "PRES",
            "balance": 0
        }
    ],
    "protected_leave_hrs_taken": 578,
    "max_protected_leave_hrs": null
},
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
        //get user/graph
    },
    logOut() {
      this.auth = '';
      this.username = '';
      this.isAdmin = false;
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
