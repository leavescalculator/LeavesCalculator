<template>
  <div id="graph-dashboard">
    <div>
      <h1>Graph History</h1>
      <b-table striped hover :items="graphs" :fields="fields"></b-table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue);

export default {
  name: "graph-dashboard",
  props: ["auth"],
  data: () => ({
    fields: [
      { key: "id", sortable: true, label: "#" },
      { key: "graph_date", sortable: true, label: "Last Modified" },
      { key: "graph_name", sortable: false, label: "Name" },
      { key: "graph_status", sortable: true, label: "Status" }
    ],
    graphs: []
  }),

  methods: {
    getGraphs() {
      fetch("http://localhost:8000/database/getgraphs/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: this.auth
        }
      })
        .then(response => {
          console.log("request good");
          response.json().then(data => {
            let len = data.length;
            for (let i = 0; i < len; ++i) {
              this.graphs.push(data[i]);
            }
          });
        })
        .catch(function(error) {
          console.log("Request failed", error);
        });
    }
  },
  created: function() {
    this.getGraphs();
  }
};
</script>

<style>
#graph-dashboard {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
