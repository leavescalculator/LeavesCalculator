<!--
  Component for making changes to a visual directed graph that is the
  representation for the various questions and outcomes that may be presented
  to a user if they choose to run a new report.
-->
<template>
  <div id="admin-dashboard" v-if="isAdmin">
    <div class="header row">
      <!--
        TODO: This textbox and associated buttons will be replaced with the
        ability to save and load graphs from the database.
      -->
      <div class="col-6">
        <div
          id="jsonOrPositions"
          class="form-control"
          contenteditable="true"
        >{{ jsonOrPositions }}</div>
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
        </div>
      </div>

      <!-- This input group is used for created new nodes -->
      <div class="col-3">
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

      <!-- This button allows for element removal to be undone -->
      <div class="col-3">
        <button @click="() => this.ur.undo()" class="btn btn-warning">
          Undo Element Removal
        </button>
      </div>
    </div>

    <div id="graph"></div>

    <!-- The popper element for displaying and changing element properties -->
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

      <!-- If the selected element is an edge -->
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

      <!-- If the selected element is a node -->
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
  // For representing, viewing, and changing the graph
  import cytoscape from 'cytoscape'
  // For creating new edges by dragging the mouse between nodes
  import edgehandles from 'cytoscape-edgehandles'
  cytoscape.use(edgehandles)
  // For undoing element removal
  import undoRedo from 'cytoscape-undo-redo'
  cytoscape.use(undoRedo)
  // For displaying information about a selected element
  import popper from 'cytoscape-popper'
  cytoscape.use(popper)
  // The styling for the Cytoscape.js graph
  import graph_style from '../assets/graph-style.json'
  // The default graph representation
  // TODO: This file will be deleted and the graph will be stored on the DB
  import json from '../assets/nodes.json'

  export default {
    name: 'admin-dashboard',
    props: ['isAdmin'],
    data: () => ({
      // The data stored in the large textbox within the header
      // TODO: this field can be removed when we are saving and loading
      // from the DB
      jsonOrPositions: '',
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
      // Initializing the graph visualization
      this.cy = cytoscape({
        container: document.getElementById('graph'),
        style: graph_style.style,
      })

      // Specifying the properties of creating a new edge
      this.cy.edgehandles({
        snap: true,
        handleNodes: '.graph-node',
        complete: (sourceNode, targetNode, edge) => {
          edge.data('title', '')
          edge.data('label', '')
          edge.data('add_time', { hours: 0, type: 'n/a' })
          edge.addClass('graph-edge')
          edge.style('target-arrow-color', targetNode.style('background-color'))
          edge.on('select', this.showInfo)
          edge.on('unselect', this.hideInfo)
        }
      })

      // Not considering the moving of nodes an undoable action
      this.ur = this.cy.undoRedo({
          undoableDrag: false
      })

      // Create legend
      for(var inputType in this.inputTypes) {
        let legendNode = this.cy.add({
          data: {
            id: this.inputTypes[inputType],
            inputType: inputType
          },
          classes: [
            'legend-node',
            this.legendClass(this.inputTypes[inputType])
          ],
          selectable: false,
          pannable: true,
        })
        this.setLegendNodePosition(legendNode)
        this.cy.on('pan', () =>
          this.setLegendNodePosition(legendNode)
        )
        this.cy.on('zoom', () =>
          this.setLegendNodePosition(legendNode)
        )
      }

      // Parsing the JSON graph
      this.parseJson(json.Nodes)

      // Displaying the graph as a tree
      this.cy.$('.graph-node, .graph-edge').layout({
        name: 'breadthfirst'
      }).run()
    },
    methods: {
      // Parses the provided map of node id's -> node objects into
      // Cytoscape.js nodes and edges.
      parseJson(nodes) {
        // First, creating the nodes
        for (const node of Object.keys(nodes)) {
          let element = this.cy.add({
            data: {
              id: node,
              label: node,
              title: nodes[node].title,
              input: nodes[node].input,
            },
            classes: [ 'graph-node', this.legendClass(nodes[node].input) ],
          })
          element.on('select', this.showInfo)
          element.on('unselect', this.hideInfo)
        }

        // Then creating the edges
        for (const node of Object.keys(nodes)) {
          for (const option of nodes[node].options) {
            // TODO: Remove this try-catch when condifident that the graph's
            // JSON structure has no invalid `next_node` id's
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
              })
              edge.style('target-arrow-color', this.cy.$id(option.next_node).style('background-color'))
              edge.on('select', this.showInfo)
              edge.on('unselect', this.hideInfo)
            } catch (err) {
              console.log(nodes[node].title)
              console.log(err)
            }
          }
        }
      },
      // Creates the JSON structure to represent the graph based on the
      // current state of the Cytoscape.js graph
      outputJson() {
        let output = {}
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
        this.jsonOrPositions = JSON.stringify(output)
      },
      // Gets the positions of every graph node
      outputPositions() {
        let output = []
        let nodes = this.cy.$('.graph-node')
        for(let node = 0; node < nodes.length; node++) {
          output.push(nodes[node].relativePosition())
        }
        this.jsonOrPositions = JSON.stringify(output)
      },
      // Sets the positions for every graph node
      loadPositions() {
        let positions = JSON.parse(this.jsonOrPositions)
        for(let node = 0; node < positions.length; node++) {
          this.cy.$('.graph-node')[node].relativePosition(positions[node])
        }
      },
      // Creates a new node
      addNode() {
        var id = document.getElementById("newNodeId").value
        var input = document.getElementById("newNodeInput").value

        let node = this.cy.add({
          data: {
            id: id,
            label: id.substring(0, 30),
            input: input,
          },
          classes: 'graph-node'
        })
        node.on('select', this.showInfo)
        node.on('unselect', this.hideInfo)
      },
      // Removes one element, regardless if it's a node or edge
      removeElement() {
        if(this.cy.$(':selected').length > 0) {
          this.ur.do("remove", this.cy.$(':selected')[0])
          document.getElementById("elementInfo").style.visibility = 'hidden'
        }
      },
      // Parses the JSON in the header's textbox and updates the graph's state
      loadJson() {
        let nodes = JSON.parse(this.jsonOrPositions)
        this.cy.$('.graph-node').remove()
        this.parseJson(nodes)
        this.cy.$('.graph-node, .graph-edge').layout({
          name: 'breadthfirst'
        }).run()
      },
      // Hides the popper element
      hideInfo() {
        let div = document.getElementById('elementInfo')
        div.style.visibility = 'hidden'
      },
      // Shows the popper element, which displays and allows the changing
      // of specific graph elements.
      showInfo() {
        let div = document.getElementById('elementInfo')
        let element = this.cy.$(':selected')[0]
        let popper = element.popper({
          content: () => {
            let isEdge = element.isEdge()
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
              }
            } else { // Node
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
              }
            }
            div.style.visibility = 'visible'
            return div
          }
        })
        let update = () => {
            popper.scheduleUpdate()
        }
        element.on('position', update)
        this.cy.on('pan zoom resize', update)
      },
      // Selects the specified node
      selectNode(toSelect) {
        this.cy.$(':selected').unselect()
        this.cy.$id(toSelect).select()
        this.showInfo()
      },
      // Sets the rendered position of the legend nodes based on the current
      // zoom value
      setLegendNodePosition(legendNode) {
        legendNode.renderedPosition({
          x: 50 * this.cy.zoom(),
          y: (60 * legendNode.data('inputType') + 50) * this.cy.zoom(),
        })
      },
      // Returns the associated class that is represented in the legend for
      // the given input type
      legendClass(inputType) {
        if(inputType === 'drop down') {
          return 'drop-down'
        } else {
          return inputType
        }
      }
    }
  }
</script>
<style scoped>
  /* The banner on the top of the screen, below the nav bar */
  .header {
    margin: 0;
    background-color: #fff;
    border-bottom: 2px solid #999;
    width: 100%;
    height: calc(200px - 42px);
    padding-top: 8px;
    z-index: 2;
    position: fixed;
    overflow-y: hidden;
  }

  /* The Cytoscape.js canvas */
  #graph {
    width: 100%;
    height: 80%;
    position: absolute;
    top: 200px;
    left: 0px;
  }

  /* The popper element */
  #elementInfo {
    visibility: hidden;
    border: 2px solid #ccc;
    background: #fff;
    padding: 10px;
    z-index: 1;
  }

  /* For the large textbox in the header
   * TODO: Remove this when removing the textbox
   */
  #jsonOrPositions {
    height: 85px;
    width: 490px;
    overflow-y: auto;
  }
</style>
