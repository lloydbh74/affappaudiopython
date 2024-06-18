const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

console.log("Webhook route initialized.");

// Middleware to validate incoming webhook requests
router.post('/webhook', (req, res) => {
  const { body } = req;

  console.log("Webhook request received:", body);

  if (!body || typeof body !== 'object') {
    console.error('Invalid request format');
    return res.status(400).json({ error: 'Invalid request format' });
  }

  // If request is valid, proceed to the next step
  console.log('Request received and validated');

  // Task 2: Implement audio selection logic
  try {
    const introDir = path.join(__dirname, '../audio/intro');
    const outroDir = path.join(__dirname, '../audio/outro');

    const introFiles = fs.readdirSync(introDir);
    const outroFiles = fs.readdirSync(outroDir);

    if (introFiles.length === 0 || outroFiles.length === 0) {
      throw new Error('No intro or outro files found');
    }

    const selectedIntro = introFiles[Math.floor(Math.random() * introFiles.length)];
    const selectedOutro = outroFiles[Math.floor(Math.random() * outroFiles.length)];

    const introPath = path.join(introDir, selectedIntro);
    const outroPath = path.join(outroDir, selectedOutro);

    console.log(`Selected intro: ${selectedIntro}`);
    console.log(`Selected outro: ${selectedOutro}`);

    // Proceed to the next steps (placeholder for now)
    res.status(200).json({
      message: 'Request received and validated',
      introPath,
      outroPath,
    });
  } catch (error) {
    console.error(`Error during audio selection: ${error.message}`);
    console.error(error.stack);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;