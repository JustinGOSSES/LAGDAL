async function getGeologyData(lat, lng) {
    // const url = `https://macrostrat.org/api/v2/units/geom?lat=${lat}&lng=${lng}&format=json`;
    const url =  `https://macrostrat.org/api/geologic_units/map/?lat=${lat}&lng=${lng}&response=long`
    
    return fetch(url)
      .then(
        response => response.json()
        )
      ;
  }