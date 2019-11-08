<template>
  <div id="admin-dashboard">
    <textarea id="jsonOrPositions" cols=50 rows=4></textarea>
    <br />
    <button type="button" @click="outputJson">Output JSON</button>
    <button type="button" @click="loadJson">Load JSON</button>
    <button type="button" @click="outputPositions">Output Positions</button>
    <button type="button" @click="loadPositions">Load Positions</button>
    <hr />

    <label for="newNodeId">ID: </label>
    <input type="text" id="newNodeId" name="newNodeId" placeholder="example id" />
    <br />
    <label for="newNodeInput">Input: </label>
    <select id="newNodeInput" name="newNodeInput">
        <option selected hidden disabled>Select one</option>
        <option v-for="inputType in inputTypes">{{ inputType }}</option>
    </select>
    <br />
    <button type="button" @click="addNode">Add a Node</button>
    <hr />

    <button @click="() => this.ur.undo()">Undo Element Removal</button>
    <hr />

    <div id="cy" @click="showInfo"></div>
    <div id="elementInfo">
        <label for="edgeTitle">Title: </label>
        <div v-if="selectedElement" @input="updateTitle" name="edgeTitle" id="elementTitle" contentEditable="true">
          {{ selectedElement.title }}
        </div>

        <div v-if="selectedElement && selectedElement.isEdge">
          <label for="edgeHours">Added hours: </label>
          <input type="number" name="edgeHours" v-model="selectedElement.add_time.hours" />
          <label for="edgeWeeks">Added weeks: </label>
          <input type="number" name="edgeWeeks" v-model="selectedElement.add_time.weeks" />
          <br />

          <label for="edgeHoursType">Added hours type: </label>
          <select v-model="selectedElement.add_time.type" name="edgeHoursType">
              <option v-for="addedTimeType in addedTimeTypes" :value="addedTimeType.value" :selected="addedTimeType.value==selectedElement.add_time.type">
                  {{ addedTimeType.type }}
              </option>
          </select>
          <br />

          <label for="edgeSource">Source node: </label>
          <button @click="selectNode(selectedElement.source)" name="edgeSource" class="nodeButton">
              {{ selectedElement.source }}
          </button>
          <br />

          <label for="edgeTarget">Target node: </label>
          <button @click="selectNode(selectedElement.target)" name="edgeTarget" class="nodeButton">
              {{ selectedElement.target }}
          </button>
        </div>
        <div v-else-if="selectedElement">
          <label for="nodeId">Id: </label><em name="nodeId">{{ selectedElement.id }}</em>
          <br />

          <label for="nodeInput">Input: </label>
          <select v-model="selectedElement.input" name="nodeInput">
              <option v-for="inputType in inputTypes" :value="inputType" :selected="inputType==selectedElement.input">{{ inputType }}</option>
          </select>
        </div>

        <button type="button" @click="removeElement">
            Remove element
        </button>
    </div>
  </div>
</template>
<script>
  import cytoscape from 'cytoscape'
  import popper from 'cytoscape-popper'
  import edgehandles from 'cytoscape-edgehandles'
  import undoRedo from 'cytoscape-undo-redo'
  import json from '../assets/nodes.json'

  cytoscape.use(popper)
  cytoscape.use(edgehandles)
  cytoscape.use(undoRedo)


  export default {
      name: 'admin-dashboard',
      data: () => ({
          // The nodes objects from `src/assets/nodes.json`
          nodes: json.Nodes,
          selectedElement: null,
          inputTypes: [ 'button', 'drop down', 'display', 'database' ],
          addedTimeTypes: [
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
      props: ['isAdmin'],
      mounted: function () {
        this.cy = cytoscape({
          container: document.getElementById('cy'),
            style: [
                {
                    selector: 'node',
                    style: {
                        'shape': 'hexagon',
                        'label': 'data(label)',
                        'color': '#000',
                        'text-background-color': '#ccc',
                        'text-background-opacity': 0.8,
                        'text-background-padding': 5,
                        'text-background-shape': 'roundrectangle',
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'curve-style': 'bezier',
                        'control-point-step-size': 50,
                        'label': 'data(label)',
                        'target-arrow-shape': 'triangle',
                        'target-arrow-color': 'green',
                        'color': '#fff',
                        'text-background-color': '#333',
                        'text-background-opacity': 0.8,
                        'text-background-padding': 5,
                        'text-background-shape': 'roundrectangle',
                        'text-rotation': 'autorotate',
                    }
                },
                {
                    selector: '.eh-handle',
                    style: {
                        'background-color': 'red',
                        'width': 12,
                        'height': 12,
                        'shape': 'ellipse',
                        'overlay-opacity': 0,
                        'border-width': 12,
                        'border-opacity': 0
                    }
                },
                {
                    selector: '.eh-hover',
                    style: {
                        'background-color': 'red'
                    }
                },
                {
                    selector: '.eh-source',
                    style: {
                        'border-width': 2,
                        'border-color': 'red'
                    }
                },
                {
                    selector: '.eh-target',
                    style: {
                        'border-width': 2,
                        'border-color': 'red'
                    }
                },
                {
                    selector: '.eh-preview, .eh-ghost-edge',
                    style: {
                        'background-color': 'red',
                        'line-color': 'red',
                        'target-arrow-color': 'red',
                        'source-arrow-color': 'red'
                    }
                },
                {
                    selector: '.eh-ghost-edge.eh-preview-active',
                    style: {
                        'opacity': 0
                    }
                }
            ],
            selectionType: 'single',
        })
        this.cy.edgehandles({
            snap: true
        });
        this.ur = this.cy.undoRedo({
            undoableDrag: false
        })

        this.cy.on('ehcomplete', (event, sourceNode, targetNode, addedEles) => {
            addedEles.data('title', '')
            addedEles.data('label', '')
            addedEles.data('add_time', { hours: 0, type: 'n/a' })
        });

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
                    }
                });
            }
            for (const node of Object.keys(nodes)) {
                for (const option of nodes[node].options) {
                    try {
                        let node_color = this.cy.$id(option.next_node).style()['background-color'];
                        let edge = this.cy.add({
                            data: {
                                title: option.title,
                                label: option.title.substring(0, 30),
                                add_time: option.add_time,
                                source: node,
                                target: option.next_node,
                            }
                        });
                    } catch (err) {
                        console.log(err);
                    }
                }
            }
          },
          outputJson() {
            let output = {};
            let nodes = this.cy.nodes()
            for(let node = 0; node < nodes.length; node++) {
              let element = this.cy.nodes()[node]
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
            let nodes = this.cy.nodes()
            for(let node = 0; node < nodes.length; node++) {
              output.push(nodes[node].relativePosition())
            }
            document.getElementById('jsonOrPositions').value = JSON.stringify(output)
          },
          loadPositions() {
              var json = document.getElementById("jsonOrPositions").value;
              let positions = JSON.parse(json);
              for(let node = 0; node < positions.length; node++) {
                this.cy.nodes()[node].relativePosition(positions[node])
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
                  }
              });
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
              this.cy.nodes().remove()
              this.parseJson(nodes.Nodes);
              this.cy.layout({
                name: 'breadthfirst'
              }).run()
          },
          showInfo() {
              let div = document.getElementById('elementInfo');
              if (this.cy.$(':selected').length > 0) {
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
              } else {
                  div.style.visibility = 'hidden';
              }
          },
          selectNode(to_select) {
              this.cy.$(':selected').unselect()
              this.cy.$id(to_select).select()
              this.showInfo()
          },
          updateTitle(event) {
              this.selectedElement.title = event.target.innerText
          },
      }
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

  #elementInfo {
    visibility: hidden;
    border: 2px solid #ccc;
    background: #fff;
    padding: 10px;
  }

  #elementTitle {
      display: inline-block;
      border: 1px solid #ccc;
      min-height: 10px;
      max-height: 100px;
      width: 250px;
      padding: 2px;
      overflow-y: auto;
  }

  label {
      display: inline-block;
      width: 120px;
      text-align: right;
  }

  #elementInfo input {
      display: inline-block;
      text-align: center;
      width: 100px;
      margin-left: auto;
      margin-right: auto;
      align: center;
  }

  .nodeButton {
    width: 250px;
  }
</style>
