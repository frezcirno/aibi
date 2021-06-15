<template>
  <div id="movie-querier">
    <div class="rule">
      <h1 style="margin: 55px 30px 20px">组织查询</h1>
      <div class="content">
        <div class="myform">
          <el-form ref="form" :model="form" label-width="150px">
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
      <h1 style="margin: 55px 30px 20px" v-if="count >= 0">
        共查询到{{ count }}条结果
      </h1>
      <div style="display: flex; justify-content: center; margin: 0 30px">
        <el-table :data="Data" height="550" stripe style="width: 100%">
          <el-table-column prop="hasPermId" label="ID" />
          <el-table-column prop="organization-name" label="组织名称" />
          <el-table-column prop="hasIPODate" label="上市时间" />
          <el-table-column prop="RegisteredAddress" label="注册地址" />
          <!-- <el-table-column prop="actor" label="演员" />
          <el-table-column prop="director" label="导演" />
          <el-table-column prop="genre" label="分类" /> -->
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { find_organization } from "@/api/movie";
import Time from "@/components/Time.vue";

export default {
  components: { Time },
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
      Data: [],
      count: 0,
      dbtime: {
        neo4j: 100,
      },
    };
  },
  methods: {
    reset() {
      this.listLoading = false;
    },
    submit() {
      this.fetchData();
    },
    fetchData() {
      this.listLoading = true;
      let params = {};
      if (this.form.name) params["name"] = this.form.name;
      console.log(params);
      find_organization(params).then((response) => {
        this.count = response.data.count;
        this.Data = response.data.data;
        this.dbtime = {
          neo4j: response.data.neo4j,
        };
        this.listLoading = false;
      });
    },
  },
};
</script>
