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
            :Nodes="nodes"
          ></router-view>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import Header from "./components/Header";
import $ from 'jquery'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import Questions from './assets/nodes.json';

export default {
  name: 'app',
  data: () => ({
    auth: "",
    username: "",
    isAdmin: false,
      nodes: {},
      user: {
          "employee_id": 800009,
          "odin_username": "HPRYNNE",
          "psu_id": "953125510",
          "first_name": "Hester",
          "last_name": "Prynne",
          "email": [
              "leaves@pdx.edu",
              "hrc-tech-team-group@pdx.edu"
          ],
          "hire_date": "2006-03-20",
          "fte": 1.0,
          "month_lookback_12": "1711.48000000000",
          "month_lookback_6": "833.75",
          "fmla_eligibility": "M",
          "ofla_eligibility": "B",
          "deductions_eligibility": [
              "LST",
              "LTD",
              "PXS"
          ],
          "paid_leave_balances": [
              [
                  "XBRV",
                  0
              ],
              [
                  "ASIC",
                  45.91
              ],
              [
                  "AVAC",
                  116.88
              ],
              [
                  "PERS",
                  15.5
              ],
              [
                  "FLSA",
                  0
              ],
              [
                  "NFLS",
                  0
              ],
              [
                  "XCHG",
                  0
              ],
              [
                  "XOTH",
                  0
              ],
              [
                  "XFUR",
                  0
              ],
              [
                  "XDON",
                  0
              ]
          ],
          "protected_leave_hrs_taken": 0,
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
    },
    mounted() {
      console.log(Questions.Nodes);
      this.nodes = Questions.Nodes;
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
