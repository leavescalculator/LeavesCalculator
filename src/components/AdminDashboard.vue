<template>
  <div id="admin-dashboard">
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

    <button class="btn btn-success" @click="changeView">Change view</button>
    <hr />

    <textarea id="json" cols=50 rows=4></textarea>
    <button type="button" @click="loadFromJSON">Load JSON</button>
    <hr />

    <div id="cy" @click="showInfo"></div>
    <div id="elementInfo">
        <div v-if="selectedElement && selectedElement.isEdge">
          <b>Edge</b>
          <br />
          <label>Title: </label><textarea v-model="selectedElement.title" class="pointable"></textarea>
          <br />
          <label>Source node: </label>
          <button @click="selectNode(selectedElement.source)" class="pointable">
              {{ selectedElement.source }}
          </button>
          <br />
          <label>Target node: </label>
          <button @click="selectNode(selectedElement.target)" class="pointable">
              {{ selectedElement.target }}
          </button>
        </div>
        <div v-else-if="selectedElement">
          <b>Node</b>
          <br />
          <label>Id: </label><textarea v-model="selectedElement.id" class="pointable"></textarea>
          <br />
          <label>Input: </label><select v-model="selectedElement.input" class="pointable">
              <option v-for="inputType in inputTypes" :value="inputType" :selected="inputType==selectedElement.input">{{ inputType }}</option>
          </select>
        </div>
        <button type="button" @click="removeElement" class="pointable">Remove element</button>
    </div>
  </div>
</template>
<script>
    import cytoscape from 'cytoscape'
    import popper from 'cytoscape-popper'
    import edgehandles from 'cytoscape-edgehandles'
    import json from '../assets/nodes.json'

    cytoscape.use(popper)
    cytoscape.use(edgehandles)

    export default {
        name: 'admin-dashboard',
        data: () => ({
            nodes: json.Nodes,
            bezierView: true,
            selectedElement: null,
            inputTypes: [ 'button', 'drop down', 'display', 'database' ]
        }),
        mounted: function () {
            this.cy = cytoscape({
                container: document.getElementById('cy'),
                layout: {
                    name: 'grid'
                },
                style: [
                    {
                        selector: 'node',
                        style: {
                            'shape': 'hexagon',
                            'label': 'data(label)',
                            'background-color': 'green',
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'curve-style': 'bezier',
                            'label': 'data(label)',
                            'target-arrow-shape': 'triangle',
                            'text-margin-y': -12,
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

            this.parseJson();

            this.cy.layout({
                name: 'breadthfirst'
            }).run();
            this.update_json_display();
        },
        methods: {
            parseJson() {
                for (const node of Object.keys(this.nodes)) {
                    let element = this.cy.add({
                        data: {
                            id: node,
                            label: node.substring(0, 30),
                            input: this.nodes[node].input,
                        }
                    });
                }
                for (const node of Object.keys(this.nodes)) {
                    for (const option of this.nodes[node].options) {
                        try {
                            let node_color = this.cy.$id(option.next_node).style()['background-color'];
                            let edge = this.cy.add({
                                data: {
                                    title: option.title,
                                    label: option.title.substring(0, 30),
                                    add_hours: option.add_hours,
                                    source: node,
                                    target: option.next_node,
                                }
                            });
                            edge.style({
                                //'line-color': node_color,
                                'target-arrow-color': node_color,
                            });
                        } catch (err) {
                            console.log(err);
                        }
                    }
                }
                this.update_json_display();
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
                this.update_json_display();
            },
            removeElement() {
                this.cy.$(':selected').remove();
                this.update_json_display();
                document.getElementById("elementInfo").style.visibility = 'hidden';
            },
            addData() {
                var node = document.getElementById("dataNode").value;
                var key = document.getElementById("key").value;
                var value = document.getElementById("value").value;
                j = this.cy.$('#' + node);
                j.data(key, value);
                update_json_display();
            },
            update_json_display() {
                document.getElementById("json").value = JSON.stringify(this.cy.json());
            },
            loadFromJSON() {
                var j = document.getElementById("json").value;
                this.cy.json(JSON.parse(j));
                this.cy.layout({
                    name: 'breadthfirst'
                }).run();
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
                                  source: element.data('source'),
                                  target: element.data('target'),
                              };
                            } else {
                              this.selectedElement = {
                                  isEdge: false,
                                  get id() {
                                      return element.data('id')
                                  },
                                  set id(id) {
                                      element.data('id', id)
                                      element.data('label', id.substring(0, 30))
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
            changeView() {
                if (this.bezierView) {
                    this.cy.elements('edge').style({
                        'curve-style': 'taxi',
                    })
                } else {
                    this.cy.elements('edge').style({
                        'curve-style': 'bezier',
                    })
                }
                this.bezierView = !this.bezierView
            },
            selectNode(to_select) {
                this.cy.$(':selected').unselect()
                this.cy.$id(to_select).select()
                this.showInfo()
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
    border: 1px solid red;
    background: #fff;
    pointer-events: none;
    width: 500px;
  }

  .pointable {
    pointer-events: auto;
  }
</style>
