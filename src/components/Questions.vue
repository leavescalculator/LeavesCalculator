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
          placeholder="other username"
          class="form-control"
          v-model="usrname"
          @keydown.enter="changeUser"
        />
      </div>
      <div class="col-md-2">
        <button class="btn btn-success" @click="changeUser">Change User</button>
        <br>
        <p>running as: {{ usrname }}</p>
      </div>
    </div>
    <div v-if="user.employee_id != null">
      <component :is="selectedComponent"
                 :title="Nodes[currentNode].title"
                 :options="Nodes[currentNode].options"
                 @option-selected="optionSelected"
                 :user="user"
                 :description="Nodes[currentNode].description"
      ></component>
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
        computed: {
            selectedComponent() {
                let input = this.Nodes[this.currentNode].input;
                switch (input) {
                    case "button":
                        return "btn-question";
                    case "button-descriptive":
                        return "btn-descriptive-question";
                    case "display":
                        return "display-question";
                    case "drop down":
                        return "drop-down-question";
                    case "database":
                        return "database-question";
                    default:
                        return "";
                }
            }
        },
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
                if (this.currentNode === "report"){
                    this.$emit("stack", this.stack);
                    this.$router.push("/report");
                }
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
