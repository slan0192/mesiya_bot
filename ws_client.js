var url = 'ws://localhost:9001/'
var status = ""

var init_ws = function(tp) {
	var html_file = "restaurants.html";
	if (tp == "sakaya") {
		html_file = "tavern.html";
  	}

	var ws = new WebSocket(url);
	ws.onopen = function() {
		status += "server connected\n";
		document.getElementById('status').innerHTML = status;
	};

  	ws.onerror = function(event) {
		status += "Error!\n";
		document.getElementById('status').innerHTML = status;
		ws.close()
	};

	ws.onmessage = function(event) {
		status += "recv: " + event.data + "\n";
		document.getElementById('status').innerHTML = status;
		if (event.data == "finished") {
			ws.close()
			location.href = html_file;
		}
	};

	ws.onclose = function() {
		ws.close();
	};

	window.onbeforeunload = function() {
		ws.close();
	}
}	
