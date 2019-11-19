<template>
  <div id="graph-dashboard">
    <div>
      <h1>Graph History</h1>
      <b-table striped hover :items="graphs" :fields="fields"></b-table>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue);

export default {
  data() {
    return {
      name: "graph-dashboard",
      props: ["auth"],
      fields: [
        { key: "id", sortable: true, label: "#" },
        { key: "graph_date", sortable: true, label: "Last Modified" },
        { key: "graph_name", sortable: false, label: "Name" },
        { key: "graph_status", sortable: true, label: "Status" }
      ],
      graphs: []
    };
  },

  method: {
    getGraphs: function() {
      fetch("http://localhost:8000/database/getgraphs/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: this.auth
        }
      })
        .then(json)
        .then(function(data) {
          console.log("request good");
          for (d in data) {
            this.graphs.push(d);
          }
        })
        .catch(function(error) {
          console.log("Request failed", error);
        });
    }
  },
  mounted: function() {
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
