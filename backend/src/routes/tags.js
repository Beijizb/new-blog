const express = require('express');
const Tag = require('../models/Tag');
const auth = require('../middleware/auth');

const router = express.Router();

router.get('/', async (req, res) => {
  const tags = await Tag.find();
  res.json(tags);
});

router.post('/', auth, async (req, res) => {
  const tag = new Tag(req.body);
  await tag.save();
  res.status(201).json(tag);
});

router.put('/:id', auth, async (req, res) => {
  const tag = await Tag.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(tag);
});

router.delete('/:id', auth, async (req, res) => {
  await Tag.findByIdAndDelete(req.params.id);
  res.json({ message: 'Tag deleted' });
});

module.exports = router;
