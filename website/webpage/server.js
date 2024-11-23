import express from "express";
import bodyParser from "body-parser";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();
const port = 3000;

app.use(express.static(__dirname + "/static"));

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

app.get("/register", (req, res) => {
    res.sendFile(__dirname + "/static/register.html");
});


app.listen(port, () => {
    console.log(`Listening on port ${port}.`);
});
