<template>
  <div id="app">
  <!-- the router outlet, where all matched components would ber viewed -->
  <router-link v-bind:to="'/'">Login</router-link>
  <router-link v-bind:to="'/questions'">Questions</router-link>
  <router-link v-bind:to="'/report'">Report</router-link>
  <router-view :user="user"></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
  data: () => ({
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
      "fmla_eligibility": "T",
      "ofla_eligibility": "T",
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
  })
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
