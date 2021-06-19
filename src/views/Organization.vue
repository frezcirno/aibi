<template>
  <div class="movie-querier">
    <div class="rule">
      <h1 class="title">组织查询</h1>
      <div class="content">
        <div class="myform">
          <el-form
            ref="form"
            :model="FormData"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="PermId">
              <span> {{ FormData.hasPermId }} </span>
            </el-form-item>
            <el-form-item label="URI">
              <span> {{ FormData.uri }} </span>
            </el-form-item>
            <el-form-item label="组织名称">
              <span> {{ FormData["organization-name"] }} </span>
            </el-form-item>
            <el-form-item label="注册地址">
              <span>
                {{ this.esc(FormData.RegisteredAddress) }}
              </span>
            </el-form-item>
            <el-form-item label="成立时间">
              <span>
                {{ FormData.hasLatestOrganizationFoundedDate }}
              </span>
            </el-form-item>
            <el-form-item label="IPO时间">
              <span> {{ FormData.hasIPODate }} </span>
            </el-form-item>
            <el-form-item label="综合评分">
              <span> {{ score + " / 10.0" }} </span>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div id="PrimaryInstuments">
      <h1 class="title">主要设备</h1>
      <div class="content">
        <div class="myform">
          <el-form
            ref="form"
            :model="InstruData"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="名称">
              <span> {{ InstruData.hasName }} </span>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div id="PrimaryQuote">
      <h1 class="title">主要报价</h1>
      <div class="content">
        <div class="myform">
          <el-form
            ref="form"
            :model="QuoteData"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="股票名称">
              <span> {{ QuoteData.hasName }} </span>
            </el-form-item>
            <el-form-item label="RIC">
              <span> {{ QuoteData.hasRic }} </span>
            </el-form-item>
            <el-form-item label="股票代码">
              <span> {{ QuoteData.hasExchangeTicker }} </span>
            </el-form-item>
            <el-form-item label="交换代码">
              <span> {{ QuoteData.hasExchangeCode }} </span>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div id="result">
      <h1 class="title" v-if="count >= 0">关系人查询：{{ count }}条结果</h1>
      <div class="table">
        <el-table
          :data="PersonDataList"
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
                :to="'/Person/Detail/' + scope.row.hasPermId"
                >{{ scope.row.hasPermId }}</router-link
              >
            </template>
          </el-table-column>
          <el-table-column prop="uri" label="uri" />
          <el-table-column prop="honorific-prefix" label="前缀" width="50" />
          <el-table-column label="姓名">
            <template slot-scope="scope">
              {{
                scope.row["family-name"] +
                ((scope.row["additional-name"] && " ") || "") +
                (scope.row["additional-name"] || "") +
                " " +
                scope.row["given-name"]
              }}
            </template>
          </el-table-column>
          <el-table-column prop="hasReportedTitle" label="职位" />
          <el-table-column prop="from" label="起始时间" />
          <el-table-column prop="to" label="结束时间" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { neo4j_sql, oscore } from "@/api";

export default {
  data() {
    return {
      list: null,
      listLoading: false,
      FormData: {},
      QuoteData: {},
      InstruData: {},
      PersonDataList: [],
      score: 0.0,
    };
  },
  computed: {
    count() {
      return this.PersonDataList.length;
    },
    hasPermId() {
      return this.$route.params.hasPermId;
    },
  },
  async created() {
    if (!this.hasPermId) {
      this.$notify.error({
        title: "参数错误",
        message: "请首先进行模糊查询或手动输入PermId",
      });
      return;
    }
    let res = await neo4j_sql({
      cypher: `MATCH (n:Organization) WHERE n.hasPermId="${this.hasPermId}" RETURN n LIMIT 1`,
    }).then((res) => res.data);
    this.FormData = res.data[0]?.properties || {};
    let res1 =
      (await neo4j_sql({
        cypher: `MATCH path=(p:Person)-[]->(d:Directorship)-[]->(o:Organization) WHERE o.hasPermId="${this.hasPermId}" RETURN path LIMIT 200 UNION MATCH path=(p:Person)-[]->(d:Officership)-[]->(o:Organization) WHERE o.hasPermId="${this.hasPermId}" RETURN path LIMIT 200`,
      }).then((res) => res.data)) || [];
    this.PersonDataList = res1.data.map((x) => this.getProperties(x));
    let res2 = await neo4j_sql({
      cypher: `MATCH (q:Quote)-[]-(o:Organization) WHERE o.hasPermId="${this.hasPermId}" RETURN q LIMIT 1`,
    }).then((res) => res.data);
    this.QuoteData = res2.data[0]?.properties || {};
    this.score = await oscore(this.QuoteData.hasExchangeTicker).then(
      (res) => res.data.score
    );
    let res3 = await neo4j_sql({
      cypher: `MATCH (i:Instrument)-[]-(o:Organization) WHERE o.hasPermId="${this.hasPermId}" RETURN i LIMIT 1`,
    }).then((res) => res.data);
    this.InstruData = res3.data[0]?.properties || {};
  },
  methods: {
    getProperties(path) {
      // middle point comes first
      return { ...path.nodes[1].properties, ...path.start_node.properties };
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
