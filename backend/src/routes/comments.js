const express = require('express');
const Comment = require('../models/Comment');
const auth = require('../middleware/auth');

const router = express.Router({ mergeParams: true });

router.get('/', async (req, res) => {
  const comments = await Comment.find({ post: req.params.postId })
    .populate('author', 'username')
    .sort({ createdAt: 1 });
  res.json(comments);
});

router.post('/', auth, async (req, res) => {
  const { content, parentComment } = req.body;
  const comment = new Comment({
    post: req.params.postId,
    author: req.user._id,
    content,
    parentComment: parentComment || null
  });
  await comment.save();
  res.status(201).json(comment);
});

module.exports = router;
