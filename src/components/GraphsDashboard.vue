<template>
  <div id="graph-dashboard">
    <div>
      <h1>Graph History</h1>
      <div>
        <b-table
          striped
          hover
          :items="graphs"
          :fields="fields"
          :tbody-tr-class="highlightActive"
          @row-clicked="loadGraph"
        >
          <!--<template v-slot:cell(id)="data">
          <router-link
            to="/graph-dashboard"
            class="nav-item nav-link"
            tag="li"
            active-class="active"
            v-if="isAdmin"
          >
            <a>{{data.value}}</a>
          </router-link>
          </template>-->
        </b-table>
      </div>
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
  props: ["isAdmin"],
  data: () => ({
    fields: [
      { key: "id", sortable: true, label: "#" },
      { key: "graph_date", sortable: true, label: "Last Modified" },
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
    },
    loadGraph(item, index, event) {
      console.log("Attempting to change to graph #" + item.id);
      this.$emit("change-graph", item);
    },
    highlightActive(item, type) {
      if (item.graph_status == "A") return "table-success";
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
