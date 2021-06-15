<template>
  <div class="time" style="width: 100%">
    <el-progress
      class="progress"
      :stroke-width="20"
      :percentage="mysql"
      :format="format('MySQL')"
    />
    <el-progress
      class="progress"
      :stroke-width="20"
      :percentage="neo4j"
      color="rgba(142, 113, 199, 0.7)"
      :format="format('Neo4J')"
    />
    <el-progress
      class="progress"
      :stroke-width="20"
      :percentage="hive"
      :format="format('Hive')"
    />
  </div>
</template>

<script>
export default {
  props: ["usedtime"],
  data() {
    return {
      mysql: 0,
      hive: 0,
      neo4j: 0,
    };
  },
  watch: {
    usedtime: {
      immediate: true,
      handler(val) {
        console.log(val);
        this.usedtime = val;
        this.getPercentage();
        console.log(this.percentage);
      },
    },
  },
  methods: {
    getPercentage() {
      const { mysql, neo4j, hive } = this.usedtime;
      let maxTime = Math.max(Number(mysql), Number(neo4j), Number(hive)) / 100;
      this.mysql = Number(mysql) / maxTime;
      this.neo4j = Number(neo4j) / maxTime;
      this.hive = Number(hive) / maxTime;
      console.log(this.percentage);
    },
    format(db) {
      return () => db + " " + this.usedtime[db.toLowerCase()] + "ms";
    },
  },
};
</script>

<style>
.time > * {
  margin: 20px 0;
}
.el-progress-bar {
  width: 85%;
}
</style>

