<html>
<head>
<title>Spellchecker | Don McCurdy, 2012</title>
<script type="text/javascript" src="./assets/js/jquery-1.7.1.min.js"></script>
<script type="text/javascript">
correct_up = false;
sorry_up = false;
unknown_up = false;
error_up = false;

$('form input').keydown(function (e) { //If 'enter' key is pressed, check spelling
    if (e.keyCode == 13) {
        e.preventDefault();
        checkSpelling();
        return false;
    }
});

function checkSpelling()  //Submit text to server, display a result
{
	word = document.getElementById("textSource").value;	//input text
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("GET","./query.php?word="+word,true);	//call PHP script query.php
	xmlHttp.onreadystatechange=function()
	{
		s = xmlHttp.responseText;
		delay = 151;	//default delay, in case there's a panel to hide
		if (sorry_up) { //hide any panels that are already up
			$("#sorry_panel").fadeOut(150); 
			sorry_up = false;
		} else if (correct_up) { 
			$("#correct_panel").fadeOut(150); 
			correct_up = false;
		} else if (error_up) { 
			$("#error_panel").fadeOut(150); 
			error_up = false;
		} else if (unknown_up) { 
			$("#unknown_panel").fadeOut(150); 
			unknown_up = false;
		}
	
		if (xmlHttp.readyState==4 && word != "")
		{		
			if (s == "SERVER_EMPTY_RESPONSE") {	//if server doesn't find close matches
				$("#unknown_panel").delay(delay).fadeIn(600);
				unknown_up = true;
			} else if (s == "SERVER_ERROR"){	//if the server isn't responding.
				$("#error_panel").delay(delay).fadeIn(600);
				error_up = true;
			} else if (s == word) {				//word was correct
				$("#correct_panel").delay(delay).fadeIn(600);
				correct_up = true;
			} else {							//if incorrect, suggest something close
				$("#sorry_panel").delay(delay).fadeIn(600);
				$('#guess').delay(delay).queue( function(n) { $(this).html(s); n(); });
				sorry_up = true;		
			}
		}
	}
	xmlHttp.send(null);
}
</script>
<link href="./assets/css/global.css" rel="stylesheet" type="text/css" />
<link href='http://fonts.googleapis.com/css?family=Cabin+Sketch:700' rel='stylesheet' type='text/css'>
</head>

<body>

<center>
<div id="wrapper">

	<div id="entry_panel"><form>
	<input id="textSource" type="text" onkeypress="{if (event.keyCode == 13) checkSpelling()}" placeholder="type a word" ></input>
	<input id="dummyInput" type="text"></input>
	<a id="check_button" href="#" onclick="checkSpelling()"><img src="./assets/images/button.png" alt="Check"></img></a>
	</form></div>
	
	<div id="correct_panel" class="panel"></div>
	<div id="sorry_panel" class="panel"><p id="guess"></p></div>
	<div id="unknown_panel" class="panel"></div>
	<div id="error_panel" class="panel"></div>
</div>
</center>

</body>
</html>