//run the function immediately upon page loading
updateTime();

//run the function every 2 seconds
setInterval(updateTime, 2000);

//queries Parse for Reading objects and converts and average of the 10 most 
//recent distance measurements to a wait time estimate
function updateTime(){
  var distanceFromFront = 12;
  var query = new Parse.Query("Reading");
  query.descending("createdAt");
  query.limit(10);
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
        if (avg < 1) { //closer than 1 foot to the sensor
          avg = 0;
          console.log("line past sensor!");
        }
        lineLength = distanceFromFront - avg;
        console.log("line length = ", lineLength);
        var waitTime = 7.416 * lineLength + 1.810; //special function
        if (lineLength == distanceFromFront){
          document.getElementById("KAF-time").innerHTML = "> " + formatTime(waitTime);
        }
        else{
          document.getElementById("KAF-time").innerHTML = formatTime(waitTime);
        }

        //console.log(results[results.length-1].get("distance"));
        var createdAt = results[0].createdAt;
        var zeroPadding = "";
        if (createdAt.getMinutes() <10){
          zeroPadding = "0";
        }
        var updated = "Last Updated: " + 
          (createdAt.getMonth()+1) + "/" + 
          createdAt.getDate() + "/" + 
          createdAt.getFullYear() + " at " + 
          createdAt.getHours() + ":" + 
          zeroPadding + 
          createdAt.getMinutes();
        document.getElementById("last-updated").innerHTML = updated;
      }
    }, error: function(error) {
      console.log(error);
    }
  });
}

//change a time in seconds to a nicer format
function formatTime(time){
  var string = "";
  var minutes = Math.floor(time/60); //rounding + truncate
  console.log("time is " + time);
  if (minutes > 0){
    if (minutes == 1) {
      string = minutes + " minute"
    }
    else {
      string = minutes + " minutes"
    }
  }
  var seconds = Math.floor(time%60);
  if (seconds > 0){
    if (minutes > 0){
      string += " ";
    }
    if (seconds == 1) {
      string += seconds + " second"
    }
    else {
      string += seconds + " seconds"
    }
  }
  return string;
}
