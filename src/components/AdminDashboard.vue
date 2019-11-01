<template>
  <div id="admin-dashboard">
    <tr>
      <td>
        <button type="button" @click="addNode">Add a Node</button>
        <input type="text" id="name" placeholder="name"></input>
        <input type="text" id="parent" placeholder="parent"></input></td>
      <td>|</td>
      <td>
        <button type="button" @click="addData">Add data to node</button>
        <input type="text" id="dataNode" placeholder="node"></input>
        <input type="text" id="key" placeholder="key"></input>
        <input type="text" id="value" placeholder="value"></input>
      </td>
    </tr>
    <button class="btn btn-success" @click="changeView">Change view</button>

    <hr>
    <textarea id="json" cols=50 rows=4></textarea>
    <button type="button" @click="remAllNode">Delete graph</button>
    <button type="button" @click="loadFromJSON">Load JSON</button>

    <hr>
    <div id="cy" @click="showInfo"></div>
    <div id="elementInfo">
      {{ selectedElement }}
      <button type="button" @click="remNode" style="pointer-events: auto;">Remove element</button>
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
            selectedElement: '',
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
                            //'background-color': 'green',
                            'label': 'data(label)',
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'curve-style': 'bezier',
                            'text-rotation': 'autorotate',
                            'target-arrow-shape': 'triangle',
                            'label': 'data(label)',
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

            this.treeLayout();
            this.update_json_display();
        },
        methods: {
            parseJson() {
                for (const node of Object.keys(this.nodes)) {
                    this.cy.add({
                        data: {
                            id: node,
                            input: this.nodes[node].input,
                            label: node.substring(0, 30)
                        }
                    });
                }
                for (const node of Object.keys(this.nodes)) {
                    for (const option of this.nodes[node].options) {
                        try {
                            let node_color = this.cy.nodes('[id="' + option.next_node + '"]').style()['background-color'];
                            let edge = this.cy.add({
                                data: {
                                    label: option.title.substring(0, 30),
                                    title: option.title,
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

                console.log("Adding node `" + name + "`, child of `" + parent + "`");
                if (name !== "") {
                    this.cy.add({
                        data: {id: name}
                    })
                    if (parent != "") {
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
            },
            remNode() {
                this.cy.$(':selected').remove();
                this.update_json_display();
                document.getElementById("elementInfo").style.visibility = 'hidden';
            },
            remAllNode() {
                this.cy.elements().remove();
                this.update_json_display();
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
                treeLayout();
            },
            showInfo() {
                let div = document.getElementById('elementInfo');
                if (this.cy.$(':selected').length > 0) {
                    let element = this.cy.$(':selected')[0];
                    let popper = element.popper({
                        content: () => {
                            if (element.isEdge()) {
                                this.selectedElement = 'Edge: ' + element.data('title')
                                    + '\nSource node: ' + element.data('source')
                                    + '\nTarget node: ' + element.data('target');
                            } else {
                                this.selectedElement = 'Node: ' + element.data('id')
                                    + '\nInput: ' + element.data('input');
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
                        'text-rotation': 'none',
                    })
                } else {
                    this.cy.elements('edge').style({
                        'curve-style': 'bezier',
                        'text-rotation': 'autorotate',
                    })
                }
                this.bezierView = !this.bezierView
            }
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
</style>
