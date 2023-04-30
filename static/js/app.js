
// get the current protocol and domain name
var siteURL = window.location.protocol + "//" + window.location.host
var radioEndpoint = "/radio/"
var nowPlayingBlock = document.getElementById("now-playing")
var radioStatus = nowPlayingBlock.querySelector('h3')
var stationName = nowPlayingBlock.querySelector('h4')
var links = document.getElementsByClassName('station');
	

function setNewAction( playOrStop ) {
	if ( playOrStop == "stop" ) {
			var newAction = "play"	
		} else {
			var newAction = "stop"
		}
	return newAction
}


function getStationInfo( station ) {
	var request = new XMLHttpRequest();
	var url = siteURL + radioEndpoint
	request.open('GET', url, false)
	request.send()
	var data = JSON.parse(request.response)
	return data
}


function newActionText( newAction, station ) {
	if ( newAction == "play" ) {
		radioStatus.textContent = "Nothing playing now"
		stationName.textContent = "Choose a station below"
		var newTextStation = "Play " 
	} else {
		radioStatus.textContent = "Now Playing"
		stationName.removeAttribute('hidden')
		if ( station == "889" ) {
			var stationText = getStationInfo(station)
			stationName.textContent = stationText['now_playing'] + " on " + station
		} else {
			stationName.textContent = station
		}
		var newTextStation = "Stop "
	}
	return newTextStation
	}


// When a link with the class `station` is clicked, get the data-station and 
// data-action attributes. Then, send a GET request to the siteURL + radioEndpoint
// with the `data-action` in the URL.
for (var i = 0; i < links.length; i++) {
	links[i].addEventListener('click', function(e) {
		e.preventDefault();
		var playOrStop = this.getAttribute('data-action')
		var newAction = setNewAction( playOrStop )
		var station = this.getAttribute('data-station')
		
		var url = siteURL + radioEndpoint + station + "?"+playOrStop
		var request = new XMLHttpRequest();

		request.open('GET', url, true);
		request.send();
		
		this.setAttribute('data-action', newAction)
		var newTextStation = newActionText(newAction, station)	
		this.textContent = newTextStation + this.getAttribute('data-station')
	});
}