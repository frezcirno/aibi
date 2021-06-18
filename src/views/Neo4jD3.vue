<template>
  <el-container>
    <div id="graph" style="width: 100%; height: 100%"></div>
  </el-container>
</template>

<style scoped>
</style>

<script>
import Neo4JD3 from "neo4jd3";
var neo4jd3 = new Neo4JD3("#neo4jd3", {
  highlight: [
    {
      class: "Project",
      property: "name",
      value: "neo4jd3",
    },
    {
      class: "User",
      property: "userId",
      value: "eisman",
    },
  ],
  minCollision: 60,
  neo4jDataUrl: "json/neo4jData.json",
  nodeRadius: 25,
  onNodeDoubleClick: function (node) {
    switch (node.id) {
      case "25":
        // Google
        window.open(node.properties.url, "_blank");
        break;
      default:
        var maxNodes = 5,
          data = neo4jd3.randomD3Data(node, maxNodes);
        neo4jd3.updateWithD3Data(data);
        break;
    }
  },
  zoomFit: true,
});
export default {
  name: "neo4j",
};
</script>
