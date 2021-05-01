const express = require('express');
const {spawn} = require('child_process');
const session = require('express-session');

const { v4: uuidv4 } = require('uuid');
const app = express();
const path = require('path');

app.set("view options", {layout: false});
app.use(express.static(__dirname + '/'));

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


app.get('/login', (req, res) => {
  console.log("hello1")
  var dataToSend;

  const python = spawn('python', ['fetchContest.py']);
  python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
  });

  python.on('close', (code) => {
  console.log(`child process close all stdio with code ${code}`);
  res.send(dataToSend)

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