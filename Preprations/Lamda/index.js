const axios = require('axios');

exports.handler = async (event) => {
  const websiteUrl = 'https://gnaganjaneyulu.blogspot.com/'; // Replace with the URL of the website you want to check

  try {
    const response = await axios.get(websiteUrl);

    if (response.status === 200) {
      return {
        statusCode: 200,
        body: 'Website is running,No action required .',
      };
    } else {
      return {
        statusCode: 500,
        body: 'Website is not running. Status code: ' + response.status,
      };
    }
  } catch (error) {
    return {
      statusCode: 500,
      body: 'Error occurred while checking website status: ' + error.message,
    };
  }
};
