"use strict";

function showGiphy(evt) {
	evt.preventDefault();
	var query = $("#query").val()

	$.get("/get_giphy_key", function(key){
		// calls the giphy API and returns data
		$.get("http://api.giphy.com/v1/gifs/search?q="+query+"&api_key="+key, function(data){
			
			// console.log(data)

			// data is a list of nested dicts 
			var giphy_data = data
			// console.log(giphy_data)

			// http://i.giphy.com/W3QKEujo8vztC.gif
			// http://i.giphy.com/W3QKEujo8vztC.gif

			for (var i=0; i < giphy_data.data.length; i++){
				// console.log(giphy_data.data[i].id)
				var giphy_id = giphy_data.data[i].id
				var url	= "http://i.giphy.com/" + giphy_id + ".gif"
				console.log(url)
				$('#giphy-field').append('<img src=' + url + ' width="75" height="75" >');

			}
  });
})
}
$('#getGiphy').on('click', showGiphy);


// $('img#giphy') function(){
//     $('img#giphy').attr('src', "");
// });

// $("p").append(" <b>Appended text</b>.");
   