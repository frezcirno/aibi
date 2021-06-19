<template>
  <div class="movie-querier">
    <div class="rule">
      <h1 class="title">人员查询</h1>
      <div class="content">
        <div class="myform">
          <el-form
            ref="form"
            :model="PersonData"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="PermId">
              <span> {{ PersonData.hasPermId }} </span>
            </el-form-item>
            <el-form-item label="URI">
              <span> {{ PersonData.uri }} </span>
            </el-form-item>
            <el-form-item label="前缀">
              <span> {{ PersonData["honorific-prefix"] }} </span>
            </el-form-item>
            <el-form-item label="姓名">
              <span>
                {{
                  PersonData["family-name"] +
                  ((PersonData["additional-name"] && " ") || "") +
                  (PersonData["additional-name"] || "") +
                  " " +
                  PersonData["given-name"]
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
    <div class="rule">
      <h1 style="margin: 55px auto 20px" v-if="count >= 0">
        教育经历查询：{{ eduCount }}条结果
      </h1>
      <div style="display: flex; justify-content: center">
        <el-table
          :data="EduDataList"
          stripe
          style="width: 100%"
          v-loading="listLoading"
          element-loading-text="拼命加载中"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)"
        >
          <el-table-column prop="fromInstitutionName" label="学校" />
          <el-table-column prop="prefLabel" label="学位" />
          <!-- <el-table-column prop="to" label="to" /> -->
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
      EduDataList: [],
      OrganizationDataList: [],
    };
  },
  computed: {
    count() {
      return this.OrganizationDataList.length;
    },
    eduCount() {
      return this.EduDataList.length;
    },
    hasPermId() {
      console.log(this.$route.params.hasPermId);
      return this.$route.params.hasPermId;
    },
  },
  async created() {
    let res = await neo4j_sql({
      cypher: `MATCH (n:Person) WHERE n.hasPermId="${this.hasPermId}" RETURN n LIMIT 1`,
    }).then((res) => res.data);
    this.PersonData = res.data[0]?.properties || {};
    let res1 =
      (await neo4j_sql({
        cypher: `MATCH path=(p:Person)-[]->(d:Directorship)-[]->(o:Organization) WHERE p.hasPermId="${this.hasPermId}" RETURN path LIMIT 25`,
      }).then((res) => res.data)) || [];
    this.OrganizationDataList = res1.data.map((x) => this.getProperties(x));
    let res2 =
      (await neo4j_sql({
        cypher: `MATCH path=(p:Person)-[]-(a:AcademicQualification)-[]-(ad:AcademicDegree) WHERE p.hasPermId="${this.hasPermId}" RETURN path LIMIT 25`,
      }).then((res) => res.data)) || [];
    console.log(res2);
    this.EduDataList = res2.data.map((x) => ({
      ...x.nodes[1].properties,
      ...x.end_node.properties,
    }));
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
