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
        :Cords="cords"
        @change-user="changeEmployee"
        @change-graph="changeGraph"
        :graph-id="graphId"
        :graph-status="graphStatus"
        @change-report="changeReport"
        :Report="report"
        @update-employee="updateEmployee"
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
            :addWeeks="addWeeks"
            @getEmployee="getEmployee"
            :Nodes="nodes"
            :Cords="cords"
            @change-report="changeReport"
            :Report="report"
            @update-employee="updateEmployee"
            @stack="storeStack"
          ></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "./components/Header";

export default {
  name: "app",
  data: () => ({
    auth: "",
    username: "",
    isAdmin: false,
    infoError: "",
    user: {},
    nodes: {},
    cords: "",
    graphStatus: "",
    graphId: "",
    report: "",
    reportId: ""
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
    updateEmployee() {
      console.log(this.user.username);
      this.getEmployee(this.user.odin_username);
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
    addWeeks(n, type) {
      //change weeks here
      console.log("ADDING WEEKS: " + type + ": " + n);
      if (this.user.hasOwnProperty("paid_leave_balances")) {
        if (this.user.paid_leave_balances.hasOwnProperty(type)) {
          this.user.paid_leave_balances[type] += n;
        } else {
          this.user.paid_leave_balances[type] = n;
        }
      }
    },
    storeStack(s) {
      this.user.stack = s;
    },
    getActiveGraph() {
      //This function will retrieve the active graph from the database for deployment
      //It is the default graph to display in the admin dashboard
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
            this.graphStatus = data.graph_status;
            this.graphId = data.id;
            this.cords = data.cords;
          });
        })
        .catch(function(error) {
          console.log("Request failed", error);
        });
    },
    changeGraph(event) {
      //This function will allow the admin to choose a graph to load into
      //the admin dashboard. It listens for the event for this case, and
      //calls another function to set the graph.
      if (this.isAdmin) {
        this.loadGraph(event);
        console.log(
          "Now using graph: #" +
            this.graphId +
            " with status: " +
            this.graphStatus
        );
        //Redirect to admin page
        this.$router.push({
          path: "/admin-dashboard"
        });
      } else {
        console.log("Graph did not get changed");
      }
    },
    loadGraph(graph) {
      //This function will set the graph display to the one passed in
      this.nodes = JSON.parse(graph.graph_data);
      this.graphStatus = graph.graph_status;
      this.graphId = graph.id;
      this.cords = graph.cords;
    },
    changeReport(event) {
      //This function will allow user/admin to choose a report to load into
      //the report vue. It listens for the event for this case, and
      //calls another function to set the report.
      console.log("in app.vue change report");
      this.loadReport(event);
      console.log("Now using report: #" + this.reportId);
      //Redirect to report page
      this.$router.push({ path: "/report" });
    },
    loadReport(report) {
      //This function will set the report display to the one passed in
      console.log("here");

      this.report = report.leavereports_report;
      this.reportId = report.id;
    }
  },
  computed: {},
  mounted() {
    this.getActiveGraph();
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
