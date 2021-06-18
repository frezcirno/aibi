<template>
  <div id="movie-querier">
    <div class="rule">
      <h1 style="margin: 55px 30px 20px">组织查询</h1>
      <div class="content">
        <div class="myform">
          <el-form ref="form" :model="Data" label-width="150px">
            <el-form-item label="URI">
              <el-input :value="Data.uri" />
            </el-form-item>
            <el-form-item label="组织名称">
              <el-input :value="Data['organization-name']" />
            </el-form-item>
            <el-form-item label="注册地址">
              <el-input :value="this.esc(Data.RegisteredAddress)" />
            </el-form-item>
            <el-form-item label="成立时间">
              <el-input :value="Data.hasLatestOrganizationFoundedDate" />
            </el-form-item>
            <el-form-item label="IPO时间">
              <el-input :value="Data.hasIPODate" />
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { neo4j_psn } from "@/api";

export default {
  data() {
    return {
      list: null,
      listLoading: false,
      Data: {},
      count: 0,
    };
  },
  computed: {
    hasPermId() {
      console.log(this.$route.params.hasPermId);
      return this.$route.params.hasPermId;
    },
  },
  async created() {
    let res = await neo4j_psn(this.hasPermId).then((res) => res.data);
    this.Data = res.data[0] || {};
  },
  methods: {
    esc(s) {
      return s.replaceAll("\n", " ");
    },
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
