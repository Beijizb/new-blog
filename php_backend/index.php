<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>Vue PHP Blog</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/mashirozx/Sakura@3.x/style.css">
</head>
<body>
  <div id="app" class="layout">
    <h1>{{ message }}</h1>
    <ul>
      <li v-for="post in posts" :key="post.id">
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
      </li>
    </ul>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/vue@2.7.16/dist/vue.js"></script>
  <script src="../frontend/app.js"></script>
</body>
</html>
