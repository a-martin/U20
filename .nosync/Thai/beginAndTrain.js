/* Thai version of Culbertson & Adger U20 experiment -- POV design
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
var condition = "";
var debug = "NA"

var vocabList = [];
var nouns = [];
var adj = [];
var num =[];
var dem = [];

var trainIndx = 0;
var firstTrainTrial = true;
var trainTrials = [];

var testIndx = 0;
var firstTestTrial = true;
var testTrials = [];
var testResponses = [];

var AUDIOAFFIX = '';

/* * * * * * * * * * * * * * * * * * * * * * * * * * *
 * parse url, set condition, etc. on document ready
 * * * * * * * * * * * * * * * * * * * * * * * * * * */
$(document).ready(function() {
url = ''+window.location;
var params = url.split("?")[1].split("&");
for (var i=0; i<params.length; i++) { 
	var name = params[i].split("=")[0];
	var value = params[i].split("=")[1];
	if (name=="id") {
		subjID = value;
	}
	if (name=="condition") {
		condition = value;
	}
	if (name=="debug") {
		debug = value;
	}
}
//doIRBInformation();
showIntroInstructions(); 
});


// * * * * * * * * * * * * 
//  * present IRB information
//  * * * * * * * * * * * *
// function doIRBInformation() {
// 	
// 	var div1 = document.createElement('h2');
// 	div1.id = "welcomeDiv";
// 	document.body.appendChild(div1);
// 	$('#welcomeDiv')
// 		.append('<p> Welcome! </p>')
// 	
// 	var div2 = document.createElement('div');
// 	div2.id = "irbDiv";
// 	document.body.appendChild(div2);
// 	$('#irbDiv')
// 		.attr('class','ui-widget')
// 		.append('<p> This is an experiment about learning a small part of a new language. It will take about 20 minutes to complete and you will be paid $1.00 for your time. This experiment is part of a series of studies being conducted by Dr. Jennifer Culbertson at the University of Edinburgh, and has been approved by the Linguistics and English Language Ethics Committee. Please <a href="MultiAdj/InformationForm.pdf">click here</a> to download a study information letter (pdf) that provides further information about the study.</p>\
// 		<p> Clicking on the <b> agree </b> button below indicates that:\
// 		<ul>\
// 		<li> you are a native speaker of English, at least 18 years old </li>\
// 		<li> you have read the information letter </li>\
// 		<li> you voluntarily agree to participate, and understand you can stop your participation at any time</li>\
// 		<li> you agree that your anonymous data may be kept permanently in Edinburgh University archives and may used by qualified researchers for teaching and research purposes</li>\
// 		</ul>\
// 		If you do not agree to all of these, please close this window in your browser now. </p>')
// 		.append('<p>This experiment requires you to listen to AUDIO. If your browser does not \
// 		support audio, or you are not in a quiet place, please do not agree to participate in this HIT.</p>')
// 	
// 	$('#irbDiv').append('<button id="acceptBtn">Accept</button>');
// 	$('#acceptBtn').button();
// 	
// 	$('#acceptBtn')
// 		.on('click', function() {
// 			document.body.removeChild(div1);
// 			document.body.removeChild(div2);
// 			// check for debugging, otherwise proceed to intro instructions
// 			if (debug=="train" | debug=="test") {
// 				createLex();
// 			} else if (debug=="demo") { 
// 				collectDemographics();
// 			} else { 
// 				showIntroInstructions(); 
// 			}
// 		});
// }


/* * * * * * * * * * * * * * * * * * *
 * present introductory instructions
 * * * * * * * * * * * * * * * * * * */
function showIntroInstructions() {
	
	var div1 = document.createElement('h2');
	div1.id = "welcomeDiv";
	document.body.appendChild(div1);
	//$('#welcomeDiv').append('<p> Welcome! </p>')
	$('#welcomeDiv').append('<p> สวัสดีครับ </p>')
	
	var div2 = document.createElement('div');
	div2.id = "introDiv";
	document.body.appendChild(div2);
	$('#introDiv')
		.attr('class','ui-widget')
		//.append('<p>In this experiment, you will be learning part of a new language. The language is similar to English, but you will notice some differences.</p>')
		//.append('<p>Your task will be to learn to translate from English into the new language.</p>')
		.append('<p>ในการทดลองนี้ ท่านจะได้เรียนภาษาใหม่ โดยภาษาดังกล่าวจะมีลักษณะคล้ายกับภาษาไทย แต่ท่านจะพบลักษณะต่างบางประการ</p>')
		.append('<p>ท่านจะต้องแปลวลีในภาษาไทยเป็นภาษาใหม่</p>')
		.append('<p></p>')

	//$('#introDiv').append('<button id="introBtn">Continue</button>');
	$('#introDiv').append('<button id="introBtn">ต่อไป</button>');
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
		//.append('<p> Instructions -- please read carefully! </p>')
		.append('<p> คำสั่ง -- กรุณาอ่านอย่างรอบคอบ </p>')

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
	div2.id = "trainInstrDiv";
	document.body.appendChild(div2);
	$('#trainInstrDiv')
		.attr('class','ui-widget')
		//.append('<p>Now you\'ll see a phrase in English, and hear a speaker of the language you\'re learning translate it.</p>')
		//.append('<p>Look at the English phrase, listen to the speaker translate it, and then click on the translation that matches what you heard the speaker say.</p>')
		//.append('<p>It\'s important to pay close attention, so that later on you\'ll be able to translate on your own.</p>')
		.append('<p>ต่อไปนี้ ท่านจะได้อ่านวลีในภาษาไทยและได้ฟังผู้พูดของภาษาใหม่.</p>')
		.append('<p>อ่านวลีในภาษาไทย ฟังผู้พูดแปลวลีดังกล่าว และเลือกคำแปลที่สอดคล้องกับวลีที่ท่านคิดว่าผู้พูดในภาษาใหม่จะแปล</p>')
		.append('<p>สิ่งสำคัญ คือ ท่านจะต้องให้ความสนใจกับขั้นตอนดังกล่าว เนื่องจากท่านจะต้องแปลวลีเหล่านั้นด้วยตนเอง</p>')

	//$('#trainInstrDiv').append('<button id="instrBtn">Begin</button>');
	$('#trainInstrDiv').append('<button id="instrBtn">เริ่ม</button>');
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

/* * * * * * * * * * * 
 * run training trial
 * * * * * * * * * * */
function doTrainTrial() {
	
	// on the first trial, set up the text, sound, and choices
	if (firstTrainTrial) {
		firstTrainTrial = false;
		
		// div to display message for trial text to-be-translated
		var div1 = document.createElement('div');
		div1.id = "translationDiv";
		document.body.appendChild(div1);
		$('#translationDiv')
			.attr('class','ui-widget')
			.css({ 'margin': 'auto', 'text-align': 'center','width':'75%', 'font-size': '16px'})
			//.append('<p id="translate">Phrase to be translated:</p>');
			.append('<p id="translate">วลีที่ต้องแปล</p>');	
		
		// initialize paragraph for text to-be-translated
   		transText = document.createElement('p');
    	transText.style.cssText = 'font-size:45px';
    	transText.textContent = '';
    	document.getElementById("translationDiv").appendChild(transText);

		// audio element
		var audio1 = document.createElement('audio');
		audio1.id = "audio1";
		audio1.removeAttribute('controls');
		div1.appendChild(audio1);

		// div to hold instructions
		var div4 = document.createElement('div');
		div4.id = "instr";
		document.body.appendChild(div4);
		$('#instr')
			.attr('class','ui-widget')
			.css({ 'margin': 'auto', 'text-align': 'center','width':'75%', 'font-size': '16px', 'font-style': 'italic', 'color': 'whitesmoke'})
			//.append('<p id="message">...click on the choice that matches what you heard...</p>');
			.append('<p id="message">......เลือกตัวเลือกที่สอดคล้องกับสิ่งที่ท่านได้ยิน...</p>');
			
		// div to hold choices
		var div3 = document.createElement('div');
		div3.id = "radioDiv";
		document.body.appendChild(div3);
		$('#radioDiv').css({ 'margin': 'auto', 'text-align': 'center','width':'75%'});
		
		// set up four response buttons
		for (var i=1; i<=4; i++) {
			$('#radioDiv').append('<input type="radio" id="radio'+i+'" name="radioDiv"><label for="radio'+i+'" id="label'+i+'">-----</label>');
			$('#label'+i).css({ 'width':'40%','padding-top': '10px', 'padding-bottom': '10px', 'font-size': '20px', 'border': '1px solid #d3d3d3', 'color': '#555555'});
			$('#radio'+i).on('click', function() {
				//this.checked=false;
				$(this).blur();																				// take the "focus" off the button pressed (for next trial)
				if (this.id != "radio"+trainTrials[trainIndx].trialCorrect) {								// if wrong response
					$('input[name=radioDiv]:checked + label').css('background-color',"#e60000");			// turn button red
					setTimeout(function() {
						$('#audio1').attr('src',"");														// clear sound 
						$('input[name=radioDiv]:checked + label').css('background-color',"");				// clear button color
						$('#radioDiv input').removeAttr('checked');											// reset buttons
						$('#radioDiv').buttonset('refresh'); 	
						for (var i=1; i<=4; i++) { $('#radio'+i).button('option', 'label', '-----'); } 		// clear button labels
						$('#instr').css('color',"whitesmoke");												// make instructions invisible
						doTrainTrial();																		// repeat trial
					},1000, this);
				} else {																					// if correct response
					$('input[name=radioDiv]:checked + label').css('background-color',"#39ac39");			// turn button green
					setTimeout(function() {
						trainIndx += 1;																		// advance trial index
						//trainIndx += 10;																	// advance trial fast for debugging	
						if (trainIndx < trainTrials.length) {
							$('#audio1').attr("src","");													// clear sound 
							$('input[name=radioDiv]:checked + label').css('background-color',"");			// clear button color
							$('#radioDiv input').removeAttr('checked');										// reset buttons
							$('#radioDiv').buttonset('refresh'); 
							for (var i=1; i<=4; i++) { $('#radio'+i).button('option', 'label', '-----'); }	// clear button labels
							$('#instr').css('color',"whitesmoke");											// make instructions invisible
							doTrainTrial();																	// do the next trial
						} else {																			// else training is over, clear everything
							document.body.removeChild(div1);
							document.body.removeChild(div3);
							document.body.removeChild(div4);
							doTestInstructions();
						}
					},1000);
				}
			});
		}
		$("#radioDiv").buttonset();
	}	// ok, now that everything is set up...
	
	// present text, sound, choices for this trial
 	var trial = trainTrials[trainIndx];																	// get the trial variables
    transText.textContent = trial.trialNounThai + trial.trialModThai; 							// add text to-be-translated
    //transText.textContent = trial.trialNounThai + ' ' + trial.trialModThai + '\n' + trial.trialNoun + ' ' + trial.trialMod; 							// add text to-be-translated WITH ENGLISH FOR DEBUGGING
    document.getElementById("translationDiv").appendChild(transText);
	audioName = trial.trialMod+trial.trialNoun+AUDIOAFFIX												// set sound for trial
	c1=trial.trialChoice1Thai;																		// set choices to display
	c2=trial.trialChoice2Thai;
	//c1=trial.trialChoice1Thai + '\n' + trial.trialChoice1;												// set choices to display WITH ENGLISH FOR DEBUGGING
	//c2=trial.trialChoice2Thai + '\n' + trial.trialChoice2;
	
	$('#audio1')
		.attr('src', "U20Thai/sounds/"+audioName)														// set sound, then after it plays, display the choices
		.bind('ended', function() {
			setTimeout(function() {
				
				$('#radio1').button('option', 'label', c1);
				$('#radio2').button('option', 'label', c2);
				$('#radio3').button('option', 'label', '-----');
				$('#radio4').button('option', 'label', '-----');
				$('#instr').css('color',"black");
				//$("#message").text('\xA0 \xA0 \xA0 \xA0...click on the choice that matches what you heard...\xA0 \xA0 \xA0('+(trainIndx+1)+'/'+(trainTrials.length)+')');
				$("#message").text('\xA0 \xA0 \xA0 \xA0......เลือกตัวเลือกที่สอดคล้องกับสิ่งที่ท่านได้ยิน...\xA0 \xA0 \xA0('+(trainIndx+1)+'/'+(trainTrials.length)+')');
			}, 150);
		});

	setTimeout(function() {
		$('#audio1')[0].play();
	}, 1000);
}
