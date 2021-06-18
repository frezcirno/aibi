<template>
  <div id="movie-querier">
    <div class="rule">
      <h1 style="margin: 55px 30px 20px">组织查询</h1>
      <div class="content">
        <div class="myform">
          <el-form ref="form" :model="Data" label-width="150px">
            <el-form-item label="URI">
              <span> {{ Data.uri }} </span>
            </el-form-item>
            <el-form-item label="组织名称">
              <span> {{ Data["organization-name"] }} </span>
            </el-form-item>
            <el-form-item label="注册地址">
              <span> {{ this.esc(Data.RegisteredAddress) }} </span>
            </el-form-item>
            <el-form-item label="成立时间">
              <span> {{ Data.hasLatestOrganizationFoundedDate }} </span>
            </el-form-item>
            <el-form-item label="IPO时间">
              <span> {{ Data.hasIPODate }} </span>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div id="result">
      <h1 style="margin: 55px 30px 20px" v-if="count >= 0">
        共查询到{{ count }}条结果
      </h1>
      <div style="display: flex; justify-content: center; margin: 0 30px">
        <el-table :data="Person" height="550" stripe style="width: 100%">
          <el-table-column label="ID">
            <template slot-scope="scope">
              <router-link
                class="color: rgb(0, 0, 238);"
                :to="'/Person/' + scope.row.hasPermId"
                >{{ scope.row.hasPermId }}</router-link
              >
            </template>
          </el-table-column>
          <el-table-column prop="uri" label="uri" />
          <el-table-column prop="honorific-prefix" label="前缀" />
          <el-table-column prop="family-name" label="姓" />
          <el-table-column prop="given-name" label="名" />
          <el-table-column prop="hasReportedTitle" label="职位" />
          <el-table-column prop="from" label="from" />
          <el-table-column prop="to" label="to" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { neo4j_org, neo4j_sql } from "@/api";

export default {
  data() {
    return {
      list: null,
      listLoading: false,
      Data: {},
      Person: [],
    };
  },
  computed: {
    count() {
      return this.Person.length;
    },
    hasPermId() {
      return this.$route.params.hasPermId;
    },
  },
  async created() {
    let res = (await neo4j_org(this.hasPermId).then((res) => res.data)) || {};
    this.Data = res.data[0];
    res =
      (await neo4j_sql({
        cypher: `MATCH path=(p:Person)-[]->(d:Directorship)-[]->(o:Organization) WHERE o.hasPermId="${this.hasPermId}" RETURN path LIMIT 25`,
      }).then((res) => res.data)) || [];
    this.Person = res.data.map((x) => this.getPersonAndType(x));
  },
  methods: {
    getPersonAndType(path) {
      return { ...path.nodes[1], ...path.nodes[0] };
    },
    esc(s) {
      if (typeof s == "string") {
        return s.replaceAll("\n", " ");
      }
      return s;
    },
    reset() {
      this.listLoading = false;
    },
  },
};
</script>
