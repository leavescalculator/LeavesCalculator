<template>
  <div id="questions">
    Questions Page!
    <btn-question :title="currentNode" :options="Questions.Nodes[currentNode].options" 
      @option-selected="optionSelected" v-if="Questions.Nodes[currentNode].input == 'button'"></btn-question>

    <display-question :title="currentNode" :options="Questions.Nodes[currentNode].options"
      @option-selected="optionSelected" v-else-if="Questions.Nodes[currentNode].input == 'display'"></display-question>

    <drop-down-question :title="currentNode" :options="Questions.Nodes[currentNode].options"
      @option-selected="optionSelected" v-else-if="Questions.Nodes[currentNode].input == 'drop down'"></drop-down-question>
      
    <btn-question :title="currentNode" :options="Questions.Nodes[currentNode].options" 
      @option-selected="optionSelected" v-if="Questions.Nodes[currentNode].input == 'database'"></btn-question>

   <!-- <database-question :title="currentNode" :options="Nodes[currentNode].options"
      @option-selected="optionSelected" v-else-if="Nodes[currentNode].input == 'database'"></database-question> -->
    <br>
    <button class="btn btn-success" @click="goBack()" v-if="stack[0]">Back</button>
  </div>
</template>

<script>
import BtnQuestion from './BtnQuestion.vue';
import DisplayQuestion from './DisplayQuestion.vue';
import DropDownQuestion from './DropDownQuestion.vue';
import DatabaseQuestion from './DatabaseQuestion.vue';
import Questions from '../assets/questions.json';

export default {
  name: 'questions',
  data: () => ({
    currentNode: "Do you have a work related injury?",
    hours: 0,
    stack: [],
    Questions,
    //Nodes: { }

  }),
  computed: {
    
  },
  components: {
    BtnQuestion, DisplayQuestion, DropDownQuestion, DatabaseQuestion,
  },
  methods: {
    optionSelected(selected) {
      console.log(selected)
      //do any relevant stuff here
      this.stack.push(this.currentNode);
      this.currentNode = this.Questions.Nodes[this.currentNode].options[selected].next_node;
    },
    goBack() {
      console.log("in go back")
      this.currentNode = this.stack.pop();
    }
  }
}



</script>
<!-- styling for the component -->
<style>
#questions {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>