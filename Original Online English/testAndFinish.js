/* Replication of Culbertson & Adger U20 experiment -- POV design
 * Manipulating the type of adjective based on pmi calculation on the Brown corpus
 * - experiment starts with beginAndTrain, then passed here
 * - present testing instructions
 * - do testing trials
 * - pass on to testAndFinish to run testing trials, collect demographic info, collate responses, and submit
 */
 
/* * * * * * * * * * * * * * * * * * *
 * present testing instructions
 * * * * * * * * * * * * * * * * * * */
function doTestInstructions() {
	
	var div1 = document.createElement('h2');
	div1.id = "welcomeDiv";
	document.body.appendChild(div1);
	$('#welcomeDiv')
		.append('<p> Instructions -- please read carefully! </p>')
	
	var div2 = document.createElement('div');
	div2.id = "testInstrDiv";
	document.body.appendChild(div2);
	$('#testInstrDiv')
		.attr('class','ui-widget')
		.append('<p>In the next part of the experiment, you will show what you have learned about this new language.')
		.append('<p>You will see an English phrase -- it may be the SAME LENGTH phrase that you have seen before, or it may be LONGER.')
		.append('<p>Look at the English phrase, and click on the translation that you think a speaker of the language WOULD BE MOST LIKELY TO SAY.')
		.append('<p>Try to do as well as you can, remembering what you learned in the first part of the experiment, but don\'t worry if once in a while you have to guess.')
		
	$('#testInstrDiv').append('<button id="instrBtn">Begin</button>');
	$('#instrBtn').button();
	$('#instrBtn').button("disable");

	setTimeout(function() {
		$('#instrBtn').button("enable");
		$('#instrBtn')
			.on('click', function() {
				document.body.removeChild(div1);
				document.body.removeChild(div2);
				doTestTrial();
			});
	}, 5000);
	//}, 20);	// fast for debugging
}


/* * * * * * * * * * * 
 * run training trial
 * * * * * * * * * * */
function doTestTrial() {
	// on the first trial, set up the text and choices
	if (firstTestTrial) {
		firstTestTrial = false;

		// div to display message for trial text to-be-translated
		var div1 = document.createElement('div');
		div1.id = "translationDiv";
		document.body.appendChild(div1);
		$('#translationDiv')
			.attr('class','ui-widget')
			.css({ 'margin': 'auto', 'text-align': 'center','width':'75%', 'font-size': '16px'})
			.append('<p id="translate">Phrase to be translated:</p>');
		
		// initialize paragraph for text to-be-translated
   		transText = document.createElement('p');
    	transText.style.cssText = 'font-size:45px';
    	transText.textContent = '';
    	document.getElementById("translationDiv").appendChild(transText);

		// div to hold instructions
		var div2 = document.createElement('div');
		div2.id = "instr";
		document.body.appendChild(div2);
		$('#instr')
			.attr('class','ui-widget')
			.css({ 'margin': 'auto', 'text-align': 'center','width':'75%', 'font-size': '16px', 'font-style': 'italic', 'color': 'whitesmoke'})
			.append('<p id="message">...click on the choice that the speaker would most likely say...</p>');

		// div to hold choices
		var div3 = document.createElement('div');
		div3.id = "radioDiv";
		document.body.appendChild(div3);
		$('#radioDiv').css({ 'margin': 'auto', 'text-align': 'center','width':'75%'});

		for (var i=5; i<=8; i++) {
			$('#radioDiv').append('<input type="radio" id="radio'+i+'" name="radioDiv"><label for="radio'+i+'" id="label'+i+'"+" choice='+i+'">-----</label>');
			$('#label'+i).css({ 'width':'40%','padding-top': '10px', 'padding-bottom': '10px', 'font-size': '20px', 'border': '1px solid #d3d3d3', 'color': '#555555'});
			$('#radio'+i).on('click', function() {
				$(this).blur();																			// take the "focus" off the button pressed (for next trial)
				testResponses[testIndx] = this.id														// record response
				var trialDataToRecord = {'phase':'test','trial':testIndx,'type':testTrials[testIndx].trialType,'correctChoice':testTrials[testIndx].trialCorrect,'response':testResponses[testIndx],'mod':testTrials[testIndx].trialMod,'noun':testTrials[testIndx].trialNoun,'choice1':testTrials[testIndx].trialChoice1,'choice2':testTrials[testIndx].trialChoice2,'choice3':testTrials[testIndx].trialChoice3,'choice4':testTrials[testIndx].trialChoice4,'noun_old_new':testTrials[testIndx].trialOldNoun,'mod1_old_new':testTrials[testIndx].trialOldMod1,'mod2_old_new':testTrials[testIndx].trialOldMod2,'choiceType1':testTrials[testIndx].trialChoiceType1,'choiceType2':testTrials[testIndx].trialChoiceType2,'choiceType3':testTrials[testIndx].trialChoiceType3,'choiceType4':testTrials[testIndx].trialChoiceType4};
				dataAccumulator.push(trialDataToRecord)
				writeDataToBlake(trialDataToRecord);
						
				testIndx += 1;																			// advance trial index
				//testIndx += 30;																		// advance fast for debuggin
				setTimeout(function() {																	// wait a moment
					$('#radioDiv input').removeAttr('checked');											// reset buttons
					$('#radioDiv').buttonset('refresh'); 
					for (var i=5; i<=8; i++) { $('#radio'+i).button('option', 'label', '-----'); } 		// clear button labels
					$('#instr').css('color',"whitesmoke");												// make instructions invisible
					setTimeout(function() {
						if (testIndx < testTrials.length) {
							doTestTrial();																// do the next trial
						} else {																		// else testing is over, clear everything
							document.body.removeChild(div1);
							document.body.removeChild(div2);
							document.body.removeChild(div3);
							showEndInstructions();
						}
					},750);
				}, 350);
			});
		}
		$('#radioDiv').buttonset();
	}	// ok, now that everything is set up...
	
	// present text, choices for this trial
	var trial = testTrials[testIndx];												// get the trial variables
	transText.textContent = trial.trialMod + ' ' + trial.trialNoun; 				// add text to-be-translated
    document.getElementById("translationDiv").appendChild(transText);
	//console.log(trial.trialCorrect)
	setTimeout(function() {
		for (var i=5; i<=8; i++) { num=i-4; $('#radio'+i).button('option', 'label', eval('trial.trialChoice' + num)); }		// add choices
		$('#instr').css('color',"black");
		$("#message").text('\xA0 \xA0 \xA0 \xA0...click on the choice that the speaker would most likely say...\xA0 \xA0 \xA0('+(testIndx+1)+'/'+(testTrials.length)+')');
	},500);
}

/* * * * * * * * * * * * * * * * * * *
 * present end instructions
 * * * * * * * * * * * * * * * * * * */
function showEndInstructions() {
	
	var div1 = document.createElement('h2');
	div1.id = "welcomeDiv";
	document.body.appendChild(div1);
	$('#welcomeDiv')
		.append('<p> Thanks! </p>')
	
	var div2 = document.createElement('div');
	div2.id = "introDiv";
	document.body.appendChild(div2);
	$('#introDiv')
		.attr('class','ui-widget')
		.append('<p>You\'re almost finished with this task. Thank you for participating!</p>')
		.append('<p>Please help us by filling out a short questionnaire, after which you\'ll submit the HIT.</p>')
		.append('<p></p>');

	$('#introDiv').append('<button id="introBtn">Continue</button>');
	$('#introBtn').button();
	
	$('#introBtn')
		.on('click', function() {
			document.body.removeChild(div1);
			document.body.removeChild(div2);
			collectDemographics();
		});
}

