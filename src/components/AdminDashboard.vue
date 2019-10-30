<template>
  <div id="admin-dashboard">
    <button id="circle" type="button" @click="circleLayout">Circle</button>
    <button id="tree" type="button" @click="treeLayout">Tree</button>
    <button id="random" type="button" @click="randLayout">Random</button>
    <hr>
    <tr>
      <td><button type="button" @click="addNode">Add a Node</button>
        <input type="text" id="name" placeholder="name"></input>
        <input type="text" id="parent" placeholder="parent"></input></td>
        <td>|</td>
        <td><button type="button" @click="addEdge">Add an edge</button>
          <input type="text" id="source" placeholder="source"></input>
          <input type="text" id="dest" placeholder="destination"></input></td>
        <td>|</td>
        <td><button type="button" @click="addData">Add data to node</button>
          <input type="text" id="dataNode" placeholder="node"></input>
          <input type="text" id="key" placeholder="key"></input>
          <input type="text" id="value" placeholder="value"></input>
        </td>
    </tr>
    
    <hr>
    <button type="button" @click="remNode()">Delete selected element</button>
    <button type="button" @click="remAllNode()">Delete graph</button>
    <button type="button" @click="loadFromJSON()">Load JSON</button>

    <hr>
    <div><div id="cy"></div></div>
    <textarea id="json" cols=50 rows=4></textarea>
  </div>
</template>
<script>
  import cytoscape from '../assets/js/cytoscape.umd.js'
  import json from '../assets/questions.json'
  
  export default {
    name: 'admin-dashboard',
    data: () => ({
        questions: json.Nodes,
    }),
    mounted: function() {
      this.cy = cytoscape({
        container: document.getElementById('cy'),
        layout: {
          name: 'grid'
        },
        style: [
          {
           selector: 'node',
           style: {
             shape: 'hexagon',
             'background-color': 'green',
             label: 'data(id)',
           }
          },
          {
            selector: 'edge',
            style: {
              'curve-style': 'bezier',
              'target-arrow-shape': 'triangle'
            }
          }
        ]
      })

      this.parseJson();

      this.treeLayout();
      this.update_json_display();

      console.log(this.cy.json());
  },
  methods: {
    parseJson() {
      for(const question of Object.keys(this.questions)) {
        this.cy.add({
          data: { id: question }
        });
      }
      for(const question of Object.keys(this.questions)) {
        for(const option of this.questions[question].options) {
            try{
              this.cy.add({
                data: {
                  id: "`" + option.title + "` for:\n\n" + question,
                  source: question,
                  target: option.next_node,
                }
              });
            }
            catch(err){
              console.log(err);
            }
        }
      }
      console.log(this.cy);
    },
    treeLayout() {
      this.cy.layout({
        name: 'breadthfirst'
      }).run();
    },
    circleLayout() {
      this.cy.layout({
        name: 'circle'
      }).run();
    },
    randLayout() {
      this.cy.layout({
        name: 'random'
      }).run();
    },
    addNode() {
      var name = document.getElementById("name").value;
      var parent = document.getElementById("parent").value;

      console.log("Adding " + name + " child of " + parent);
      if(name !== ""){
        this.cy.add({
          data: { id: name }
        })
        if(parent != "") {
          this.cy.add({
            data: {
              id: parent + name,
              source: parent,
              target: name,
            }
          })
        }
      }
      update_json_display();
      console.log(this.cy.json());
    },
    addEdge() {
      var source = document.getElementById("source").value;
      var dest = document.getElementById("dest").value;

      console.log("Adding " + source + " to " + dest);
      if(source !== "" && dest !== ""){
          this.cy.add({
            data: {
              id: source + '-' + dest,
              source: source,
              target: dest,
              arrow: 'triangle'
            }
          })
        }
        update_json_display();
      console.log(this.cy.json());
    },
    remNode() {  
      this.cy.$(':selected').remove();
      console.log(this.cy.json());
      update_json_display();
    },
    remAllNode() {
      this.cy.elements().remove();
      update_json_display();
    },
    addData() {
      var node = document.getElementById("dataNode").value;
      var key = document.getElementById("key").value;
      var value = document.getElementById("value").value;
      j = this.cy.$('#' + node);
      j.data(key, value);
      console.log(this.cy.json());
      update_json_display();
    },
    update_json_display() {
      document.getElementById("json").value = JSON.stringify(this.cy.json());
    },
    loadFromJSON() {
      var j = document.getElementById("json").value;
      this.cy.json(JSON.parse(j));
      treeLayout();
    }
  },
}
</script>
<!-- styling for the component -->
<style>
  #cy {
    width: 100%;
    height: 80%;
    position: absolute;
    top: 200px;
    left: 0px;
  }
</style>
