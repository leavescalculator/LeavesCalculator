<template>
  <div id="questions" class="container">
    <div v-if="isAdmin" class="row">
      <div class="input-group mb-3 col-md-3">
        <div class="input-group-prepend">
          <label for="usrname" class="input-group-text">Run as: </label>
        </div>
        <input
          type="text"
          id="usrname"
          placeholder="other usrname"
          class="form-control"
          v-model="usrname"
          @keydown.enter="changeUser"
        />
      </div>
      <div class="col-md-2">
        <button class="btn btn-success" @click="changeUser">Change User</button>
      </div>
    </div>
    <div v-if="user.employee_id != null">
      <btn-question
        :title="Nodes[currentNode].title"
        :options="Nodes[currentNode].options"
        @option-selected="optionSelected"
        v-if="Nodes[currentNode].input === 'button'"
      ></btn-question>

      <btn-descriptive-question
        :title="Nodes[currentNode].title"
        :options="Nodes[currentNode].options"
        @option-selected="optionSelected"
        v-if="Nodes[currentNode].input === 'button-descriptive'"
      ></btn-descriptive-question>

      <display-question
        :title="Nodes[currentNode].title"
        :options="Nodes[currentNode].options"
        :description="Nodes[currentNode].description"
        @option-selected="optionSelected"
        v-if="Nodes[currentNode].input === 'display'"
      ></display-question>

      <drop-down-question
        :title="Nodes[currentNode].title"
        :options="Nodes[currentNode].options"
        @option-selected="optionSelected"
        v-if="Nodes[currentNode].input === 'drop down'"
      ></drop-down-question>

      <database-question
        :title="Nodes[currentNode].title"
        :options="Nodes[currentNode].options"
        @option-selected="optionSelected"
        v-if="Nodes[currentNode].input === 'database'"
        :user="user"
      ></database-question>

      <br />
      <button class="btn btn-success" @click="goBack()" v-if="stack[0]">
        Back
      </button>
    </div>
    <div v-if="user.employee_id == null && !isAdmin">
      <router-link to="/" class="nav-item nav-link" tag="li" active-class="active"><a>Login</a></router-link>
    </div>
  </div>
</template>

<script>
import BtnQuestion from './BtnQuestion.vue';
import DisplayQuestion from './DisplayQuestion.vue';
import DropDownQuestion from './DropDownQuestion.vue';
import DatabaseQuestion from './DatabaseQuestion.vue';
import BtnDescriptiveQuestion from "./BtnDescriptiveQuestion";



export default {
  name: "questions",
  props: ["isAdmin", "user", "Nodes", "addWeeks"],
  data: () => ({
    currentNode: "work related injury", // initialized to first node of JSON graph structure
    hours: 0, // accumulated leave hours
    stack: [], // structure containing nodes visited
    usrname: "",
  }),
  computed: {},
  components: {
    BtnQuestion,
    DisplayQuestion,
    DropDownQuestion,
    DatabaseQuestion,
    BtnDescriptiveQuestion
  },
  mounted() {
    //console.log(this.Nodes);
  },
  methods: {
    optionSelected(selected) {
      //console.log(this.stack);
      //do any relevant stuff here ie addWeeks
      let curr = this.Nodes[this.currentNode].options[selected];

      if (curr.hasOwnProperty("add_time") && curr.add_time.hasOwnProperty("weeks") && curr.add_time.hasOwnProperty("type"))
      {
          console.log("weeks: " + curr.add_time.weeks);
          if(curr.add_time.type !== "n/a") {
              this.addWeeks(curr.add_time.weeks, curr.add_time.type);
          }
      }

      if(this.Nodes[this.currentNode].input !== 'database') {
        this.stack.push({
            "node": this.currentNode,
            "edge": selected
        });
      }
      this.currentNode = curr.next_node;
    },
    goBack() {
      //console.log("in go back");
      let node = this.stack.pop();
      this.currentNode = node.node;
      //logic to find Nodes[currentNod] option leading to oldNode
      let option = this.Nodes[node.node].options[node.edge];
      if(option.add_time.weeks !== 0) {
          this.addWeeks(-option.add_time.weeks, option.add_time.type)
      }
    },
    changeUser() {
      //add code to replace the user object with a new one based on a provided username
      console.log(this.usrname);
      console.log("Attempting to change to :" + this.usrname);
      this.currentNode = "work related injury",
      this.$emit('change-user', this.usrname);
    }
  }
};
</script>
<!-- styling for the component -->
<style>
#questions {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
