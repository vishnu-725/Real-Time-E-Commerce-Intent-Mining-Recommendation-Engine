const { Client } = require("pg");

let client;

async function connect() {
    client = new Client({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASS,
        database: process.env.DB_NAME,
        port: 5432
    });

    await client.connect();
}

module.exports = { connect };
