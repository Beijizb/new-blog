const express = require('express');
const slugify = require('slugify');
const Post = require('../models/Post');
const auth = require('../middleware/auth');
const commentRoutes = require('./comments');

const router = express.Router();

router.get('/', async (req, res) => {
  const { page = 1, limit = 10 } = req.query;
  const posts = await Post.find({ status: 'published' })
    .skip((page - 1) * limit)
    .limit(Number(limit))
    .populate('author', 'username');
  res.json(posts);
});

router.get('/:slug', async (req, res) => {
  const post = await Post.findOne({ slug: req.params.slug })
    .populate('author', 'username')
    .populate('categories')
    .populate('tags');
  if (!post) return res.status(404).json({ message: 'Not found' });
  res.json(post);
});

router.post('/', auth, async (req, res) => {
  const { title, content, categories, tags, status } = req.body;
  const slug = slugify(title, { lower: true, strict: true });
  const post = new Post({
    title,
    content,
    slug,
    author: req.user._id,
    categories,
    tags,
    status: status || 'draft'
  });
  await post.save();
  res.status(201).json(post);
});

router.put('/:id', auth, async (req, res) => {
  const post = await Post.findById(req.params.id);
  if (!post) return res.status(404).json({ message: 'Not found' });
  if (post.author.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
    return res.status(403).json({ message: 'Forbidden' });
  }
  Object.assign(post, req.body);
  if (req.body.title) {
    post.slug = slugify(req.body.title, { lower: true, strict: true });
  }
  await post.save();
  res.json(post);
});

router.delete('/:id', auth, async (req, res) => {
  const post = await Post.findById(req.params.id);
  if (!post) return res.status(404).json({ message: 'Not found' });
  if (post.author.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
    return res.status(403).json({ message: 'Forbidden' });
  }
  await post.deleteOne();
  res.json({ message: 'Post deleted' });
});

router.use('/:postId/comments', commentRoutes);

module.exports = router;
