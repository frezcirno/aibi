<template>
  <div id="movie-querier">
    <div class="rule">
      <h1 style="margin: 55px 30px 20px">合作关系查询</h1>
      <div class="content">
        <div class="myform">
          <el-form ref="form" :model="form" label-width="100px">
            <el-form-item label="导演名字">
              <el-input v-model="form.director" placeholder="导演名字" />
            </el-form-item>
            <el-form-item label="主演名字">
              <el-input v-model="form.actor" placeholder="主演名字" />
            </el-form-item>
            <el-form-item label="参演名字">
              <el-input v-model="form.support_actor" placeholder="参演名字" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submit" :loading="searching">
                Search
              </el-button>
              <el-button type="info" @click="reset">Reset</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div id="result">
      <h1 style="margin: 55px 30px 20px" v-if="count">
        共查询到{{ count }}条结果
      </h1>
      <div style="display: flex; justify-content: center; margin: 0 30px">
        <el-table :data="movieData" height="550" stripe style="width: 100%">
          <el-table-column prop="asin" label="电影ID" width="150" />
          <el-table-column prop="title" label="电影名称" width="150" />
          <el-table-column prop="y" label="上映年份" width="150" />
          <el-table-column prop="m" label="上映月份" width="150" />
          <el-table-column prop="d" label="上映日期" width="150" />
          <el-table-column prop="weekday" label="星期" width="150" />
          <el-table-column prop="rating" label="评分" width="150" />
          <el-table-column
            prop="pos_review_count"
            label="好评人数"
            width="150"
          />
          <el-table-column
            prop="neg_review_count"
            label="差评人数"
            width="150"
          />
          <!-- <el-table-column prop="actor" label="演员" width="150" />
        <el-table-column prop="director" label="导演" width="150" />
        <el-table-column prop="genre" label="分类" width="150" /> -->
          <!-- <el-table-column
          prop="review_count"
          sortable
          label="评论数"
          width="150"
        />
        <el-table-column prop="release_time" sortable label="上映时间" /> -->
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { neo4j_relation } from "@/api";

export default {
  data() {
    return {
      list: null,
      listLoading: true,
      searching: false,
      genre_options: [
        "",
        "Action",
        "Adventure",
        "Science Fiction",
        "Suspense",
        "Comedy",
        "Drama",
        "Fantasy",
        "Horror",
        "Arts",
        "Culture",
        "Entertainment",
        "Special Interest",
        "Kids",
        "Sports",
        "Documentary",
        "Romance",
        "Western",
        "Military  War",
        "Music Videos  Concerts",
        "Arthouse",
        "Animation",
        "Historical",
        "Young Adult Audience",
        "LGBTQ",
        "International",
        "Anime",
        "Faith  Spirituality",
        "Unscripted",
        "Fitness",
        "Talk Show  Variety",
        "Erotic",
      ],
      form: {
        director: "",
        actor: "",
        support_actor: "",
      },
      movieData: [],
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
      if (this.form.director) params["director"] = this.form.director;
      if (this.form.actor) params["actor"] = this.form.actor;
      if (this.form.support_actor)
        params["support_actor"] = this.form.support_actor;
      neo4j_relation(params).then((response) => {
        this.movieData = response.data.data;
        this.listLoading = false;
      });
    },
  },
};
</script>
