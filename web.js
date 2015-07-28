
var fs = require('fs');
var express = require('express');
var pythonshell = require('python-shell');
var xml2js = require('xml2js');
var util = require('util');
var bodyParser = require('body-parser');

var app = express();
var parser = new xml2js.Parser();

var mainfile = "main.html";

var resultfile = "result.json";

app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); // to support JSON-encoded bodies

app.use(express.static(__dirname+'/static'));

app.get('/main', function(req,res){

  var mainhtml = fs.readFileSync(mainfile).toString();
  res.send(mainhtml)
});

app.post('/temp',function(req,res){

    var bodytag = JSON.stringify(req.body)
    var headertag = JSON.stringify(req.headers)
    var routetag = JSON.stringify(req.route.path)
    var methodtag = JSON.stringify(req.method)
 
    var logobject = new Object();

    logobject["REQUEST"] = [headertag, routetag, methodtag, bodytag]
    logobject["RESPONSE"] = "HELLO!";

    var jsonlogobject = JSON.stringify(logobject)
    var options = {
	mode:'text',
	args: [jsonlogobject],
	pythonOptions: ['-u'],
	scriptPath: '/home/ubuntu/Hackathon/Code'
    }
    
    pythonshell.run('KafkaInterface.py',options,function(err,results){
        if(err) throw err;
        console.log(results)
    });
   
    /*
    var nodes = req.body.objectslist;
    var coorrdinates = req.body.colist;
    
    var jsonnodes = JSON.stringify(nodes)
    var coordinatesnodes = JSON.stringify(coorrdinates)
    console.log(jsonnodes)
    console.log(coordinatesnodes)
    var options = {
      mode:'text',
      args: [jsonnodes,coordinatesnodes],
      pythonOptions: ['-u'],
      scriptPath: '/home/ubuntu/Hackathon/Code'
    }
    
    console.log(jsonnodes)
    console.log(coordinatesnodes)

    pythonshell.run('queryfile.py',options,function(err,results){
        if(err) throw err;
        console.log(results)
    });   
    */
    res.send(200);
});

app.post('/test', function(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.send(JSON.stringify({a:1}));
});

app.post('/getcoordinates',function(req,res){

  var lat1 = req.body.lat1;
  var long1 = req.body.long1;
  var lat2 = req.body.lat2;
  var long2 = req.body.long2;

  var options = {
      mode: 'text',
      args: [lat1,long1,lat2,long2],
      pythonOptions: ['-u'],
      scriptPath: '/home/master/DBLP/dblp_phd_app/'
    };

      pythonshell.run('findcoordinates.py',options,function(err,results){
        if(err) throw err;
        
        var coorrdinates = []
        for( result in results)
        {
            var alpha = results[result].split(", ")
            var beta = alpha[0].substring(1,alpha[0].length)
            var gamma = alpha[1].substring(0,alpha[1].length-1)

            beta =parseFloat(beta)
            gamma = parseFloat(gamma)
            var temp = []
            temp.push(beta,gamma)
            coorrdinates.push(temp)
        }
        res.send(coorrdinates);
      });
});

var port = process.env.PORT || 8080;
app.listen(port, function() {
console.log("Listening on " + port);
});


//AUTHORS DETAILS DATA ENDS

var authorstext;

app.post('/tempresult',function(req,res){
  var resultdata = fs.readFileSync(resultfile).toString();
  res.send(resultdata);
});

app.post('/getlocation', function (req, res) {

  var name = req.body.name.toString().toLowerCase(); 
  var article = req.body.article.toString().toLowerCase(); 

  parser.parseString(authorstext,function(err,result){
    
    var authors = result.dblp;
  
    var articles = authors.article;
  
    for(i=0;i < articles.length;i++)
    {
      
      var articletitle = articles[i].title.toString().toLowerCase();
      var url = articles[i].ee.toString();
      var keys = articles[i].$;

      if(articletitle == article)
      {
          console.log(keys);
          console.log(url);
          var options = {
          mode: 'text',
          args: [url,keys.mdate,keys.key],
          pythonOptions: ['-u'],
          scriptPath: '/home/master/DBLP/dblp_phd_app/'
        };

        pythonshell.run('findloc.py',options,function(err,results){
          if(err) throw err;
          console.log(results.toString());
          res.send(results.toString());
        });
      }
    }
  });    
});


  
