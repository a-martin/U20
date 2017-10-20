function createLex() {
	$.ajax({
		url : "U20NewAdj/all_vocab.csv",
		dataType : "text",
		cache : false,
		success : function(text, status, jqXHR) {
			// add train trials from file after http request
			var vocabArray = text.split("\n");
			for (var i=1; i<vocabArray.length; i++) {	//skip header row
				var vocab_i = vocabArray[i].split(",");
				var vocab = {word:vocab_i[0], syncat:vocab_i[1]};
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
    		nouns.push(v.word);
  		}
  		if (v.syncat=="adj_inner") { 	
    		adj_inner.push(v.word);
  		}
  		if (v.syncat=="adj_outer") { 	
    		adj_outer.push(v.word);
  		}
  		if (v.syncat=="adj_original") { 	
    		adj_original.push(v.word);
  		}
  		if (v.syncat=="num") { 	
    		num.push(v.word);
  		}
	}
	createLists(condition)
}
	
function createLists(condition) {
	/* * * * * * * * * * * * * 
	* SET TRAIN & TEST PHRASES
	* * * * * * * * * * * * */
	
	/* * * * 
	* MODS
	* * * * */
	var inner = []
	var outer = []
	var trainInner = []
	var trainOuter = []
	var testInner = []
	var testOuter = []
	var testOuterInner = []
	
	/* * * * * * * * * * * * */ 
	// During training: 30 trials total, 15 trials for each of two mod types
	// therefore: pick 5 of each modifier to repeat 3x
	// During testing: 20 single mod, 30 two mod
	// therefore: use all modifiers of each type (there are 8 of each) and repeat a random subset once
	/* * * * * * * * * * * * */ 
	
	// Set inner and outer modifiers based on condition
	if (condition=="AdjAdj") { inner = adj_inner; outer = adj_outer } 
	if (condition=="AdjOrigNum") { inner = adj_original; outer = num.slice(0,8) }
	if (condition=="AdjInnerNum") { inner = adj_inner; outer = num.slice(0,8) }
	if (condition=="AdjOuterNum") { inner = adj_outer; outer = num.slice(0,8) }
	//shuffle them
	shuffle(inner); shuffle(outer);
	
	// If it's the original set, need to pick 8 from the original 10 to matched reduced size of the new sets
	if (condition=="AdjOrigNum") { inner = inner.slice(0,8) }
	
	// Pick the inner training and testing set	
	inSet = inner.slice(0,5) // pick 5
	trainInner = inSet.concat(inSet.concat(inSet)) // rep 3x for 15 total
	testInner = inner.concat(inner.slice(0,2)) // all 8 plus 2 repeats = 10 total
	
	// Pick the outer training and testing set	
	outSet = outer.slice(0,5) // pick 5
	trainOuter = outSet.concat(outSet.concat(outSet)) // rep 3x for 15 total
	testOuter = outer.concat(inner.slice(0,2)) // all 8 plus 2 repeats = 10 total
	
	// Set the testing combinations, and shuffle them 	
	for (var i=0; i<outer.length; i++) {
		for (var j=0; j<inner.length; j++) {
			testOuterInner = testOuterInner.concat(outer[j] + ' ' + inner[i]) // outer first, then inner, since will display in English order
		}
	}; shuffle(testOuterInner)
	testOuterInner = testOuterInner.slice(0,30)
	
	// put the trials together, and set trial type
	trainMod = trainInner.concat(trainOuter)
	trainType = fillArray("inner",15).concat(fillArray("outer",15))
	testMod = testInner.concat(testOuter).concat(testOuterInner)
	testType = fillArray("inner",10).concat(fillArray("outer",10)).concat(fillArray("inner-outer",30))
	
	/* * * * 
	* NOUNS
	* * * * */
	// During train: 30 trials total
	// therefore: pick 20 for training (there are 30 total), pick 10 of those to repeat twice
	// During test: 50 trials total
	// therefore: take all 30, and then pick 20 randomly to repeat once
	shuffle(nouns)
	Nset = nouns.slice(0,20) // pick 20
	trainSet = Nset.concat(Nset.slice(0,10)) // 20+10 repeated, nouns with uncorrected number
	shuffle(nouns)
	testSet = nouns.concat(nouns.slice(0,20)) // 30+20 repeated, nouns with uncorrected number

	// now correct the number agreement
	trainNoun = []; testNoun = [];
	for (var i=0; i<trainSet.length; i++) {
		trainNoun.push(setNumber(trainMod[i],trainSet[i]))
	}
	for (var i=0; i<testSet.length; i++) {
		testNoun.push(setNumber(testMod[i],testSet[i]))
	}

	/* * * * * * * * * * * * * 
	* SET TRAIN CHOICES
	* * * * * * * * * * * * */
	// train choice is either 1 or 2
	trainCorrect = []
	for (i=0; i<trainNoun.length/2;i++) {
		trainCorrect = trainCorrect.concat(1).concat(2)
	}; shuffle(trainCorrect)

	trainChoice1 = []; trainChoice2= []
	for (i=0; i<trainCorrect.length;i++) { 
	  if (trainCorrect[i]==1) {
			trainChoice2 = trainChoice2.concat(trainMod[i].concat(' ').concat(trainNoun[i])) // pre-nominal (wrong)
			trainChoice1 = trainChoice1.concat(trainNoun[i].concat(' ').concat(trainMod[i])) // post-nominal (correct)
		}
		if (trainCorrect[i]==2) {
			trainChoice2 = trainChoice2.concat(trainNoun[i].concat(' ').concat(trainMod[i])) // post-nominal (correct)
			trainChoice1 = trainChoice1.concat(trainMod[i].concat(' ').concat(trainNoun[i])) // pre-nominal (wrong)
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
			singleTestChoice2 = singleTestChoice2.concat(testMod[i].concat(' ').concat(testNoun[i])) // pre-nominal (wrong)
			singleTestChoice1 = singleTestChoice1.concat(testNoun[i].concat(' ').concat(testMod[i])) // post-nominal (correct)
		}
		if (singleCorrect[i]==2) {
			singleTestChoice2 = singleTestChoice2.concat(testNoun[i].concat(' ').concat(testMod[i])) // post-nominal (correct)
			singleTestChoice1 = singleTestChoice1.concat(testMod[i].concat(' ').concat(testNoun[i])) // pre-nominal (wrong)
		}
	}

	// for multi (two) mod trials, need to fill in choices based on the order of response types in the buttons
	multiTestChoice = [[],[],[],[]]; multiTestCorrect = []
	multiTestChoiceType = [[],[],[],[]]
	for (i=20; i<multiChoiceNum.length;i++) {	// OuterInner trials start after 20, 
		outer = testMod[i].split(' ')[0] 		// get outer
		inner = testMod[i].split(' ')[1] 		// get inner
		noun = testNoun[i]						// get noun
		for (j=0; j<multiChoiceNum[0].length;j++) {
			if (multiChoiceNum[i][j]==1) {	//  1, then "correct" post, isomorphic choice, i.e., N-Inner-Outer
				multiTestChoice[j] = multiTestChoice[j].concat(noun.concat(' ').concat(inner).concat(' ').concat(outer))
				multiTestChoiceType[j] = multiTestChoiceType[j].concat("N-Inner-Outer")
				multiTestCorrect=multiTestCorrect.concat(j+1) // set this one as the correct choice
			}
			if (multiChoiceNum[i][j]==2) {	// if response type is 2, then post, non-isomorphic choice, i.e., N-Outer-Inner
				multiTestChoice[j] = multiTestChoice[j].concat(noun.concat(' ').concat(outer).concat(' ').concat(inner))
				multiTestChoiceType[j] = multiTestChoiceType[j].concat("N-Outer-Inner")
			}
			if (multiChoiceNum[i][j]==3) {	// if response type is 3, then English pre, isomorphic choice, i.e., Outer-Inner-N
				multiTestChoice[j] = multiTestChoice[j].concat(outer.concat(' ').concat(inner).concat(' ').concat(noun))
				multiTestChoiceType[j] = multiTestChoiceType[j].concat("Outer-Inner-N")
			}
			if (multiChoiceNum[i][j]==4) {	// if response type is 3, then pre, non-isomorphic choice, i.e., Inner-Outer-N
				multiTestChoice[j] = multiTestChoice[j].concat(inner.concat(' ').concat(outer).concat(' ').concat(noun))
				multiTestChoiceType[j] = multiTestChoiceType[j].concat("Inner-Outer-N")
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
		var trial = {trialType:trainType[i], trialNoun:trainNoun[i], trialMod:trainMod[i], trialCorrect:trainCorrect[i], trialChoice1:trainChoice1[i], trialChoice2:trainChoice2[i], trialChoice3:'----', trialChoice4:'----'};
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
		var trial = {trialType:testType[i], trialNoun:testNoun[i], trialMod:testMod[i], trialCorrect:testCorrect[i], trialChoice1:testChoice1[i], trialChoice2:testChoice2[i], trialChoice3:testChoice3[i], trialChoice4:testChoice4[i], trialChoiceType1:testChoiceType1[i], trialChoiceType2:testChoiceType2[i], trialChoiceType3:testChoiceType3[i], trialChoiceType4:testChoiceType4[i], trialOldNoun:old_noun, trialOldMod1: old_mod1, trialOldMod2: old_mod2};
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

var pl_nums = ["two","three","four","five","six","seven","eight","nine","ten"];
function setNumber(mods,noun) {
	noun_set = "";
	if (mods.indexOf(' ') >= 0) { 											// when there are two modifiers
		if (mods.indexOf('one') >= 0) { noun_set = noun.split('_')[0] }		// if the number is 'one' then get the singular
		else { noun_set = noun.split('_')[1] }								// otherwise they are all plural
	}
	else {																	// when there is only one modifier
		if (pl_nums.indexOf(mods) >= 0) { noun_set = noun.split('_')[1]	}	// if a plural number, then it's plural
		else { noun_set = noun.split('_')[0] }								// if it's anything else, it's singular
	}
  	return noun_set;
}
