<template>
  <div style="width: 100%; height: 100%">
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
      neo4jd3: {},
      neo4jData: {},
      cypher: `MATCH p=(n:Person)-[*4]-(m:Person) RETURN p LIMIT 25`,
    };
  },
  async created() {
    await this.getData(this.cypher);
  },
  methods: {
    async getData(cypher) {
      let res = await neo4j_sql({ cypher }).then((res) => res.data);
      this.neo4jData = this.preprocess(res.data);
      this.neo4jd3 = new Neo4JD3("#graph", {
        highlight: [
          {
            class: "Person",
            property: "name",
            value: "neo4jd3",
          },
          {
            class: "Organization",
            property: "userId",
            value: "eisman",
          },
        ],
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
        neo4jData: this.neo4jData,
        nodeRadius: 25,
        // zoomFit: true,
      });
    },
    async search() {
      await this.getData(this.cypher);
    },
    preprocess(paths) {
      let nodesDict = new Map();
      let relationships = [];
      for (const path of paths) {
        for (const node of path.nodes) {
          if (!nodesDict.has(node.id)) {
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
          relationships.push(relationship);
        }
      }

      let nodes = Array.from(nodesDict.values());
      let graph = { nodes, relationships };
      let data = [{ graph }];
      let columns = [];
      let results = [{ columns, data }];
      let res = { results, errors: [] };
      return res;
    },
  },
};
</script>
