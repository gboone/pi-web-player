
// get the current protocol and domain name
var siteURL = window.location.protocol + "//" + window.location.host
var radioEndpoint = "/radio/"
var nowPlayingBlock = document.getElementById("now-playing")
var radioStatus = nowPlayingBlock.querySelector('h3')
var stationName = nowPlayingBlock.querySelector('h4')
var buttons = document.getElementsByClassName('station');
var stopAllButton = document.getElementById("button-stop-all")

function setNewAction( playOrStop ) {
	if ( playOrStop == "stop" ) {
			var newAction = "play"	
		} else {
			var newAction = "stop"
		}
	return newAction
}


function getNewURL( url, newAction ) {
	if ( newAction == "play" ) {
		var url = url.replace("stop", "play")
	} else {
		var url = url.replace("play", "stop")
	}
	return url
}


function getStationInfo( station ) {
	var request = new XMLHttpRequest();

	var url = siteURL + radioEndpoint
	console.log(url)
	request.open('GET', url, true)
	request.send()
	console.log(JSON.parse(request.response)['now_playing'])
	var data = JSON.parse(request.response)
	return data
}


function newActionText( newAction, station ) {
	if ( newAction == "play" ) {
		radioStatus.textContent = "Nothing playing now"
		stationName.textContent = "Choose a station below"
		var newTextStation = "Play" 
	} else {
		radioStatus.textContent = "Now playing: " + station
		stationName.removeAttribute('hidden')
		var newTextStation = "Stop"
	}
	return newTextStation
	}


// When a link with the class `station` is clicked, get the data-station and 
// data-action attributes. Then, send a GET request to the siteURL + radioEndpoint
// with the `data-action` in the URL.
for (var i = 0; i < buttons.length; i++) {
	buttons[i].addEventListener('click', function(e) {
		e.preventDefault();
		var playOrStop = this.getAttribute('data-action')
		var url = this.getAttribute('data-target')
		var station = this.getAttribute('data-station')
		// the stop all button will have data-station "all" and data-action "stop-all"
		// when this happens, we need to set the URL to "/radio/stop-all/"

		var request = new XMLHttpRequest();

		request.open('GET', url, true);
		request.onload = () => {
			if ( request.status == 200 ) {
				console.log("Radio station " + station + " did: " + playOrStop)
			} else {
				console.log("Radio station " + station + " failed to " + playOrStop + " with status " + request.status)
			}
		}
		request.send();
		// update buttons with new actions, text, and URLs
		var newAction = setNewAction( playOrStop )
		this.setAttribute('data-action', newAction)
		var newTextStation = newActionText(newAction, station)
		this.textContent = newTextStation
		var newURL = getNewURL( url, newAction )
		this.setAttribute('data-target', newURL)
	});


}