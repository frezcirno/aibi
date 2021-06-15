<template>
  <div id="movie-querier">
    <div class="rule">
      <h1 style="margin: 55px 30px 20px">评论用户查询</h1>
      <div class="content">
        <div class="myform">
          <el-form ref="form" :model="form" label-width="150px">
            <el-form-item label="电影id">
              <el-input v-model="form.asin" placeholder="电影id" />
            </el-form-item>
            <el-form-item label="电影名称">
              <el-input v-model="form.title" placeholder="电影名称" />
            </el-form-item>
            <el-form-item label="电影类别">
              <el-select v-model="form.genre" placeholder="请选择">
                <el-option
                  v-for="item in genre_options"
                  :key="item"
                  :label="item"
                  :value="item"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="导演名字">
              <el-input v-model="form.director" placeholder="导演名字" />
            </el-form-item>
            <el-form-item label="主要演员名字">
              <el-input v-model="form.actor" placeholder="主要演员名字" />
            </el-form-item>
            <el-form-item label="参与演员名字">
              <el-input
                v-model="form.support_actor"
                placeholder="参与演员名字"
              />
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
      <h1 style="margin: 55px 30px 20px" v-if="count >= 0">时间统计</h1>
      <div style="display: flex; justify-content: left; margin: 0 30px">
        <Time :usedtime="dbtime" />
      </div>
    </div>
    <div id="result">
      <h1 style="margin: 55px 30px 20px" v-if="count >= 0">
        共查询到{{ count }}条结果
      </h1>
      <div style="display: flex; justify-content: center; margin: 0 30px">
        <el-table :data="movieData" height="550" stripe style="width: 100%">
          <el-table-column prop="asin" label="商品ID" width="150" />
          <el-table-column prop="movie" label="所属电影ID" width="150" />
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
import { combine_product } from "@/api/movie";
import Time from "@/components/Time.vue";

export default {
  components: { Time },
  data() {
    return {
      list: null,
      listLoading: false,
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
      weekday_options: [1, 2, 3, 4, 5, 6, 7],
      month_options: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      day_options: [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
      ],
      form: {
        asin: "",
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
      movieData: [],
      count: 0,
      dbtime: {
        mysql: 100,
        neo4j: 100,
        hive: 100,
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
      if (this.form.asin) params["asin"] = this.form.asin;
      if (this.form.title) params["title"] = this.form.title;
      if (this.form.director) params["director"] = this.form.director;
      if (this.form.actor) params["actor"] = this.form.actor;
      if (this.form.support_actor)
        params["support_actor"] = this.form.support_actor;
      if (this.form.genre) params["genre"] = this.form.genre;
      if (this.form.title) params["title"] = this.form.title;
      if (this.form.y) params["y"] = this.form.y;
      if (this.form.m) params["m"] = this.form.m;
      if (this.form.d) params["d"] = this.form.d;
      if (this.form.weekday) params["weekday"] = this.form.weekday;
      combine_product(params).then((response) => {
        this.count = response.data.count;
        this.movieData = response.data.data;
        this.dbtime = {
          mysql: response.data.mysql,
          neo4j: response.data.neo4j,
          hive: response.data.hive,
        };
        this.listLoading = false;
      });
    },
  },
};
</script>
