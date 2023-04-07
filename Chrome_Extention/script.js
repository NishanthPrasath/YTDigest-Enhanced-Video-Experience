async function uploadData(){

    var language = document.getElementById("language").value;
    var link = document.getElementById("link").value;

      // Do something with the values (for example, log them to the console)
    console.log("Language:", language.toString());
    console.log("Link:", link.toString());

    const data = {
        "link": link.toString(),
        "language": language.toString()
      };

    console.log("Data:", data);
    const res = await fetch('http://localhost:8080/transcribeAndStore', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
    const response = await res.json()
    console.log(response)
}

const form = document.querySelector("form");
form.addEventListener("submit", uploadData);