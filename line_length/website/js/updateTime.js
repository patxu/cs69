updateTime();
setInterval(updateTime, 2000);
function updateTime(){
  var query = new Parse.Query("Reading");
  query.descending("createdAt");
  query.limit(10);// value * 3 seconds = how far back you're looking
  query.find({
    success: function(results) {
      var index;
      var sum = 0;
      for (index = 0; index < results.length; index++){
        sum = parseFloat(sum) + parseFloat(results[index].get("distance"));
      }
      if (isNaN(sum)){
        document.getElementById("KAF-time").innerHTML = "Not Available";
      }
      else {
        var avg = sum/results.length*0.0328; //cm to feet
        var waitTime = 7.416 * avg + 1.810; //function
        var seconds = Math.floor(waitTime%60);
        var minutes = Math.floor(waitTime/60);
        console.log("length =", avg);
        var zeroPadding = "";
        if (seconds < 10) {
          zeroPadding = "0";
        }
        document.getElementById("KAF-time").innerHTML = minutes+ ":" + zeroPadding + seconds;
      }
    }, error: function(error) {
      console.log(error);
    }
  });
}
