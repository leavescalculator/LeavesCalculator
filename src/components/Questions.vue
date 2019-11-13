<template>
  <div id="questions" class="container">
    <div v-if="isAdmin" class="row">
      <div class="input-group mb-3 col-md-3">
        <div class="input-group-prepend">
          <span class="input-group-text">Run as: </span>
        </div>
        <input
          type="text"
          id="usrname"
          placeholder="other username"
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

      <display-question
        :title="Nodes[currentNode].title"
        :options="Nodes[currentNode].options"
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



export default {
  name: "questions",
  props: ["isAdmin", "user", "Nodes"],
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
    DatabaseQuestion
  },
  mounted() {
    console.log(this.Nodes);
  },
  methods: {
    optionSelected(selected) {
      console.log(this.stack);
      //do any relevant stuff here ie addWeeks
      let curr = this.Nodes[this.currentNode].options[selected];

      this.stack.push(this.currentNode);


      this.currentNode = curr.next_node;
    },
    goBack() {
      console.log("in go back");
      let oldNode = this.currentNode;
      this.currentNode = this.stack.pop();
      //logic to find Nodes[currentNod] option leading to oldNode
      // then update weeks if needed
        let option;
        //Find the path from the node we backed up to, to the one we left
        for (let o in this.Nodes[this.currentNode].options) {
            if (o.next_node === oldNode) {
                option = o;
                break;
            }
        }
        //If this edge modifies the number of protected weeks, undo that change because
        //we are backing up
        //if(option.hasOwnProperty('weeks')){
          //  this.$emit('add-weeks', -option.weeks);
        //}
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
