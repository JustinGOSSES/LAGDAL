        latitude = 35.442911
        longitude = -105.585828
        var map = L.map('map').setView([latitude, longitude], 5);

        var openstreet = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
            tileSize: 512,
            zoomOffset: -1
        }).addTo(map);

        var macrostratMap = L.map('macrostrat-map').setView([latitude, longitude], 5);

        L.tileLayer('https://tiles.macrostrat.org/carto/{z}/{x}/{y}.png', {
            attribution: '<a href="https://macrostrat.org/">Macrostrat</a>',
            maxZoom: 18,
            tileSize: 512,
            zoomOffset: -1
        }).addTo(macrostratMap);

    
        
         // Add a street map overlay
      var streetsLight = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
            tileSize: 512,
            zoomOffset: -1,
            opacity: 0.25,
        attribution: 'Street Map &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      });
      var streetsBold = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
            tileSize: 512,
            zoomOffset: -1,
            opacity: 0.65,
        attribution: 'Street Map &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      });

      var overlayMaps = {
        "StreetsLight": streetsLight,
        "streetsBold": streetsBold
      };
      
      L.control.layers(null, overlayMaps).addTo(macrostratMap);
     
    
        // add the OpenTopoMap tile layer to the map
      topo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
            maxZoom: 17,
            attribution: 'Map data: &copy; OpenStreetMap contributors, SRTM | Rendering: &copy; <a href="https://opentopomap.org/about">OpenTopoMap</a>'
        })
          
          L.control.layers({
            "openstreet": openstreet,
            "topo": topo,
          }, null, {
            collapsed: false
          }).addTo(map);

          topo.addTo(map)


          async function fetchData(latitude,longitude) {
            const data = {
              latitude: latitude,
              longitude: longitude
            };
            console.log("sending data over of :",data)
            await fetch('/fieldStopIntro', {
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
                //const paragraph = document.createElement('p');
                
                // Set the content of the paragraph to the received data
                //paragraph.textContent = JSON.stringify(result);
                finishAfterGenerationBack(result)
                return result
                // Get the div element with the ID of dataHolder
                //const dataHolder = document.getElementById('dataHolder');
                
                // Append the paragraph element to the dataHolder div
                //dataHolder.appendChild(paragraph);
              })
              .catch(error => {
                console.error('Error:', error);
              });
          }

          function parseCoordinates(str) {
            //latitude = 38.861499, longitude = -110.858994
            const coordinates = {};
            latlongstrings = str.split(',')
            latPlus = latlongstrings[0]
            lngPlus = latlongstrings[1]
            coordinates.lat = parseFloat(latPlus.split('=')[1].trim())
            coordinates.lng = parseFloat(lngPlus.split('=')[1].trim())
            return {"latlng":coordinates}
          }
          
        
          function addDataToGenerativeText(jsonData) {
            const generativeText = document.getElementById('GenerativeText');
          
            // Extract location and geology_response values from JSON
            const location = jsonData.location;
            const geologyResponse = jsonData.geology_response;
            // parse coordinates for link
            console.log("location before coordinatesInObject to be added as onclick = ",location)
            coordinatesInObject = parseCoordinates(location)
            console.log("coordinatesInObject to be added as onclick = ",coordinatesInObject)
          
            // Create the div element
            const divElement = document.createElement('div');

            // Create the location paragraph element and set its text
            const locationParagraph = document.createElement('p');
            const locationLink = document.createElement('a');
            locationLink.textContent = 'Location: ' + location;
            locationLink.className = "link"
            
            // Add a click event listener to the location link
            locationLink.addEventListener('click', () => {
                // Simulate the map click behavior when clicked
                console.log("coordinatesInObject to be added as onclick = ",coordinatesInObject)
                mapClick(coordinatesInObject)
            });
              // Append the location link to the paragraph element
            locationParagraph.appendChild(locationLink);
            
            // Create the geology_response paragraph element and set its text
            const geologyResponseParagraph = document.createElement('p');
            geologyResponseParagraph.textContent = 'Geology Response: ' + geologyResponse;
          
            // Append the paragraph elements to the div element
            divElement.appendChild(locationParagraph);
            divElement.appendChild(geologyResponseParagraph);
          
            // Append the div element to the GenerativeText div
            generativeText.appendChild(divElement);
          }  

        function finishAfterGenerationBack(responseJSON){
            const geology_response = responseJSON["geology_response"];
            const location_used = responseJSON["location"];
            // Add data to GenerativeText
            addDataToGenerativeText(responseJSON);
            // Get the generate button and spinner element
            const generateButton = document.getElementById('generateButton');
            const spinner = document.querySelector('.spinner');
            // Hide the spinner
            spinner.style.display = 'none';
            // Update last point generated
            updateLastPointGenerated(location_used)
            // refresh button
            generateButton.innerText = 'Generate Field Trip Stop Description';
            generateButton.style.backgroundColor = '#4caf50';
            spinner.style.display = 'none';
        }

        function updateLastPointGenerated(locationLatLong){
            const infoBox = document.getElementById('infoBoxLastGeneratedPoint');
            const spanElement = infoBox.querySelector('span');
            // Replace the current text with the new text
            const newText = "updateLastPointGenerated: "+toString(locationLatLong)
            // Update the span element with the new text
            spanElement.innerText = newText;
        }

        function mapClick(e){            
            var latlng = e.latlng;
            latitude = parseFloat(latlng.lat.toFixed(6))
            longitude = parseFloat(latlng.lng.toFixed(6))
            lat = document.getElementById("latP")
            console.log("clicked lat",lat)
            lat.innerHTML = latlng.lat.toFixed(6);
            lng = document.getElementById("lngP")
            lng.innerHTML = latlng.lng.toFixed(6);
            var circle = L.circle(e.latlng, {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.3,
                radius: 50
            })
            circle.addTo(map);
            var circleClone = L.circle(e.latlng, {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.3,
                radius: 50
            })
            circleClone.addTo(macrostratMap)

            var streetview = new google.maps.StreetViewPanorama(document.getElementById("streetview"), {
                position: {lat: latlng.lat, lng: latlng.lng},
                pov: {heading: 165, pitch: 0},
                zoom: 1
            });

            // var streetviewMarker = new google.maps.Marker({
            //     position: {lat: latlng.lat, lng: latlng.lng},
            //     map: streetview
            // });

            getGeologyData(latlng.lat, latlng.lng).then(data => {
                    console.log("data",data)
                    const macrostratPointDiv = document.getElementById("macrostratPoint")
                    const resultsHolder = document.getElementById("results")
                    resultsHolder.innerHTML = ""
                    
                    data =  data["success"]["data"]
                    try {
                        data = data.slice(0, 2)
                        data.sort((a, b) => a.b_age.localeCompare(b.b_age));
                      }
                      catch(err) {
                        data = data
                      }
                    for (let i = 0; i < data.length; i++) {
                        const result = data[i];
                        const resultDiv = document.createElement('div');
                        resultDiv.classList.add('result');

                        const title = document.createElement('h4');
                        title.textContent = result.name;
                        resultDiv.appendChild(title);

                        const age_words = document.createElement('p');
                        age_words.textContent = "AGE: "+result.t_int_name+" to "+result.b_int_name                 ;
                        resultDiv.appendChild(age_words);

                        const age_range = document.createElement('p');
                        age_range.textContent = "AGE: "+result.t_age+" to "+result.b_age+" millions years"                        ;
                        resultDiv.appendChild(age_range);

                        const lithSingular = document.createElement('p');
                        lithSingular.textContent = "Lith: "+result.lith                        ;
                        resultDiv.appendChild(lithSingular);

                        const description = document.createElement('p');
                        description.textContent = result.descrip;
                        resultDiv.appendChild(description);

                        const comments = document.createElement('p');
                        description.textContent = result.comments;
                        resultDiv.appendChild(comments);

                        const source = document.createElement('p');
                        source.textContent = "source ID ="+result.source_id                        ;
                        resultDiv.appendChild(source);

                        resultsHolder.append(resultDiv);
                    };
                    console.log("data",data)
                }
            );
        }

        var ignoreNextZoom = false;

        map.on('move', function(e) {
            if (!ignoreNextZoom) {
                var center = map.getCenter();
                macrostratMap.setView(center, map.getZoom(), { animate: false });
            }
            ignoreNextZoom = false;
        });

        macrostratMap.on('move', function(e) {
            if (!ignoreNextZoom) {
                var center = macrostratMap.getCenter();
                map.setView(center, macrostratMap.getZoom(), { animate: false });
            }
            ignoreNextZoom = false;
        });

        map.on('click', function(e) {
            mapClick(e)
        });

        macrostratMap.on('click', function(e) {
            mapClick(e)
        });

        map.on('zoomend', function(e) {
            ignoreNextZoom = true;
        });

        macrostratMap.on('zoomend', function(e) {
            ignoreNextZoom = true;
        });

    // Get the generate button and spinner element
    const generateButton = document.getElementById('generateButton');
    const spinner = document.querySelector('.spinner');

    // Add a click event listener to the generate button
    generateButton.addEventListener('click', () => {
        // Toggle the visibility of the spinner
        spinner.style.display = 'block';
      
        async function fetchDataAndAddData() {
          if (generateButton.innerText === 'Generate Field Trip Stop Description') {
            generateButton.innerText = 'Stop Generation';
            generateButton.style.backgroundColor = 'orange';
            
            //// Get last clicked lat and long from HTML
            const latPElement = document.getElementById('latP');
            const latValue = parseFloat(latPElement.textContent);
            const lngPElement = document.getElementById('lngP');
            const lngValue = parseFloat(lngPElement.textContent);
            // Call fetchData and wait for the response
            const responseJSON = await fetchData(latValue, lngValue);
          } else {
            generateButton.innerText = 'Generate Field Trip Stop Description';
            generateButton.style.backgroundColor = '#4caf50';
            spinner.style.display = 'none';
          }
        }
        // Call the async function
        fetchDataAndAddData();
      });
      


     
