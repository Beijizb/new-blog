# Flask Markdown 博客

这是一个使用 Flask 构建的简易博客系统，支持 Markdown 撰写文章，并提供明亮/暗色主题切换。系统包含基本的文章管理、分类和标签功能，同时提供简单的后台登录。

## 功能

- 创建、编辑和查看文章
- Markdown 实时预览，支持代码高亮
- 文章分类与标签
- 简单的密码登录保护后台
- 明亮和暗色主题切换
- 自动生成 `sitemap.xml` 和 `rss.xml`

## 安装与运行

1. **创建虚拟环境（推荐）**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```
3. **运行应用**
   ```bash
   python app.py
   ```
   默认情况下博客会运行在 `http://localhost:5000`。

默认管理员密码可通过环境变量 `ADMIN_PASSWORD` 设置（默认为 `password`）。

## 备注

此项目适合作为个人博客或学习 Flask 的示例，功能简单，可在此基础上继续扩展。
