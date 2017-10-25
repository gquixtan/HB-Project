// makes a request to giphy API and sends the response back to the client.

"use strict";

// var listOfGiphs = [];
var giphy_url = " ";

function showGiphy(evt) {
	evt.preventDefault();

	// obtains the keyword from the user to do the giphy query.
	var query = $("#query").val();


	// giphy's key.
	$.get("/get_giphy_key", function(key){

		// calls the giphy API and returns data
		$.get("http://api.giphy.com/v1/gifs/search?q="+query+"&api_key="+key, function(data){
			
			// console.log(data)

			// data is a dict that has a list of nested dicts.
			var giphy_data = data;

			// loops through the list and gets the giphy id
			for (var i=0; i < giphy_data.data.length; i++){
				// console.log(giphy_data.data[i].id)
				

				// giphy id.
				var giphy_id = giphy_data.data[i].id;

				// testing urls
				// var url = giphy_data.data[i].original.url
				// console.log(url)

				// the url for giphys
				var url	= "http://i.giphy.com/" + giphy_id + ".gif";
				// console.log(url)

				// url example:
				// http://i.giphy.com/W3QKEujo8vztC.gif

				// for img (height="75" width="75")
				$('#giphy-field').append('<button><img class="url" src=' + url + ' width="200" height="200"></button>');
			}

			$('button img').click(function(){

				// THIS SAVES THE URL THAT USER CHOOSES TO SEND OUT AS A TEXT
				giphy_url = (this.src);
				console.log(giphy_url);				

				// this creates a list of giphys
				// listOfGiphs.push(this.src)
				// console.log(listOfGiphs);
			});
  			
		});
	});
}

function getUrl(evt){
	evt.preventDefault();

	var date = $("#date2").val();
	var phone = $("#phone2").val();
	console.log(date);
	console.log(phone);

	$.get("/geturl", {
		"date" : date,
		"phone" : phone,
		"url": giphy_url
		// "urls": listOfGiphs[0]
	}, function(){
		alert("Your texts has been submitted!");
		$("#form2").submit();
	});
}
$("#send-url").on("click", getUrl);
$('#getGiphy').on('click', showGiphy);
   