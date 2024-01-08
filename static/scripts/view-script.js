function getCurrentTime() {
  var date = new Date();
  // var utcDate = new Date(date.toUTCString());
  // utcDate.setHours(utcDate.getHours() - 8);
  // var usDate = new Date(utcDate);
  // Format the current time as "YYYY-MM-DDTHH:mm:ss" (e.g., "2023-01-01T12:00:00")
  var formattedTime = date.toISOString().slice(0, 19).replace("T", " ");
  // var formattedTime = formattedTime.toLocaleString("en-US", {
  //   timeZone: "America/Los_Angeles"
  // })
  return formattedTime;
}

function updateTextForElements(className) {
  // Get all elements with the specified class
  var elements = document.getElementsByClassName(className);

  // Iterate over the elements and update the text for each one
  for (var i = 0; i < elements.length; i++) {
    var element = elements[i];

    // Get the set time from the data-set-time attribute
    var setTime = element.getAttribute("data-set-time");

    // Convert current time and setTime to Date
    var currentTimeDate = new Date(getCurrentTime());
    var setTimeDate = new Date(setTime);

    // Calculate the time difference in milliseconds
    var timeDifference = currentTimeDate - setTimeDate;

    // Convert milliseconds to minutes, hours, or days
    var minutesAgo = Math.floor(timeDifference / (1000 * 60));
    var hoursAgo = Math.floor(timeDifference / (1000 * 60 * 60));
    var daysAgo = Math.floor(timeDifference / (1000 * 60 * 60 * 24));

    // Update the text inside the current element based on its time difference
    if (minutesAgo < 60) {
      element.innerText = "Last Modified: " + minutesAgo + " mins ago";
    } else if (hoursAgo < 24) {
      element.innerText = "Last Modified: " + hoursAgo + " hrs ago";
    } else {
      element.innerText = "Last Modified: " + daysAgo + " days ago";
    }
  }
}

// Call the updateTextForElements function with the class
window.onload = updateTextForElements("card-time");
console.log(getCurrentTime())