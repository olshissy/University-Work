let bookingData = [,,,,,,,,
	{
  	time: "08:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "09:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "10:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "11:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "12:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "13:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "14:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "15:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "16:00",
    reason: "",
    label: "",
    booked: false
  },{
  	time: "17:00",
    reason: "",
    label: "",
    booked: false
  }
];

//Task 1
function bookRoom(time,reason,label)
{
    for(let i=8; i<bookingData.length; i++)
    {
        if(bookingData[i].time==time)
        {
            bookingData[i].reason = reason;
            bookingData[i].label = label;
            bookingData[i].booked= true;
        }
    }
}

//Task 2
function checkRoomBooked(time)
{
  for (let i=8; i<bookingData.length; i++)
  {
    if (bookingData[i].time == time)
    {
      return (bookingData[i].booked);
    }
  }
}

//Task 3
function clearRoomBookings()
{
  for(let i=8; i<bookingData.length; i++)
  {
    bookingData[i].reason = "";
    bookingData[i].label = "";
    bookingData[i].booked= false;
  }
  updateDisplay();
}

//Task 5
function updateDisplay()
{
  let output = "";
  for(let i=8; i<bookingData.length; i++)
  {
    let roomTime="<p>" + bookingData[i].time;
    if(bookingData[i].booked == false)
    {
      roomTime += ": Available";
    }
    else 
    {
      roomTime += ": Not Available (" + (bookingData[i].label) + ")";
    }
    roomTime += "</p>"
    output += roomTime;
  }
 document.getElementById("output").innerHTML = output;
 
}

//Task 6
function doBooking()
{
  let timeRef = document.getElementById("inputTime").value;
  let reasonRef  = document.getElementById("inputReason").value;
  let labelRef = document.getElementById("inputLabel").value;
  if(reasonRef =="")
  {
    window.alert("Please enter reason");
  }
  if(labelRef =="")
  {
    window.alert("Please enter label");
  }
  if(timeRef =="0")
  {
    window.alert("Please select time");
  }
  if(checkRoomBooked(timeRef)==true)
  {
    window.alert("This time is not available");
  }
  else
  {
    bookRoom(timeRef, reasonRef, labelRef);
    updateDisplay();
  }
}

//Task 7
function clearAllBookings()
{
 if(window.confirm("Are you sure you want to clear all bookings?")==true)
  {
  clearRoomBookings();
  }
}

//Task 8
function updateDayTime()
{
  let timeRef= document.getElementById("timeNow");
  let timeNow= new Date().toLocaleTimeString();
  timeRef.innerText=timeNow;
}

//Task 9
setInterval(updateDayTime,1000);

