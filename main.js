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

var username

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

app.get('/login', (req, res) => {
  res.render(__dirname +'/Frontend/Login/login')

  });

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));

app.post('/login', (req, res) => {
 username = req.body.username
 res.render(__dirname +'/Frontend/Landing Page-Final/cards.html')
});


app.get('/CodersGym', (req, res) => {
  res.render(__dirname +'/Frontend/Landing Page-Final/cards.html')

  });

app.get('/Analysis', (req, res) => {

   var dataToSend = ""

   const python = spawn('python', ['fetchProfile.py', username]);
   python.stdout.on('data', function (data) {
   console.log('Pipe data from python script ...');
   dataToSend += data.toString();
   });

  python.on('close', (code) => {
  console.log(`child process close all stdio with code ${code}`);
  dataToSend = dataToSend.split("\n")

  var username, rating, count, solved, average, submissions, easy, medium, beg, hard, partialac, tle, ac, runtimerr, compilerr, wrong
  username = dataToSend[0]
  rating = dataToSend[1]
  solved = dataToSend[2]
  submissions = dataToSend[3]
  average = dataToSend[4]
  easy = dataToSend[5]
  beg = dataToSend[6]
  medium = dataToSend[7]
  hard = dataToSend[8]

  partialac = dataToSend[9]
  tle = dataToSend[10]
  wrong = dataToSend[11]
  ac = dataToSend[12]
  compilerr = dataToSend[13]
  runtimerr = dataToSend[14]

  var tags = {}
  tags = dataToSend[15]
  console.log(tags)
  tags = tags.split(",")

  var map = {};
  for (var k in tags)
  {
      var tags2 = tags[k].split(":")
      tags2[0] = tags2[0].substr(1)

      if(k==(tags.length-1))
          tags2[1] = tags2[1].slice(0, tags2[1].length-2)

      map[tags2[0]] = tags2[1]
  }

  var label = []
  var val = []

  var l = ""
  var v = ""

  for (var k in map)
  {
     l += k + "$"
     map[k] = map[k].substr(1)
     v += map[k] + "$"
  }

  var label = l.split("$")
  var val = v.split("$")

  weakar = dataToSend[16]
  goodar = dataToSend[17]
  profar = dataToSend[18]

  easyrc = dataToSend[19]
  easyrl = dataToSend[20]

  mediumrc = dataToSend[21]
  mediumrl = dataToSend[22]

  hardrc = dataToSend[23]
  hardrl = dataToSend[24]

  console.log(weakar)
  console.log(goodar)
  console.log(profar)
  console.log(easyrc)
  console.log(easyrl)
  console.log(mediumrc)
  console.log(mediumrl)
  console.log(hardrc)
  console.log(hardrl)

  res.render(__dirname +'/Frontend/Profile Analyser/index',{username:username, rating:rating, solved:solved,
  submissions:submissions, average:average, easy:easy, beg:beg, medium:medium, hard:hard, partialac:partialac, tle:tle,
  wrong:wrong, ac:ac, compilerr:compilerr, runtimerr:runtimerr, l:l, v:v, username:username})
  });

  });

//app.set('view engine', 'ejs');
app.get('/UpcomingContests', (req, res) => {
    
    var dataToSend;

    const python = spawn('python', ['fetchContest.py']);
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend += data.toString();
    });

    console.log(dataToSend);

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

    // var dataToSend1;

    // const python = spawn('python', ['fetchContest.py']);
    // python.stdout.on('data', function (data) {
    // console.log('Pipe data from python script ...');
    // dataToSend += data.toString();
    // });

    // python.on('close', (code) => {
    // console.log(`child process close all stdio with code ${code}`);


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

    for (var i = 1; i < 6142; i++) {
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

    for (var i = 6143; i < arrayLength-1; i++) {
            data = dataToSend[i].split(",")

            var tempList = new Array();
            var tempList = [];

             for(var j = 0; j < 4; j++)
             {
                        var s = data[j]
                    var l = data[j].length

                    if (j==0)
                    s = data[j].slice(2, -1)
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

app.listen(3000);