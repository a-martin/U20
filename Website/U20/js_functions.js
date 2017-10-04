function playsound(music) {
   var music = new Audio(music);
   music.play();
 }


function play_pair(sing, plur, dir) {
  var sing = new Audio(dir.concat(sing).concat('.wav'));
  var plur = new Audio(dir.concat(plur).concat('.wav'));
  sing.play();

  setTimeout(function() {
      plur.play();
    }, (1500));
}


function play_triplet(stem, one, two, dir) {
    var stem = new Audio(dir.concat(stem).concat('.wav'));
    var one = new Audio(dir.concat(one).concat('.wav'));
    var two = new Audio(dir.concat(two).concat('.wav'));

    stem.play();

    
    setTimeout(function() {

	one.play();

	setTimeout(function() {
	    two.play();
	}, (1500))

    }, (2000));
}
