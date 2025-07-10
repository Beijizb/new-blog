new Vue({
  el: '#app',
  data: {
    message: 'Sakura Theme Blog',
    posts: []
  },
  created() {
    fetch('../php_backend/api.php')
      .then(response => response.json())
      .then(data => { this.posts = data });
  }
});
