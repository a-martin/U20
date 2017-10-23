function createLex() {
	$.ajax({
		url : "U20Thai/ThaiU20VocabForJS.csv",
		dataType : "text",
		cache : false,
		success : function(text, status, jqXHR) {
			// add train trials from file after http request
			var vocabArray = text.split("\n");
			for (var i=1; i<vocabArray.length; i++) {	//skip header row
				var vocab_i = vocabArray[i].split(",");
				var vocab = {english:vocab_i[0], thai:vocab_i[1],syncat:vocab_i[3]};
				vocabList.push(vocab);
			}
			shuffleArray(vocabList);
			getCatLists(vocabList)
		},
		error : function(x, text, error) {
			alert(error);
		}
	});
}

function getCatLists(dict) {
	for(var i=0; i<dict.length; i++){
 		var v = dict[i];
 		if (v.syncat=="noun") { 	
    		nouns.push(v.english);
  		}
  		if (v.syncat=="adj") { 	
    		adj.push(v.english);
  		}
  		if (v.syncat=="num") { 	
    		num.push(v.english);
  		}
  		if (v.syncat=="dem") { 	
    		dem.push(v.english);
  		}
	}
	createLists(condition)
}
	
function createLists(condition) {
	/* * * * * * * * * * * * * 
 	* NOUNS
 	* * * * * * * * * * * * */
	shuffle(nouns)
	// Train = 30 trials total
	// pick 20 for training, pick 10 of those to repeat twice
	Nset = nouns.slice(0,20)
	trainNoun = Nset.concat(Nset.slice(0,10))
	// Test = 50 trials total (mix of all nouns)
	shuffle(nouns)
	testNoun = nouns.concat(nouns.slice(0,20))

	/* * * * * * * * * * * * * 
	* MODIFIERS
	* * * * * * * * * * * * */
	// Train = 30 trials total, 15 trials for each of two mod types
	// pick 5 adj or num to repeat 3x, pick all dem, repeat 3 or 4x
	// Test = 20 single mod, 30 two mod
	var trainInner = []
	var trainOuter = []
	var testInner = []
	var testOuter = []
	var testInnerOuter = []

	if (condition=="AdjDem") {
		inner = adj; outer = dem
		shuffle(inner); shuffle(outer); 
	
		inSet = inner.slice(0,5)
		trainInner = inSet.concat(inSet.concat(inSet)) //15 adj
		testInner = inner //10 adj
	
		trainOuter = outer.concat(outer.concat(outer).concat(outer).concat(outer.slice(0,3))) //15 dem
		testOuter = outer.concat(outer.concat(outer.slice(0,2))) //10 dem
			
		testInnerOuter = []
		for (var i=0; i<dem.length; i++) {
			for (var j=0; j<adj.length; j++) {
				testInnerOuter = testInnerOuter.concat(adj[j] + ' ' + dem[i]) // inner first, then outer
			}
		}; shuffle(testInnerOuter)
		testInnerOuter = testInnerOuter.slice(0,30)
	}
	if (condition=="AdjNum") {
		inner = adj; outer = num
		shuffle(inner); shuffle(outer); 
	
		inSet = inner.slice(0,5)
		trainInner = inSet.concat(inSet).concat(inSet) //15 adj
		testInner = inner //10 adj
	
		outSet = outer.slice(0,5)
		trainOuter = outSet.concat(outSet.concat(outSet)) //15 num
		testOuter = outer //10 num
	
		testInnerOuter = []
		for (var i=0; i<num.length; i++) {
			for (var j=0; j<adj.length; j++) {
				testInnerOuter = testInnerOuter.concat(adj[j] + ' ' + num[i]) // inner first, then outer
			}
		}; shuffle(testInnerOuter)
		testInnerOuter = testInnerOuter.slice(0,30)
	}
	if (condition=="NumDem") {
		inner = num; outer = dem
		shuffle(inner); shuffle(outer); 
	
		inSet = inner.slice(0,5)
		trainInner = inSet.concat(inSet.concat(inSet)) //15 num
		testInner = inner //10 num
	
		trainOuter = outer.concat(outer.concat(outer).concat(outer).concat(outer.slice(0,3))) //15 dem
		testOuter = outer.concat(outer.concat(outer.slice(0,2))) //10 dem
	
		testInnerOuter = []
		for (var i=0; i<dem.length; i++) {
			for (var j=0; j<num.length; j++) {
				testInnerOuter = testInnerOuter.concat(num[j] + ' ' + dem[i]) // inner first, then outer
			}
		}; shuffle(testInnerOuter)
		testInnerOuter = testInnerOuter.slice(0,30)
	}

	// put the trials together, and set trial type
	trainMod = trainInner.concat(trainOuter)
	trainType = fillArray("inner",15).concat(fillArray("outer",15))
	testMod = testInner.concat(testOuter).concat(testInnerOuter)
	testType = fillArray("inner",10).concat(fillArray("outer",10)).concat(fillArray("inner-outer",30))
	/* * * * * * * * * * * * * 
	* SET CHOICES TRAIN
	* * * * * * * * * * * * */
	// train choice is either 1 or 2
	trainCorrect = []
	for (i=0; i<trainNoun.length/2;i++) {
		trainCorrect = trainCorrect.concat(1).concat(2)
	}; shuffle(trainCorrect)

	trainChoice1 = []; trainChoice2= []
	for (i=0; i<trainCorrect.length;i++) {
	  if (trainCorrect[i]==1) {
			trainChoice2 = trainChoice2.concat(trainNoun[i].concat(' ').concat(trainMod[i])) // post-nominal (wrong)
			trainChoice1 = trainChoice1.concat(trainMod[i].concat(' ').concat(trainNoun[i])) // pre-nominal (correct)
		}
		if (trainCorrect[i]==2) {
			trainChoice2 = trainChoice2.concat(trainMod[i].concat(' ').concat(trainNoun[i])) // pre-nominal (correct)
			trainChoice1 = trainChoice1.concat(trainNoun[i].concat(' ').concat(trainMod[i])) // post-nominal (wrong)
		}
	}
	
	/* * * * * * * * * * * * * 
	* SET CHOICES TEST
	* * * * * * * * * * * * */
	// for multiple modifier trials, each type of response is assigned a number: 1, 2, 3, 4
	// for a given trial, there is some order of those response types mapped to the buttons, given by permutations of 1, 2, 3, 4
	multiChoiceNum = permutator([1,2,3,4]).concat(permutator([1,2,3,4])).concat(permutator([1,2,3,4]))
	shuffle(multiChoiceNum); multiChoiceNum = multiChoiceNum.slice(0,50) // need 50 total

	// for single mod trials, choice is either 1 or 2 (need 20 of these)
	singleCorrect = []
	for (i=0; i<20/2;i++) {
		singleCorrect = singleCorrect.concat(1).concat(2)
	}; shuffle(singleCorrect);

	singleTestChoice1 = []; singleTestChoice2= []
	for (i=0; i<singleCorrect.length;i++) {
	  if (singleCorrect[i]==1) {
			singleTestChoice2 = singleTestChoice2.concat(testNoun[i].concat(' ').concat(testMod[i])) // post-nominal (wrong)
			singleTestChoice1 = singleTestChoice1.concat(testMod[i].concat(' ').concat(testNoun[i])) // pre-nominal (correct)
		}
		if (singleCorrect[i]==2) {
			singleTestChoice2 = singleTestChoice2.concat(testMod[i].concat(' ').concat(testNoun[i])) // pre-nominal (correct)
			singleTestChoice1 = singleTestChoice1.concat(testNoun[i].concat(' ').concat(testMod[i])) // post-nominal (wrong)
		}
	}

	// for multi (two) mod trials, need to fill in choices based on the order of response types in the buttons
	multiTestChoice = [[],[],[],[]]; multiTestCorrect = []
	multiTestChoiceType = [[],[],[],[]]
	for (i=20; i<multiChoiceNum.length;i++) {	// InnerOuter trials start after 20, 
		inner = testMod[i].split(' ')[0] 		// get inner
		outer = testMod[i].split(' ')[1] 		// get outer
		noun = testNoun[i]						// get noun
		for (j=0; j<multiChoiceNum[0].length;j++) {
			if (multiChoiceNum[i][j]==1) {	//  1, then "correct" pre, isomorphic choice, i.e., Outer-Inner-N
				multiTestChoice[j] = multiTestChoice[j].concat(outer.concat(' ').concat(inner).concat(' ').concat(noun))
				multiTestChoiceType[j] = multiTestChoiceType[j].concat("Outer-Inner-N")
				multiTestCorrect=multiTestCorrect.concat(j+1) // set this one as the correct choice
			}
			if (multiChoiceNum[i][j]==2) {	// if response type is 2, then pre, non-isomorphic choice, i.e., Inner-Outer-N
				multiTestChoice[j] = multiTestChoice[j].concat(inner.concat(' ').concat(outer).concat(' ').concat(noun))
				multiTestChoiceType[j] = multiTestChoiceType[j].concat("Inner-Outer-N")
			}
			if (multiChoiceNum[i][j]==3) {	// if response type is 3, then Thai post, isomorphic choice, i.e., N-Inner-Outer
				multiTestChoice[j] = multiTestChoice[j].concat(noun.concat(' ').concat(inner).concat(' ').concat(outer))
				multiTestChoiceType[j] = multiTestChoiceType[j].concat("N-Inner-Outer")
			}
			if (multiChoiceNum[i][j]==4) {	// if response type is 3, then post, non-isomorphic choice, i.e., N-Outer-Inner
				multiTestChoice[j] = multiTestChoice[j].concat(noun.concat(' ').concat(outer).concat(' ').concat(inner))
				multiTestChoiceType[j] = multiTestChoiceType[j].concat("N-Outer-Inner")
			}
		}
	}
	testCorrect = singleCorrect.concat(multiTestCorrect)
	testChoice1 = singleTestChoice1.concat(multiTestChoice[0])
	testChoice2 = singleTestChoice2.concat(multiTestChoice[1])
	testChoice3 = fillArray('----',20).concat(multiTestChoice[2])
	testChoice4 = fillArray('----',20).concat(multiTestChoice[3])
	testChoiceType1 = fillArray('NA',20).concat(multiTestChoiceType[0])
	testChoiceType2 = fillArray('NA',20).concat(multiTestChoiceType[1])
	testChoiceType3 = fillArray('NA',20).concat(multiTestChoiceType[2])
	testChoiceType4 = fillArray('NA',20).concat(multiTestChoiceType[3])


	/* * * * * * * * * * * * * 
	* COMBINE AND RETURN
	* * * * * * * * * * * * */
	for (var i=0; i<trainNoun.length; i++) {
		var trial = {trialType:trainType[i], trialNoun:trainNoun[i], trialNounThai:findThai(vocabList,trainNoun[i]), trialMod:trainMod[i], trialModThai:findThai(vocabList,trainMod[i]), trialCorrect:trainCorrect[i], trialChoice1:trainChoice1[i], trialChoice1Thai:findThai(vocabList,trainChoice1[i]), trialChoice2:trainChoice2[i], trialChoice2Thai:findThai(vocabList,trainChoice2[i]), trialChoice3:'----', trialChoice4:'----'};
		trainTrials.push(trial);
	}; shuffle(trainTrials)
 
	for (var i=0; i<testCorrect.length; i++) {
		old_noun = trainNoun.includes(testNoun[i])
		if (testType[i] == "inner-outer") {
			mods = testMod[i].split(' ')
			old_mod1 = trainMod.includes(mods[0])
			old_mod2 = trainMod.includes(mods[1])
		}
		else { 
			old_mod1 = trainMod.includes(testMod[i])
			old_mod2 = "NA"
		}
		var trial = {trialType:testType[i], trialNoun:testNoun[i], trialNounThai:findThai(vocabList,testNoun[i]), trialMod:testMod[i], trialModThai:findThai(vocabList,testMod[i]), trialCorrect:testCorrect[i], trialChoice1:testChoice1[i], trialChoice1Thai:findThai(vocabList,testChoice1[i]), trialChoice2:testChoice2[i], trialChoice2Thai:findThai(vocabList,testChoice2[i]), trialChoice3:testChoice3[i], trialChoice3Thai:findThai(vocabList,testChoice3[i]), trialChoice4:testChoice4[i], trialChoice4Thai:findThai(vocabList,testChoice4[i]), trialChoiceType1:testChoiceType1[i], trialChoiceType2:testChoiceType2[i], trialChoiceType3:testChoiceType3[i], trialChoiceType4:testChoiceType4[i], trialOldNoun:old_noun, trialOldMod1: old_mod1, trialOldMod2: old_mod2};
		testTrials.push(trial);
	}; shuffle(testTrials)
	
	// check for debugging, otherwise proceed to training instructions
	if (debug=="train") {
		doTrainTrial();
	} else if (debug=="test") { 
		doTestTrial();
	} else { 
		showTrainInstructions(); 
	}
}
	
/* * * * * * * * * * * * * 
 * HELPER FUNCTIONS
 * * * * * * * * * * * * */
function shuffle(array) {
 	var currentIndex = array.length, temporaryValue, randomIndex;

  	// While there remain elements to shuffle...
  	while (0 !== currentIndex) {

    	// Pick a remaining element...
    	randomIndex = Math.floor(Math.random() * currentIndex);
    	currentIndex -= 1;

    	// And swap it with the current element.
    	temporaryValue = array[currentIndex];
    	array[currentIndex] = array[randomIndex];
    	array[randomIndex] = temporaryValue;
  	}

  return array;
}
	
function permutator(inputArr) {
	var results = [];
	function permute(arr, memo) {
		var cur, memo = memo || [];
		for (var i = 0; i < arr.length; i++) {
			cur = arr.splice(i, 1);
			if (arr.length === 0) {
				results.push(memo.concat(cur));
			}
			permute(arr.slice(), memo.concat(cur));
			arr.splice(i, 0, cur[0]);
		}
		return results;
	}
	return permute(inputArr);
}
	
function fillArray(value, len) {
  	var arr = [];
  	for (var i = 0; i < len; i++) {
		arr.push(value);
  	}
  	return arr;
}

function findThai(dict,string) {
	if (string == '----') { 
		thai = '----'
	}
	else {
		words = string.split(' ')
		thai = [];
		for (var w=0; w<words.length; w++){
 			for (var i=0; i<dict.length; i++){
 				var v = dict[i];
 				if (v.english==words[w]) { 	
    				thai.push(v.thai);
  				}
  			}
  		}
  		thai = thai.join('');
  	}
  	return thai;
}
