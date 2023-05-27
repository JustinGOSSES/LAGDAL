console.log("hello")

function fetchData() {
    const data = {
      latitude: 55.012,
      longitude: -109.023
    };
    console.log("sending data over of :",data)
    fetch('/fieldStopIntro', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => {
         console.log(response); // Log the response object
         //console.log(response.text()); // Log the response object
        return response.json();
        })
      .then(result => {
        console.log(result); // Handle the response data here
        // Create a new paragraph element
        const paragraph = document.createElement('p');
        
        // Set the content of the paragraph to the received data
        paragraph.textContent = JSON.stringify(result);
        
        // Get the div element with the ID of dataHolder
        const dataHolder = document.getElementById('dataHolder');
        
        // Append the paragraph element to the dataHolder div
        dataHolder.appendChild(paragraph);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  fetchData() 

//   fetch('/hello', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify(data)
//   })
//     .then(response => {
//       console.log(response); // Log the response object
//       return response.json();
//     })
//     .then(result => {
//       console.log(result); // Handle the response data here
//     })
//     .catch(error => {
//       console.error('Error:', error);
//     });