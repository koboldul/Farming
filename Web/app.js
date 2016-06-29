var express = require('express')
  , logger = require('morgan')
  , app = express()
  , template = require('pug').compileFile(__dirname + '/templates/homepage.pug')
var fs = require ('fs')
var py_console = require('python-shell')
var bp = require('body-parser')

app.use(logger('dev'))
app.use(express.static(__dirname + '/static'))
app.use(express.static(__dirname + '/client_scripts'))
app.use(bp.urlencoded({ extend: false }));
app.use(bp.json());

app.get('/', function (req, res, next) {
  try {
    var html = template({ title: 'Home' })
    res.send(html)
  } catch (e) {
    next(e)
  }
});

app.get('/getLogFile', function(req, resp) {
	console.log('hit')
	file_p = __dirname + '/../farming.log'
	fs.readFile(file_p, 'utf8', function(err, data) {
		if (err) {
			console.log(err.toString());
			resp.end(err.toString());
		}
		else {
			resp.end(data);
		}
	})
});	

app.post('/toggleDevice', function(req, resp) {
	var device = req.body.device;
	var isStart = req.body.isStart;
	args = []
	if (isStart == 'true'){
		args.push(device)
	}
	else{
		args.push('s')
	}
	
	console.log(args)
	py_console.run('led.py', { scriptPath: __dirname + '/../', args: args  }, 
		function(err, result){
			if (err) {
				console.log(err.toString());
				resp.end(err.toString());
			}
			else {
				console.log('results: %j', result);
				resp.end(result.toString());	
			}
		});
});

app.listen(process.env.PORT || 3000, function () {
  console.log('Listening on http://localhost:' + (process.env.PORT || 3000))
});
	
