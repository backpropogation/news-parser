<template>
  <div class="container">
    <b-table striped hover :items="news"></b-table>
  </div>
</template>

<script>
    import axios from 'axios';
    export default {
      name: 'News',
      data() {
        return {

          news: '',
        };
      },
      methods: {
        getMessage() {
          const path = 'http://0.0.0.0:8000/api/news/';
          axios.get(path)
            .then((res) => {
              this.news = res.data;
            })
            .catch((error) => {
              console.error(error);
            });
        },
      },
      created() {
        this.getMessage();
      },
    };
</script>
