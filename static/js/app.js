
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

		var button = this
		var request = new XMLHttpRequest();

		button.textContent = "…"
		request.open('GET', url, true);
		request.onload = () => {
			var data = {}
			try {
				data = JSON.parse(request.response)
			} catch (err) {
				data = { status: "error", message: "Unexpected response from server" }
			}
			if ( request.status == 200 && data.status != "error" ) {
				console.log("Radio station " + station + " did: " + playOrStop)
				// update buttons with new actions, text, and URLs
				var newAction = setNewAction( playOrStop )
				button.setAttribute('data-action', newAction)
				var newTextStation = newActionText(newAction, station)
				button.textContent = newTextStation
				var newURL = getNewURL( url, newAction )
				button.setAttribute('data-target', newURL)
			} else {
				// Surface the failure in the now-playing block
				console.log("Radio station " + station + " failed to " + playOrStop + ": " + (data.message || "HTTP " + request.status))
				radioStatus.textContent = "⚠️ Couldn't play " + station
				stationName.textContent = data.message || "The stream failed to open. Check the stream URL and the Pi's network."
				stationName.removeAttribute('hidden')
				// leave the button as Play so the user can retry
				button.textContent = playOrStop == "play" ? "Play" : "Stop"
			}
		}
		request.onerror = () => {
			radioStatus.textContent = "⚠️ Couldn't reach the Pi"
			button.textContent = playOrStop == "play" ? "Play" : "Stop"
		}
		request.send();
	});


}