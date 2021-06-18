<template>
  <div class="movie-querier">
    <div class="rule">
      <h1 class="title">人员查询</h1>
      <div class="content">
        <div class="myform">
          <el-form
            ref="form"
            :model="PersonData.properties"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="PermId">
              <span> {{ PersonData.properties.hasPermId }} </span>
            </el-form-item>
            <el-form-item label="URI">
              <span> {{ PersonData.properties.uri }} </span>
            </el-form-item>
            <el-form-item label="前缀">
              <span> {{ PersonData.properties["honorific-prefix"] }} </span>
            </el-form-item>
            <el-form-item label="姓名">
              <span>
                {{
                  PersonData.properties["family-name"] +
                  ((PersonData.properties["additional-name"] && " ") || "") +
                  (PersonData.properties["additional-name"] || "") +
                  " " +
                  PersonData.properties["given-name"]
                }}
              </span>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div id="result">
      <h1 style="margin: 55px auto 20px" v-if="count >= 0">
        关系组织查询：{{ count }}条结果
      </h1>
      <div style="display: flex; justify-content: center">
        <el-table
          :data="OrganizationDataList"
          height="550"
          stripe
          style="width: 100%"
          v-loading="listLoading"
          element-loading-text="拼命加载中"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)"
        >
          <el-table-column label="ID" width="110">
            <template slot-scope="scope">
              <router-link
                style="color: rgb(0, 0, 238)"
                :to="'/Organization/Detail/' + scope.row.hasPermId"
                >{{ scope.row.hasPermId }}</router-link
              >
            </template>
          </el-table-column>
          <el-table-column prop="uri" label="uri" />
          <el-table-column prop="organization-name" label="就职组织" />
          <el-table-column prop="hasReportedTitle" label="职位" />
          <el-table-column prop="from" label="起始时间" />
          <el-table-column prop="to" label="结束时间" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { neo4j_sql } from "@/api";

export default {
  data() {
    return {
      list: null,
      listLoading: false,
      PersonData: {},
      OrganizationDataList: [],
    };
  },
  computed: {
    count() {
      return this.OrganizationDataList.length;
    },
    hasPermId() {
      console.log(this.$route.params.hasPermId);
      return this.$route.params.hasPermId;
    },
  },
  async created() {
    let res =
      (await neo4j_sql({
        cypher: `MATCH (n:Person) WHERE n.hasPermId="${this.hasPermId}" RETURN n LIMIT 1`,
      }).then((res) => res.data)) || {};
    this.PersonData = res.data[0];
    let res1 =
      (await neo4j_sql({
        cypher: `MATCH path=(p:Person)-[]->(d:Directorship)-[]->(o:Organization) WHERE p.hasPermId="${this.hasPermId}" RETURN path LIMIT 25`,
      }).then((res) => res.data)) || [];
    this.OrganizationDataList = res1.data.map((x) => this.getProperties(x));
  },
  methods: {
    getProperties(path) {
      return { ...path.nodes[1].properties, ...path.end_node.properties };
    },
    esc(s) {
      if (typeof s == "string") {
        return s.replaceAll("\n", " ");
      }
      return s;
    },
  },
};
</script>
