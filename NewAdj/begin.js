/* Replication of Culbertson & Adger U20 experiment -- POV design
 * Manipulating the type of adjective based on pmi calculation on the Brown corpus
 * - set up global variables
 * - show IRB information
 * - show intro instructions
 * - read lists (external function)
 * - show training instructions
 * - do training trials
 * - pass on to testAndFinish to run testing trials, collect demographic info, collate responses, and submit
 */
 
/* * * * * * * * * * * * * 
 * Global variables
 * * * * * * * * * * * * */
var url = "";
var subjID = new Date().toString();
var workerId = "NOTAREALWORKERID1"; // needs to be set (rather than undefined) to allow people to preview the HIT
var assignId = "";
var hitId = "";
var assignId = "NOTAREALASSIGNMENTID1"; // needs to be set (rather than undefined) to allow data to be written to blake during debugging
var hitId = "NOTAREALHITID1"; // needs to be set (rather than undefined) to allow data to be written to blake during debugging
var condition = "";
var debug = "NA"

var vocabList = [];
var nouns = [];
var adj_original = [];
var adj_inner = [];
var adj_outer = [];
var num =[];

var trainIndx = 0;
var firstTrainTrial = true;
var trainTrials = [];

var testIndx = 0;
var firstTestTrial = true;
var testTrials = [];
var testResponses = [];
var dataAccumulator = []; //this is where trial data will be stored

var AUDIOAFFIX = '';

// * * * * * * * * * * * * * * * * * * * * * * * * * *
//  * function to send data to server online
//  * * * * * * * * * * * * * * * * * * * * * * * * * *
// Send data to server and write it to a file
//uses PHP file on other end to write to file
function writeDataToBlake(data) {
	//console.log(data['trial'])
  	data['workerId']=workerId
  	data['assignmentId']=assignId
  	data['hitId']=hitId
  	data['condition']=condition
  	$.ajax({
  		type: 'POST',
  		url: 'save_data_U20NewAdj.php',//url of receiver file on server
  		//url: 'savetest.php',//url of receiver file on server
  		data:data,
  		cache:false,
  		// success: function(html) {
// 				alert("Submitted! Thanks!");
// 			}
	});
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * *
 * parse url, set condition, etc. on document ready
 * * * * * * * * * * * * * * * * * * * * * * * * * * */
$(document).ready(function() {
	url = ''+window.location;
	var params = url.split("?")[1].split("&");
	for (var i=0; i<params.length; i++) { 
		var name = params[i].split("=")[0];
		var value = params[i].split("=")[1];
		if (name=="assignmentId") {
			assignId = value;
		}
		if (name=="hitId") {
			hitId = value;
		}
		if (name=="workerId") {
			workerId = value;
		}
		if (name=="condition") {
			condition = value;
		}
		if (name=="debug") {
			debug = value;
		}
	}
	//doIRBInformation();
	readWorkerIDList();	// normal operation - check ID, then preload stims etc
});

/* * * * * * * * * * * * 
 * check for retakes
 * * * * * * * * * * * */
function readWorkerIDList() {
	//console.log("attempting to read list of IDs...");
	$.ajax({
		url : "U20NewAdj/workerIDs.csv",
		//url : "https://s3.amazonaws.com/linglabgmufiles/U20NewAdj/U20NewAdj/workerIDs.csv",
		dataType : "text",
		cache : false,
		success : function(text, status, jqXHR) {
			// get list of workerIds from file after http request

			idsList = text.split("\n");
			checkRetakes();
		},
		error : function(x, text, error) {
			alert(error);
		}
	});
}

function checkRetakes() {
	//console.log('workerId:'+workerId)
	var redo = 0;
    //console.log("Here're the IDs I found:")
    for (var i=0; i<idsList.length; i++) {
 		//console.log(idsList[i])
    	if (workerId==idsList[i]) {	
			redo=1;
		}
	}
    if (redo==1) {
        var div1 = document.createElement('h2');
		div1.id = "welcomeDiv";
		document.body.appendChild(div1);
		$('#welcomeDiv')
			.append('<p>This is an experiment about learning a small part of a new language. There are simple phrases with English words in an unusual order.</p>')
			.append('<p>Sorry, but our records show that you have already completed this HIT (or one closely related to it). Please help us out and click \'Return HIT\' and don\'t complete this one. We apologize for the inconvenience!</p>')
			.css({ 'font-size': '16px', 'color':'red'})
	}
    else {
    	//console.log('workerId not found')
    	doIRBInformation(); // normal operation
	}
}


/* * * * * * * * * * * * 
 * present IRB information
 * * * * * * * * * * * */
function doIRBInformation() {
	
	var div1 = document.createElement('h2');
	div1.id = "welcomeDiv";
	document.body.appendChild(div1);
	$('#welcomeDiv')
		.append('<p> Welcome! </p>')
		
	// audio element for determining which type of audio file to use
	var audio1 = document.createElement('audio');
	audio1.id = "audio1";
	audio1.removeAttribute('controls');
	div1.appendChild(audio1);

	//got this audio switching business from https://developer.mozilla.org/en-US/Apps/Fundamentals/Audio_and_video_delivery/Cross-browser_audio_basics
	//uses AUDIOAFFIX as a global variable to store the correct audio file extension
	if (audio1.canPlayType('audio/ogg')) {
		AUDIOAFFIX = ".ogg";
	}
	else if (audio1.canPlayType('audio/mpeg')) {
		AUDIOAFFIX= ".mp3";
	}
	else if (audio1.canPlayType('audio/aac')) {
		AUDIOAFFIX= ".aac";
	}
	console.log(AUDIOAFFIX)
	
	var div2 = document.createElement('div');
	div2.id = "irbDiv";
	document.body.appendChild(div2);
	$('#irbDiv')
		.attr('class','ui-widget')
		.append('<p> This is an experiment about learning a small part of a new language. It will take about 20 minutes to complete and you will be paid $2.00 for your time. This experiment is part of a series of studies being conducted by Dr. Jennifer Culbertson at the University of Edinburgh, and has been approved by the Linguistics and English Language Ethics Committee. Please <a href="MultiAdj/InformationForm.pdf">click here</a> to download a study information letter (pdf) that provides further information about the study.</p>\
		<p> Clicking on the <b> agree </b> button below indicates that:\
		<ul>\
		<li> you are a native speaker of English, at least 18 years old </li>\
		<li> you have read the information letter </li>\
		<li> you voluntarily agree to participate, and understand you can stop your participation at any time</li>\
		<li> you agree that your anonymous data may be kept permanently in Edinburgh University archives and may used by qualified researchers for teaching and research purposes</li>\
		</ul>\
		If you do not agree to all of these, please close this window in your browser now. </p>')
		.append('<p>This experiment requires you to listen to AUDIO. If your browser does not \
		support audio, or you are not in a quiet place, please do not agree to participate in this HIT.</p>')
	
	$('#irbDiv').append('<button id="acceptBtn">Accept</button>');
	$('#acceptBtn').button();
	
	$('#acceptBtn')
		.on('click', function() {
			document.body.removeChild(div1);
			document.body.removeChild(div2);
			// check for debugging, otherwise proceed to intro instructions
			if (debug=="train" | debug=="test") {
				createLex();
			} else if (debug=="demo") { 
				collectDemographics();
			} else { 
				showIntroInstructions(); 
			}
		});
}


/* * * * * * * * * * * * * * * * * * *
 * present introductory instructions
 * * * * * * * * * * * * * * * * * * */
function showIntroInstructions() {
	
	var div1 = document.createElement('h2');
	div1.id = "welcomeDiv";
	document.body.appendChild(div1);
	$('#welcomeDiv').append('<p> Welcome! </p>')
	
	var div2 = document.createElement('div');
	div2.id = "introDiv";
	document.body.appendChild(div2);
	$('#introDiv')
		.attr('class','ui-widget')
		.append('<p>In this experiment, you will be learning part of a new language. The language is similar to English, but you will notice some differences.</p>')
		.append('<p>Your task will be to learn to translate from English into the new language.</p>')
		.append('<p></p>')

	$('#introDiv').append('<button id="introBtn">Continue</button>');
	$('#introBtn').button();
	
	$('#introBtn')
		.on('click', function() {
			document.body.removeChild(div1);
			document.body.removeChild(div2);
			// check for debugging, otherwise proceed to intro instructions
			if (debug=="train" | debug=="test") {
				createLex();
			} else if (debug=="demo") { 
				collectDemographics();
			} else { 
				createLex();
			}
		});
}

/* * * * * * * * * * * * * * * * * * *
 * present training instructions
 * * * * * * * * * * * * * * * * * * */
function showTrainInstructions() {
	
	var div1 = document.createElement('h2');
	div1.id = "welcomeDiv";
	document.body.appendChild(div1);
	$('#welcomeDiv')
		.append('<p> Instructions -- please read carefully! </p>')
	
	var div2 = document.createElement('div');
	div2.id = "trainInstrDiv";
	document.body.appendChild(div2);
	$('#trainInstrDiv')
		.attr('class','ui-widget')
		.append('<p>Now you\'ll see a phrase in English, and hear a speaker of the language you\'re learning translate it.</p>')
		.append('<p>Look at the English phrase, listen to the speaker translate it, and then click on the translation that matches what you heard the speaker say.</p>')
		.append('<p>It\'s important to pay close attention, so that later on you\'ll be able to translate on your own.</p>')

	$('#trainInstrDiv').append('<button id="instrBtn">Begin</button>');
	$('#instrBtn').button();
	$('#instrBtn').button("disable");

	setTimeout(function() {
		$('#instrBtn').button("enable");
		$('#instrBtn')
			.on('click', function() {
				document.body.removeChild(div1);
				document.body.removeChild(div2);
				doTrainTrial();
			});
	}, 7000);
	//}, 500); //short for debugging
}