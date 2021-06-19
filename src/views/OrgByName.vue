<template>
  <div class="movie-querier">
    <div class="rule">
      <h1 class="title">组织模糊查询</h1>
      <div class="content">
        <div class="myform">
          <el-form
            ref="form"
            :model="form"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="组织名称">
              <el-input v-model="form.name" placeholder="组织名称" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submit" :loading="listLoading">
                Search
              </el-button>
              <el-button type="info" @click="reset">Reset</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div id="result">
      <h1 class="title" v-if="count >= 0">共查询到{{ count }}条结果</h1>
      <div class="table">
        <el-table :data="TableData" stripe style="width: 100%">
          <el-table-column label="PermId">
            <template slot-scope="scope">
              <router-link
                style="color: rgb(0, 0, 238)"
                :to="'/Organization/Detail/' + scope.row.properties.hasPermId"
                >{{ scope.row.properties.hasPermId }}</router-link
              >
            </template>
          </el-table-column>
          <el-table-column prop="properties.uri" label="uri" />
          <el-table-column
            prop="properties.organization-name"
            label="组织名称"
          />
          <el-table-column prop="properties.hasIPODate" label="上市时间" />
          <el-table-column
            prop="properties.RegisteredAddress"
            label="注册地址"
          />
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
      form: {
        name: "",
        title: "",
        date: "",
        director: "",
        actor: "",
        genre: "",
        y: "",
        m: "",
        d: "",
        weekday: "",
        support_actor: "",
      },
      TableData: [],
      count: 0,
      dbtime: {
        neo4j: 100,
      },
    };
  },
  computed: {
    name() {
      return this.$route.params.name;
    },
  },
  async created() {
    if (!this.name) {
      return;
    }
    this.form.name = this.name;
    await this.fetchData(this.name);
  },
  methods: {
    reset() {
      this.listLoading = false;
    },
    submit() {
      this.$router.push({
        name: this.$route.name,
        params: { name: this.form.name },
      });
    },
    async fetchData(name) {
      this.listLoading = true;
      let res = await neo4j_sql({
        cypher: `MATCH (n:Organization) WHERE ANY (name IN n.\`organization-name\` WHERE name CONTAINS "${name}") RETURN n LIMIT 250`,
      }).then((res) => res.data);
      this.count = res.count;
      this.TableData = res.data;
      this.dbtime = {
        neo4j: res.neo4j,
      };
      this.listLoading = false;
    },
  },
};
</script>
