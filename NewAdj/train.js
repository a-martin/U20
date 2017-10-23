
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
			.append('<p id="translate">Phrase to be translated:</p>');
		
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
			.append('<p id="message">...click on the choice that matches what you heard...</p>');
			
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
						var trialDataToRecord = {'phase':'training','trial':trainIndx,'type':trainTrials[trainIndx].trialType,'correctChoice':trainTrials[trainIndx].trialCorrect,'response':trainTrials[trainIndx].trialCorrect,'mod':trainTrials[trainIndx].trialMod,'noun':trainTrials[trainIndx].trialNoun};
						dataAccumulator.push(trialDataToRecord)
						writeDataToBlake(trialDataToRecord);
						
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
 	var trial = trainTrials[trainIndx];											// get the trial variables
    transText.textContent = trial.trialMod + ' ' + trial.trialNoun; 			// add text to-be-translated
    document.getElementById("translationDiv").appendChild(transText);
	audioName = trial.trialNoun+trial.trialMod+AUDIOAFFIX						// set sound for trial
	c1=trial.trialChoice1;														// set choices to display
	c2=trial.trialChoice2;

	$('#audio1')
		.attr('src', "U20NewAdj/sounds/"+audioName)					// set sound, then after it plays, display the choices
		.bind('ended', function() {
			setTimeout(function() {
				
				$('#radio1').button('option', 'label', c1);
				$('#radio2').button('option', 'label', c2);
				$('#radio3').button('option', 'label', '-----');
				$('#radio4').button('option', 'label', '-----');
				$('#instr').css('color',"black");
				$("#message").text('\xA0 \xA0 \xA0 \xA0...click on the choice that matches what you heard...\xA0 \xA0 \xA0('+(trainIndx+1)+'/'+(trainTrials.length)+')');
			}, 150);
		});

	setTimeout(function() {
		$('#audio1')[0].play();
	}, 1000);
}
