<template>
  <div id="graph-dashboard">
    <div>
      <h1>Graph History</h1>
      <div>
        <!-- Table rows -->
        <b-table
          striped
          hover
          :items="graphs"
          :fields="fields"
          :tbody-tr-class="highlightActive"
          @row-clicked="loadGraph"
        >
          <!-- Redirect to admin dashboard with this graph if selected -->
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
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue);

export default {
  name: "graph-dashboard",
  props: ["isAdmin"],
  data: () => ({
    //Fields to display in table
    fields: [
      { key: "id", sortable: true, label: "#" },
      { key: "graph_date", sortable: true, label: "Last Modified" },
      { key: "graph_status", sortable: true, label: "Status" }
    ],
    //List of all graph versions
    graphs: []
  }),

  methods: {
    getGraphs() {
      //This function will retrieve all the graphs in the database
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
      //This function will emit a call to change the current graph to display
      //in the admin dashboard. Item is the graph, index is the index in
      //this.graphs[] in which this graph is stored, and event is the event handler
      console.log("Attempting to change to graph #" + item.id);
      this.$emit("change-graph", item);
    },
    highlightActive(item, type) {
      //This function will highlight the current active in the table for
      //easy detection
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
