const express = require('express');
const {spawn} = require('child_process');
const session = require('express-session');

const { v4: uuidv4 } = require('uuid');
const app = express();
const path = require('path');

app.set("view options", {layout: false});
app.use(express.static(__dirname + '/'));
//app.engine('html', require('ejs').renderFile);
app.set('view engine', 'ejs');
var mysql = require('mysql');

var con = mysql.createConnection(
	{
	host: "localhost",
	user: "root",
	password: "",
	database: "capstone",
	insecureAuth : true
	}
);

con.connect(

	function(err)
	{
		if (err) throw err;
	}
);

app.use(session({
  genid: (req) => {
    console.log('Inside the session middleware');
    console.log(req.sessionID);
    return uuidv4();
  },
  secret: 'keyboard cat',
  resave: false,
  saveUninitialized: true
}));


app.get('/CodersGym', (req, res) => {
  res.render(__dirname +'/Frontend/Landing Page-Final/cards.html')
  //res.send(dataToSend)

  });

app.get('/UpcomingContests', (req, res) => {
    var dataToSend;

    const python = spawn('python', ['fetchContest.py']);
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    });

    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend)
    console.log(dataToSend[0])
    res.render(__dirname +'/Frontend/Problem+Challenges-Final/FinalChallengesModule',{testing: "hello"})
  });
  });

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: true }));


app.post('/login', (req, res) => {
 console.log("hello")
 console.log(req.body.username)
 res.render(path.join(__dirname+'/login.html'));
});

app.listen(3000);