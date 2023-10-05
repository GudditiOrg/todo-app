const swaggerJsdoc = require('swagger-jsdoc');

const options = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'To-Do List API',
            version: '1.0.0',
            description: 'A simple To-Do list API using Node.js, Express, and MongoDB.'
        },
        servers: [
            {
                url: 'http://localhost:3000',
                description: 'Development server'
            }
        ]
    },
    apis: ['./routes/tasks.js']
};

const specs = swaggerJsdoc(options);

module.exports = specs;
