<template>
  <!-- Firefox bug: height:100% in min-height not inheriting height
  https://stackoverflow.com/questions/8468066/child-inside-parent-with-min-height-100-not-inheriting-height -->
  <div style="position: absolute; width: 100%; height: 100%">
    <div style="position: absolute; bottom: 5px; left: 5px; right: 5px">
      <el-input v-model="cypher">
        <el-button slot="append" @click.prevent="search">提交</el-button>
      </el-input>
    </div>
    <div id="graph" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
window.d3 = d3;
import "neo4jd3/dist/css/neo4jd3.min.css";
import Neo4JD3 from "neo4jd3";
import { neo4j_sql } from "@/api";

export default {
  name: "Graph",
  data() {
    return {
      cypher: `MATCH p=(n:Person)-[*4]-(m:Person) RETURN p LIMIT 25`,
      neo4jd3: {},
      neo4jData: {},
    };
  },
  async created() {
    this.neo4jData = await this.getData(this.cypher);
    this.initTree(this.neo4jData);
  },
  methods: {
    initTree(neo4jData) {
      let that = this;
      this.neo4jd3 = new Neo4JD3("#graph", {
        // highlight: [
        //   {
        //     class: "Person",
        //     property: "name",
        //     value: "neo4jd3",
        //   },
        //   {
        //     class: "Organization",
        //     property: "userId",
        //     value: "eisman",
        //   },
        // ],
        /// Inner Image
        icons: {
          Person: "user",
          Organization: "building",
        },
        /// Bottom Right Corner Image
        // images: {
        //   Person: "img/twemoji/1f3e0.svg",
        //   Organization: "img/twemoji/1f382.svg",
        //   Password: "img/twemoji/1f511.svg",
        //   Project: "img/twemoji/2198.svg",
        //   "Project|name|neo4jd3": "img/twemoji/2196.svg",
        //   User: "img/twemoji/1f600.svg",
        // },
        infoPanel: true,
        minCollision: 60, // Minimum distance between nodes. Default: 2 * nodeRadius.
        neo4jData,
        nodeRadius: 25,
        // zoomFit: true,
        /// 单击时进入更多节点
        // onNodeClick: function (node) {
        //   if (node.labels.includes("Person")) {
        //     console.log(node);
        //     that.$router.push({
        //       name: "PersonDetail",
        //       params: { hasPermId: node.properties.hasPermId },
        //     });
        //   } else if (node.labels.includes("Organization")) {
        //     console.log(node);
        //     that.$router.push({
        //       name: "OrganizationDetail",
        //       params: { hasPermId: node.properties.hasPermId },
        //     });
        //   } else {
        //     window.open(node.properties.uri, "_blank");
        //   }
        // },
        /// 双击时展开更多节点
        onNodeDoubleClick: function (node) {
          let id = node.id;
          let cypher = `match p=(n)-[]-() WHERE id(n)=${id} RETURN p LIMIT 25`;
          that.getData(cypher).then((data) => {
            that.neo4jData = that.merge(neo4jData, data);
            that.initTree(that.neo4jData);
          });
        },
      });
    },
    async getData(cypher) {
      let res = await neo4j_sql({ cypher }).then((res) => res.data);
      return this.preprocess(res.data);
    },
    async search() {
      this.neo4jData = await this.getData(this.cypher);
      this.initTree(this.neo4jData);
    },
    preprocess(paths) {
      let nodesDict = new Map();
      let relationships = [];
      for (const path of paths) {
        for (const node of path.nodes) {
          if (!nodesDict.has(node.id)) {
            if (node.labels.length == 0) {
              node.labels.push("Resource");
            }
            nodesDict.set(node.id, node);
          }
        }
        for (const relationship of path.relationships) {
          relationship.startNode = relationship.start_node.id;
          delete relationship.start_node;
          relationship.endNode = relationship.end_node.id;
          delete relationship.end_node;
          delete relationship.nodes;
          relationship.properties = {};
          if (relationships.every((rel) => rel.id != relationship.id)) {
            relationships.push(relationship);
          }
        }
      }

      let singleRelationships = [];
      for (const relationship of relationships) {
        let ok = true;
        for (const relationship1 of relationships) {
          if (
            (relationship.startNode == relationship1.endNode &&
              relationship.endNode == relationship1.startNode) ||
            (relationship.startNode == relationship1.startNode &&
              relationship.endNode == relationship1.endNode)
          ) {
            if (relationship.id > relationship1.id) {
              ok = false;
              break;
            }
          }
        }
        if (ok) {
          singleRelationships.push(relationship);
        }
      }

      let nodes = Array.from(nodesDict.values());
      let graph = { nodes, relationships: singleRelationships };
      let data = [{ graph }];
      let columns = [];
      let results = [{ columns, data }];
      let res = { results, errors: [] };
      return res;
    },
    merge(data1, data2) {
      let nodesDict = new Map();
      let relationshipsDict = new Map();
      for (const node of data1.results[0].data[0].graph.nodes) {
        if (!nodesDict.has(node.id)) {
          nodesDict.set(node.id, node);
        }
      }
      for (const node of data2.results[0].data[0].graph.nodes) {
        if (!nodesDict.has(node.id)) {
          nodesDict.set(node.id, node);
        }
      }
      for (const node of data1.results[0].data[0].graph.relationships) {
        if (!relationshipsDict.has(node.id)) {
          relationshipsDict.set(node.id, node);
        }
      }
      for (const node of data2.results[0].data[0].graph.relationships) {
        if (!relationshipsDict.has(node.id)) {
          relationshipsDict.set(node.id, node);
        }
      }
      let nodes = Array.from(nodesDict.values());
      let relationships = Array.from(relationshipsDict.values());
      let graph = { nodes, relationships };
      let data = [{ graph }];
      let columns = [];
      let results = [{ columns, data }];
      let res = { results, errors: [] };
      console.log(data1.results[0].data[0].graph.nodes.length, nodes.length);
      console.log(
        data1.results[0].data[0].graph.relationships.length,
        relationships.length
      );
      return res;
    },
  },
};
</script>
