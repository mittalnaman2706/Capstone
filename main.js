const express = require('express');
const {spawn} = require('child_process');
const session = require('express-session');

const { v4: uuidv4 } = require('uuid');
const app = express();
const path = require('path');

app.set("view options", {layout: false});
app.use(express.static(__dirname + '/'));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'ejs');
app.set('views',path.join(__dirname, 'views'))
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

app.get('/Analysis', (req, res) => {
  res.render(__dirname +'/Frontend/Profile Analyser/index')
  //res.send(dataToSend)

  });

//app.set('view engine', 'ejs');
app.get('/UpcomingContests', (req, res) => {
    var dataToSend;

    const python = spawn('python', ['fetchContest.py']);
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend += data.toString();
    });

    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);

    dataToSend = dataToSend.split("\n")

    var arrayLength = dataToSend.length;
    var contests = new Array();

    for (var i = 1; i < arrayLength; i++) {
         data = dataToSend[i].split(",")

         var tempList = new Array();
         var tempList = [];

         for(var j = 0; j < data.length; j++)
         {
            var s

            var l = data[j].length

            if (j==0)
                s = data[j].slice(2, l-1)
            else if (j==1)
                s = data[j].slice(2, -1)
            else if(j==2 || j==7)
                s = data[j].substr(19, l-19)
            else if(j==6 || j==11)
                s = data[j].slice(1, l-1)
            else if(j==12)
                s = data[j].slice(2, l-3)
            else
                s = data[j].slice(1, l)
            tempList.push(s)
         }

         var temp2 = new Array();
         var temp2 = [];

         for(var j = 0; j<tempList.length;j++)
         {
             if(j==2 || j==7)
             {
                 var temp

                 temp="-"
                 temp += tempList[j]
                 j++

                 temp = tempList[j] + temp
                 temp = "-" + temp
                 j++;

                 temp = tempList[j] + temp
                 j++;
                 temp += " "

                 temp += tempList[j]
                 j++;
                 temp += ":"

                 temp += tempList[j]
                 temp += ":"

                 temp+= "00"

                 temp2.push(temp)
             }

             else
                 temp2.push(tempList[j])

         }

            for(var j = 0;j<temp2.length;j++)
                console.log(temp2[j])

            contests.push(temp2)
        }

    res.render(__dirname +'/Frontend/Problem+Challenges-Final/FinalChallengesModule',{contests: contests})
  });
  });

app.get('/PracticeProblems', (req, res) => {
    var dataToSend;

    const python = spawn('python', ['fetchProblems.py']);
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend += data.toString();
    });

    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    dataToSend = dataToSend.split("\n")

    var arrayLength = dataToSend.length;
    var problems = new Array();

    for (var i = 1; i < arrayLength-1; i++) {
        data = dataToSend[i].split(",")

        var tempList = new Array();
        var tempList = [];

        for(var j = 0; j < 4; j++)
        {
            var s
            var l = data[j].length

            if (j==0)
                s = data[j].slice(6, -7)
            else
                s = data[j].slice(2, -1)

            tempList.push(s)
        }
            problems.push(tempList)
    }

    //for(var i=0;i<problems.length;i++)
    //console.log(problems[i][2])

    res.render(__dirname +'/Frontend/Problem+Challenges-Final/FinalProblemsModule',{problems:problems})
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