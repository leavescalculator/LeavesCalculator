<template>
  <div id="questions" class="container">
    <div v-if="isAdmin" class="row">
      <div class="input-group mb-3 col-md-3">
        <div class="input-group-prepend">
          <span class="input-group-text">Run as: </span>
        </div>
        <input
          type="text"
          placeholder="other username"
          class="form-control"
          v-model="usrname"
        />
      </div>
      <div class="col-md-2">
        <button class="btn btn-success" @click="changeUser">Change User</button>
      </div>
    </div>
    <btn-question
      :title="currentNode"
      :options="Questions.Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-if="Questions.Nodes[currentNode].input == 'button'"
    ></btn-question>

    <display-question
      :title="currentNode"
      :options="Questions.Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-else-if="Questions.Nodes[currentNode].input == 'display'"
    ></display-question>

    <drop-down-question
      :title="currentNode"
      :options="Questions.Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-else-if="Questions.Nodes[currentNode].input == 'drop down'"
    ></drop-down-question>

    <btn-question
      :title="currentNode"
      :options="Questions.Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-if="Questions.Nodes[currentNode].input == 'database'"
    ></btn-question>

    <!-- <database-question
      :title="currentNode"
      :options="Questions.Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-else-if="Questions.Nodes[currentNode].input == 'database'"
      ></database-question> -->

    <br />
    <button class="btn btn-success" @click="goBack()" v-if="stack[0]">
      Back
    </button>
  </div>
</template>

<script>
import BtnQuestion from './BtnQuestion.vue';
import DisplayQuestion from './DisplayQuestion.vue';
import DropDownQuestion from './DropDownQuestion.vue';
import DatabaseQuestion from './DatabaseQuestion.vue';
import Questions from '../assets/nodes.json';

export default {
  name: "questions",
  props: ["isAdmin", "user"],
  data: () => ({
    currentNode: "Do you have a work related injury?", // initialized to first node of JSON graph structure
    hours: 0, // accumulated leave hours
    stack: [], // structure containing nodes visited
    Questions,
  }),
  computed: {},
  components: {
    BtnQuestion,
    DisplayQuestion,
    DropDownQuestion,
    DatabaseQuestion
  },
  methods: {
    optionSelected(selected) {
      console.log(selected);
      //do any relevant stuff here ie addWeeks
      let curr = this.Questions.Nodes[this.currentNode].options[selected];
      if (curr.weeks !== 0) {
        this.$emit("add-weeks", curr.weeks);
      }

      this.stack.push(this.currentNode);
      this.currentNode = curr.next_node;
    },
    goBack() {
      console.log("in go back");
      let oldNode = this.currentNode;
      this.currentNode = this.stack.pop();
      //logic to finde Nodes[currentNod] option leading to oldNode
      // then update weeks if needed
        var option;
        for (var o in this.Nodes[this.currentNode].options) {
            if (o.next_node === oldNode) {
                option = o;
                break;
            }
        }
        if(option.hasOwnProperty('weeks')){
            this.$emit('add-weeks', -option.weeks);
        }
    },
    changeUser() {
      console.log(this.usrname);
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
