<template>
  <div class="movie-querier">
    <div>
      <h1 class="title">人员模糊查询</h1>
      <div class="content">
        <div class="myform">
          <el-form
            ref="form"
            :model="form"
            label-position="left"
            label-width="100px"
          >
            <el-form-item label="姓 (family-name)">
              <el-input v-model="form['family-name']" placeholder="姓" />
            </el-form-item>
            <el-form-item label="中间名 (middle-name)">
              <el-input
                v-model="form['additional-name']"
                placeholder="中间名"
              />
            </el-form-item>
            <el-form-item label="名 (given-name)">
              <el-input v-model="form['given-name']" placeholder="名" />
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
        <el-table :data="Data" height="550" stripe style="width: 100%">
          <el-table-column label="ID">
            <template slot-scope="scope">
              <router-link
                style="color: rgb(0, 0, 238)"
                :to="'/Person/' + scope.row.hasPermId"
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
        "family-name": "",
        "additional-name": "",
        "given-name": "",
      },
      Data: [],
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
    familyName() {
      return this.$route.params.name.split(",")[0];
    },
    additionalName() {
      return this.$route.params.name.split(",")[1];
    },
    givenName() {
      return this.$route.params.name.split(",")[2];
    },
  },
  async created() {
    if (!this.familyName && !this.additionalName && !this.givenName) {
      return;
    }
    this.form["family-name"] = this.familyName;
    this.form["additional-name"] = this.additionalName;
    this.form["given-name"] = this.givenName;
    await this.fetchData(this.familyName, this.additionalName, this.givenName);
  },
  methods: {
    reset() {
      this.listLoading = false;
    },
    submit() {
      this.$router.push({
        name: this.$route.name,
        params: {
          name:
            this.form["family-name"] +
            "," +
            this.form["additional-name"] +
            "," +
            this.form["given-name"],
        },
      });
    },
    async fetchData(familyName, additionalName, givenName) {
      this.listLoading = true;
      let conditions = [];
      if (familyName.trim()) {
        conditions.push(`n.\`family-name\` = "${familyName}"`);
      }
      if (additionalName.trim()) {
        conditions.push(`n.\`additional-name\` CONTAINS "${additionalName}"`);
      }
      if (givenName.trim()) {
        conditions.push(`n.\`given-name\` CONTAINS "${givenName}"`);
      }
      let res = await neo4j_sql({
        cypher: `MATCH (n:Person) WHERE ${conditions.join(
          " AND "
        )} RETURN n LIMIT 25`,
      }).then((res) => res.data);
      this.count = res.count;
      this.Data = res.data;
      this.dbtime = {
        neo4j: res.neo4j,
      };
      this.listLoading = false;
    },
  },
};
</script>
