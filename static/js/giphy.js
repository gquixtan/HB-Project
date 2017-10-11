// makes a request to giphy API and sends the response back to the client.

"use strict";

function showGiphy(evt) {
	evt.preventDefault();

	// obtains the keyword from the user to do the giphy query.
	var query = $("#query").val()

	// giphy's key.
	$.get("/get_giphy_key", function(key){

		// calls the giphy API and returns data
		$.get("http://api.giphy.com/v1/gifs/search?q="+query+"&api_key="+key, function(data){
			
			// console.log(data)

			// data is a dict that has a list of nested dicts.
			var giphy_data = data
			// console.log(giphy_data)

			// loops through the list and gets the giphy id
			for (var i=0; i < giphy_data.data.length; i++){
				// console.log(giphy_data.data[i].id)

				// giphy id.
				var giphy_id = giphy_data.data[i].id

				// testing urls
				// var url = giphy_data.data[i].original.url
				// console.log(url)

				// the url for giphys
				var url	= "http://i.giphy.com/" + giphy_id + ".gif"
				// console.log(url)

				// url example:
				// http://i.giphy.com/W3QKEujo8vztC.gif

				// for img (height="75" width="75")
				$('#giphy-field').append('<img src=' + url + ' width="200" height="200" >');
			}
  });
})
}
$('#getGiphy').on('click', showGiphy);
   