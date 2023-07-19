const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 80;

// Parse JSON data sent in requests
app.use(bodyParser.json());

// Define a sample route
app.get('/', (req, res) => {
  res.send('Hello, this is your Node.js web server running on port 80!');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
