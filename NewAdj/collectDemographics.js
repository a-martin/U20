/*
 * Collect demographic information and post demographic info and trial results to MTurk
 */
function collectDemographics() {
	var demoDiv = document.createElement('div');
	demoDiv.id = "demoDiv";
	document.body.appendChild(demoDiv);
	$('#demoDiv')
		.attr('style',"margin-left:45px")
		.css('font-size',"20px")
		//.append('<form id="demoForm" action="U20NewAdj/handle_data.php" method="post">\
		//.append('<form id="demoForm" action="https://www.mturk.com/mturk/externalSubmit" method="POST">\
		.append('<form id="demoForm" action="https://workersandbox.mturk.com/mturk/externalSubmit" method="POST">\
		<p>Please provide us with some information about you and how you did the experiment. We will keep this information private (it will not be associated with your worker id), and it will help us very much when we analyze the data.</p>\
		<p><b>Gender</b><br>\
		<input type="radio" name="gender" id="genderF" value="female"/>female\
		<input type="radio" name="gender" id="genderM" value="male"/>male\
		<input type="radio" name="gender" id="genderO" value="other"/>other\
		<input type="radio" name="gender" id="genderNA" value="NA"/>prefer not to say</p>\
		<p><b>Age</b><br>\
		<input id="age" name="age" size="5"/></p>\
		<p><b>Language background</b><br>\
		<input id="langNative" name="langNative" size="20"/> Native language(s)<br>\
		<input id="langOther" name="langOther" size="20"/> Other language experience (indicate if fluent)\
		<p><b>Tell us:</b> How did you decide which translation to choose?<br>\
		Include any other comments you have as well.<br>\
		<textarea id="comments" name="comments" rows="10" cols="30"></textarea></p>\
		<input type="submit" value="Submit HIT" style="height: 35px; width: 130px; font-size: 18px">\
		</form>');
	
	
	$('#demoForm')
		.append('<input type="hidden" name="assignmentId" value="'+ assignId +'" />')
		.append('<input type="hidden" name="hitId" value="'+ hitId +'" />')
		.append('<input type="hidden" name="workerId" value="'+ workerId +'" />')
		.append('<input type="hidden" name="condition" value="condition_'+ condition +'" />')
	for (var i=0; i<dataAccumulator.length; i++) {
		var trial_i = dataAccumulator[i]
		if (trial_i.phase=="training") {
			var trialData = [trial_i.phase,trial_i.trial,trial_i.type,trial_i.correctChoice,trial_i.mod,trial_i.noun,'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'];
			$('#demoForm')
				.append('<input type="hidden" name="trainTrial'+ i +'" value="'+ trialData +'" />');	
		}
		else {
 			var trialData = [trial_i.phase,trial_i.trial,trial_i.type,trial_i.correctChoice,trial_i.response,trial_i.mod,trial_i.noun,trial_i.choice1,trial_i.choice2,trial_i.choice3,trial_i.choice4,trial_i.noun_old_new,trial_i.mod1_old_new,trial_i.mod2_old_new,trial_i.choiceType1,trial_i.choiceType2,trial_i.choiceType3,trial_i.choiceType4];
			$('#demoForm')
				.append('<input type="hidden" name="trainTrial'+ i +'" value="'+ trialData +'" />');	
 		} 
	}

	$('#demoForm').submit(function() {
		//return false;	// xxx debugging only
		return true;
	});
	
	
	// This function is for sending data directly to blake
// 	$('#demoForm').submit(function() {
// 		var data = $("#demoForm").serialize();
// 		//var data = trainTrials[0].serialize();
// 		$.ajax({
// 			type: "POST",
// 			data: data,
// 			cache: false,
// 			success: function(html) {
// 				alert("Submitted! Thanks!");
// 			}
// 		});
//  	});
// 	

}
