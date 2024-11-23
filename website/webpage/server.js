import express from "express";

const app = express();
const port = 3000;

app.use(express.static("static"));

app.get("/", (req, res) => {
    res.render('index.ejs');
})

app.get("/team", (req, res) => {
    res.render('team.ejs');
});

app.get("/detect", (req, res) => {
    res.render('detector.ejs');
})

app.get("/model", (req, res) => {
    res.render('tech-arch.ejs');
})

app.get("/dashboard", (req, res) => {
    res.render('dashboard.ejs');
})

app.get("/register", (req, res) => {
    res.render('register.ejs');
});

app.get("/login", (req, res) => {
    res.render('login.ejs');
});

app.listen(port, () => {
    console.log(`Listening on port ${port}.`);
});