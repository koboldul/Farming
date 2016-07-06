var viewLogs = function(){
	$.ajax({
		url: 'http://192.168.2.4:3000/getLogFile'
	}).then(function(data) {
		$('#log').text(data)
	});
};

var toggleDevice = function(d, isStart){
	var data = {};
	data.device = d;
	data.isStart = isStart;
	$.ajax({
		url: 'http://192.168.2.4:3000/toggleDevice',
		type: 'POST',
		data: data
	}).then(function(data){
		$('#log').text(data)
	});
}; 
