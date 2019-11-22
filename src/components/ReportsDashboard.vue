<template>
  <div id="report-dashboard">
    <div>
      <h1>Reports History</h1>
      <b-table striped hover :items="reports" :fields="fields" @row-clicked="loadReport"></b-table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue);

export default {
  name: "report-dashboard",
  props: ["user", "Report"],
  data: () => ({
    fields: [
      { key: "leavereports_pidm", sortable: true, label: "PIDM" },
      { key: "leavereports_date", sortable: true, label: "Last Modified" },
      { key: "leavereports_report", sortable: false, label: "Name" }
    ],
    reports: []
  }),

  methods: {
    getReports() {
    var tosend = this.user.employee_id;
    fetch("http://localhost:8000/database/getreports/" + tosend + "/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: this.auth
      }
    })
      .then(response => {
        console.log(response);
        response.json().then(data => {
          let len = data.length;
          for (let i = 0; i < len; ++i) {
            this.reports.push(data[i]);
          }
        });
      })
      .catch(function(error) {
        console.log("Request failed", error);
      });
  },
    loadReport(item, index, event) {
      console.log("attempting to load");
      console.log(item.leavereports_report);
      this.report = item.leavereports_report;
      console.log(this.report);
      this.$emit("change-report", item);

    }
  },
  created: function() {
    this.getReports();
  }
};
</script>

<style>
#report-dashboard {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
