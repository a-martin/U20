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
		.append('<form id="demoForm" action="handle_data.php" method="post">\
		<p>กรุณากรอกข้อมูลของท่านและขั้นตอนในการเลือกตัวเลือก ทีมผู้วิจัยจะเก็บข้อมูลของท่านโดยไม่เปิดเผยและข้อมูลดังกล่าวจะเป็นประโยชน์ต่อการวิเคราะห์ข้อมูลของทีมวิจัย</p>\
		<p><b>เพศ</b><br>\
		<input type="radio" name="gender" id="genderF" value="female"/>หญิง\
		<input type="radio" name="gender" id="genderM" value="male"/>ชาย\
		<input type="radio" name="gender" id="genderO" value="other"/>อื่นๆ\
		<input type="radio" name="gender" id="genderNA" value="NA"/>ไม่ประสงค์ที่จะระบุ</p>\
		<p><b>อายุ</b><br>\
		<input id="age" name="age" size="5"/></p>\
		<p><b>กรุณาชี้แจง</b> ท่านมีขั้นตอนการตัดสินใจในการเลือกตัวเลือกอย่างไร<br>\
		โปรดแสดงความคิดเห็นของท่าน<br>\
		<textarea id="comments" name="comments" rows="10" cols="30"></textarea></p>\
		<input type="submit" value="ส่ง" style="height: 35px; width: 130px; font-size: 18px">\
		</form>');
		
	$('#demoForm')
		.append('<input type="hidden" name="subjID" value="id_'+ subjID +'" />')
		.append('<input type="hidden" name="condition" value="condition_'+ condition +'" />');
	for (var i=0; i<trainTrials.length; i++) {
		var trial_i = trainTrials[i];
		//var trial = {trialType:trainType[i], trialNoun:trainNoun[i], trialMod:trainMod[i], trialCorrect:trainCorrect[i], trialChoice1:trainChoice1[i], trialChoice2:trainChoice2[i], trialChoice3:'----', trialChoice4:'----'};
		var x = 'trainTrial'+ i +'_'+ trial_i.trialType +'_'+ trial_i.trialCorrect +'_'+ trial_i.trialMod +'_'+ trial_i.trialNoun;
		$('#demoForm')
			.append('<input type="hidden" name="trainTrial'+ i +'" value="'+ x +'" />');	
	}
	for (var i=0; i<testTrials.length; i++) {
		var trial_i = testTrials[i];
		//var trial = {trialType:testType[i], trialNoun:testNoun[i], trialNounThai:findThai(vocabList,testNoun[i]), trialMod:testMod[i], trialModThai:findThai(vocabList,testMod[i]), trialCorrect:testCorrect[i], trialChoice1:testChoice1[i], trialChoice1Thai:findThai(vocabList,testChoice1[i]), trialChoice2:testChoice2[i], trialChoice2Thai:findThai(vocabList,testChoice2[i]), trialChoice3:testChoice3[i], trialChoice3Thai:findThai(vocabList,testChoice3[i]), trialChoice4:testChoice4[i], trialChoice4Thai:findThai(vocabList,testChoice4[i]), trialChoiceType1: testChoiceType1[i], trialChoiceType2: testChoiceType2[i], trialChoiceType3: testChoiceType3[i], trialChoiceType4: testChoiceType4[i], trialOldNoun:old_noun, trialOldMod1: old_mod1, trialOldMod2: old_mod2};
		var x = 'testTrial'+ i +'_'+ trial_i.trialType +'_'+ trial_i.trialCorrect +'_'+ trial_i.trialChoice1 +'_'+ trial_i.trialChoice2 +'_'+ trial_i.trialChoice3 +'_'+ trial_i.trialChoice4 +'_'+ testResponses[i] +'_'+ trial_i.trialMod +'_'+ trial_i.trialNoun +'_'+ trial_i.trialOldNoun +'_'+ trial_i.trialOldMod1 +'_'+ trial_i.trialOldMod2 +'_'+ trial_i.trialChoiceType1 +'_'+ trial_i.trialChoiceType2 +'_'+ trial_i.trialChoiceType3 +'_'+ trial_i.trialChoiceType4;
		$('#demoForm')
			.append('<input type="hidden" name="testTrial'+ i +'" value="' + x +'" />');	
	}

	$('#demoForm').submit(function() {
		var data = $("#demoForm").serialize();
		$.ajax({
			type: "POST",
			data: data,
			cache: false,
			//success: function(html) {
			//	alert("Submitted! Thanks!");
			//}
		});
		//return false;	// xxx debugging only
		//return true;
	});
}
