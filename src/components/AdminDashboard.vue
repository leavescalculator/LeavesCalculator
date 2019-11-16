<template>
  <div id="admin-dashboard">
    <div class="header row">
      <div class="col-auto">
        <textarea
          id="jsonOrPositions"
          class="form-control"
          cols=50 rows=3
        ></textarea>
        <br />
        <div class="btn-group" role="group">
        <button class="btn btn-info" @click="outputJson">
          Output JSON
        </button>
        <button class="btn btn-info" @click="loadJson">
          Load JSON
        </button>
        <button class="btn btn-info" @click="outputPositions">
          Output Positions
        </button>
        <button class="btn btn-info" @click="loadPositions">
          Load Positions
        </button>
        <button class="btn btn-info" @click="Save">
          Save Graph
        </button>
        </div>
      </div>

      <div class="col-auto">
        <div class="row input-group">
          <div class="col input-group-prepend">
            <label for="newNodeId" class="input-group-text">ID:</label>
          </div>
          <input
            type="text"
            id="newNodeId"
            placeholder="example id"
            class="col form-control"
          />
        </div>
        <div class="row input-group">
          <div class="col input-group-prepend">
            <label for="newNodeInput" class="input-group-text">Input:</label>
          </div>
          <select class="form-control" id="newNodeInput">
              <option selected hidden disabled>Select one</option>
              <option v-for="inputType in inputTypes" :key="inputType">
                {{ inputType }}
              </option>
          </select>
        </div>
        <button class="btn btn-success" @click="addNode">Add a Node</button>
      </div>

      <div class="col-auto">
        <button @click="() => this.ur.undo()" class="btn btn-warning">
          Undo Element Removal
        </button>
      </div>
    </div>

    <div id="graph"></div>

    <!-- The popper element for changing element properties -->
    <div id="elementInfo">
      <div class="row input-group">
        <div class="col input-group-prepend">
          <label class="input-group-text" for="elementTitle">Title:</label>
        </div>
        <textarea
          v-if="selectedElement"
          id="elementTitle"
          class="col form-control"
          v-model="selectedElement.title"
        ></textarea>
      </div>

      <!-- Edge -->
      <template v-if="selectedElement && selectedElement.isEdge">
        <div class="row input-group">
          <div class="col input-group-prepend">
            <label class="input-group-text" for="edgeHours">
              Added hours:
            </label>
          </div>
          <input
            type="number"
            id="edgeHours"
            v-model="selectedElement.add_time.hours"
            class="col form-control"
          />
        </div>
        <div class="row input-group">
          <div class="col input-group-prepend">
            <label class="input-group-text" for="edgeWeeks">
              Added weeks:
            </label>
          </div>
          <input
            type="number"
            id="edgeWeeks"
            v-model="selectedElement.add_time.weeks"
            class="col form-control"
          />
        </div>

        <div class="row input-group">
          <div class="col input-group-prepend">
            <label class="input-group-text" for="edgeLeaveType">
              Leave type:
            </label>
          </div>
          <select
            v-model="selectedElement.add_time.type"
            id="edgeLeaveType"
            class="col form-control"
          >
            <option
              v-for="addedTimeType in leaveTypes"
              :value="addedTimeType.value"
              :key="addedTimeType.value"
              :selected="addedTimeType.value == selectedElement.add_time.type"
            >{{ addedTimeType.type }}</option>
          </select>
        </div>

        <div class="row input-group">
          <div class="col input-group-prepend">
            <label class="input-group-text" for="edgeSource">
              Source node:
            </label>
          </div>
          <button
            @click="selectNode(selectedElement.source)"
            id="edgeSource"
            class="col form-control btn btn-info"
          >{{ selectedElement.source }}</button>
        </div>

        <div class="row input-group">
          <div class="col input-group-prepend">
            <label class="input-group-text" for="edgeTarget">
              Target node:
            </label>
          </div>
          <button
            @click="selectNode(selectedElement.target)"
            id="edgeTarget"
            class="col form-control btn btn-info"
          >{{ selectedElement.target }}</button>
        </div>
      </template>

      <!-- Node -->
      <template v-else-if="selectedElement">
        <div class="row input-group">
          <div class="col input-group-prepend">
            <span class="input-group-text">Id:</span>
          </div>
          <em class="col form-control">
            {{ selectedElement.id }}
          </em>
        </div>

        <div class="row input-group">
          <div class="col input-group-prepend">
            <label class="input-group-text" for="nodeInput">Input:</label>
          </div>
          <select
            v-model="selectedElement.input"
            id="nodeInput"
            class="col form-control"
          >
            <option
              v-for="inputType in inputTypes"
              :value="inputType"
              :key="inputType"
              :selected="inputType == selectedElement.input"
            >{{ inputType }}</option>
          </select>
        </div>
      </template>

      <div class="row input-group">
        <button
          type="button"
          @click="removeElement"
          class="form-control btn btn-danger"
        >Remove element</button>
      </div>
    </div>
  </div>
</template>
<script>
  import cytoscape from 'cytoscape'
  import edgehandles from 'cytoscape-edgehandles'
  import undoRedo from 'cytoscape-undo-redo'
  import popper from 'cytoscape-popper'
  import graph_style from '../assets/graph-style.json'
  import json from '../assets/nodes.json'

  cytoscape.use(edgehandles)
  cytoscape.use(undoRedo)
  cytoscape.use(popper)

  export default {
      name: 'admin-dashboard',
      data: () => ({
          graph_style: graph_style.style,
          // The nodes objects from `src/assets/nodes.json`
          nodes: json.Nodes,
          // Will become an object with setters and getters for fields of the selected element on selection
          selectedElement: null,
          // The available input fields for a node
          inputTypes: [ 'button', 'drop down', 'display', 'database' ],
          // The types of leave and their corresponding acronyms
          leaveTypes: [
            { type: 'Not Applicable', value: 'n/a' },
            { type: 'Sick',           value: 'LTS' },
            { type: 'Vacation',       value: 'LTV' },
            { type: 'AAUP/SEIU',      value: 'LW1' },
            { type: 'STD',            value: 'STD' },
            { type: 'Unpaid Leave',   value: 'LW3' },
            { type: 'FLSA/NLFA',      value: 'LSA' },
            { type: 'Personal Day',   value: 'Per' },
          ],
      }),
      mounted: function () {
        this.cy = cytoscape({
          container: document.getElementById('graph'),
          style: this.graph_style,
          selectionType: 'single',
        })
        this.cy.edgehandles({
            snap: true,
            complete: (sourceNode, targetNode, addedEles) => {
              addedEles.data('title', '')
              addedEles.data('label', '')
              addedEles.data('add_time', { hours: 0, type: 'n/a' })
              addedEles.addClass('graph-edge')
              addedEles.on('select', this.showInfo)
              addedEles.on('unselect', this.hideInfo)
            }
        });
        this.ur = this.cy.undoRedo({
            undoableDrag: false
        })

        this.parseJson(this.nodes);
        this.cy.layout({
          name: 'breadthfirst'
        }).run()
      },
      methods: {
          parseJson(nodes) {
            for (const node of Object.keys(nodes)) {
                let element = this.cy.add({
                    data: {
                        id: node,
                        label: node,
                        title: nodes[node].title,
                        input: nodes[node].input,
                    },
                    classes: 'graph-node',
                });
                element.on('select', this.showInfo)
                element.on('unselect', this.hideInfo)
            }
            for (const node of Object.keys(nodes)) {
                for (const option of nodes[node].options) {
                    try {
                        let edge = this.cy.add({
                            data: {
                                title: option.title,
                                label: option.title.substring(0, 30),
                                add_time: option.add_time,
                                source: node,
                                target: option.next_node,
                            },
                            classes: 'graph-edge',
                        });
                        edge.on('select', this.showInfo)
                        edge.on('unselect', this.hideInfo)
                    } catch (err) {
                        console.log(err);
                    }
                }
            }
          },
          outputJson() {
            let output = {};
            let nodes = this.cy.$('.graph-node')
            for(let node = 0; node < nodes.length; node++) {
              let element = nodes[node]
              let nodeId = element.data('id')
              output[nodeId] = {
                title: element.data('title'),
                input: element.data('input'),
                options: [],
              }
              let edges = this.cy.edges('[source = "' + nodeId + '"]')
              for(let edge = 0; edge < edges.length; edge++) {
                element = edges[edge]
                output[nodeId].options.push({
                  title:     element.data('title'),
                  add_time: element.data('add_time'),
                  next_node: element.data('target'),
                })
              }
            }
            document.getElementById('jsonOrPositions').value = JSON.stringify(output)
          },
          outputPositions() {
            let output = []
            let nodes = this.cy.$('.graph-node')
            for(let node = 0; node < nodes.length; node++) {
              output.push(nodes[node].relativePosition())
            }
            document.getElementById('jsonOrPositions').value = JSON.stringify(output)
          },
          loadPositions() {
              var json = document.getElementById("jsonOrPositions").value;
              let positions = JSON.parse(json);
              for(let node = 0; node < positions.length; node++) {
                this.cy.$('.graph-node')[node].relativePosition(positions[node])
              }
          },
          addNode() {
              var id = document.getElementById("newNodeId").value;
              var input = document.getElementById("newNodeInput").value;

              let node = this.cy.add({
                  data: {
                      id: id,
                      label: id.substring(0, 30),
                      input: input,
                  },
                  classes: 'graph-node'
              });
              node.on('select', this.showInfo)
              node.on('unselect', this.hideInfo)
          },
          removeElement() {
              if(this.cy.$(':selected').length > 0) {
                  this.ur.do("remove", this.cy.$(':selected')[0])
                  document.getElementById("elementInfo").style.visibility = 'hidden';
              }
          },
          loadJson() {
              var json = document.getElementById("jsonOrPositions").value;
              var nodes ={Nodes: JSON.parse(json)}
            console.log()
              this.cy.$('.graph-node').remove()
              this.parseJson(nodes.Nodes);
              this.cy.layout({
                name: 'breadthfirst'
              }).run()
          },
          hideInfo() {
            let div = document.getElementById('elementInfo');
            div.style.visibility = 'hidden'
          },
          Save(){
          var tosend = JSON.stringify({"GRAPH_DATA": "ASDFASD","GRAPH_NAME": "Asd","CORDS": "aDSF"})
          fetch('http://localhost:8000/database/savegraph/',{
            method: 'POST',
            body: tosend,
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.auth
            }
          })

          },
          showInfo() {
              let div = document.getElementById('elementInfo');
              let element = this.cy.$(':selected')[0];
              let popper = element.popper({
                  content: () => {
                      let isEdge = element.isEdge();
                      if(isEdge) {
                        this.selectedElement = {
                            isEdge: true,
                            get title() {
                                return element.data('title')
                            },
                            set title(title) {
                                element.data('title', title)
                                element.data('label', title.substring(0, 30))
                            },
                            get add_time() {
                                return element.data('add_time')
                            },
                            set add_time(add_time) {
                                element.data('add_time', add_time)
                            },
                            source: element.data('source'),
                            target: element.data('target'),
                        };
                      } else {
                        this.selectedElement = {
                            isEdge: false,
                            get id() {
                                return element.data('id')
                            },
                            get title() {
                                return element.data('title')
                            },
                            set title(title) {
                                element.data('title', title)
                            },
                            get input() {
                                return element.data('input')
                            },
                            set input(input) {
                                element.data('input', input)
                            },
                        };
                      }
                      div.style.visibility = 'visible';
                      return div;
                  }
              });
              let update = () => {
                  popper.scheduleUpdate();
              };
              element.on('position', update);
              this.cy.on('pan zoom resize', update);
          },
          selectNode(to_select) {
              this.cy.$(':selected').unselect()
              this.cy.$id(to_select).select()
              this.showInfo()
          }
      }
  }
</script>
<style>
  .header {
    background-color: #fff;
  }

  #graph {
    width: 100%;
    height: 80%;
    position: absolute;
    top: 200px;
    left: 0px;
  }

  #elementInfo {
    visibility: hidden;
    border: 2px solid #ccc;
    background: #fff;
    padding: 10px;
  }

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
