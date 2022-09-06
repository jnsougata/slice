let input = document.getElementById("input");
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("generate").click();
  }
});

function notify(message, color) {
  const snackbar = document.getElementById("snackbar");
  snackbar.style.backgroundColor = color;
  snackbar.innerText = message;
  snackbar.classList.add("show");
  setTimeout(() => { snackbar.classList.remove("show"); }, 3000);
}

function shortenURL() {
  let isValid = true;
  let target = document.getElementById("input").value;

  if (target.length === 0) {
    notify("Please enter an URL", "red");
    return;
  }
  if (target.includes(window.location.host)) {
    notify("Already shrinked URL", "red");
    return;
  }
  if (!target.startsWith("http://") && !target.startsWith("https://")) {
    target = "http://" + target;
  }
  if (!target.match(/^(?:https?|ftp):\/\/(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4])|(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*\.[a-z\u00a1-\uffff]{2,})(?::\d{2,5})?(?:\/\S*)?$/)) {
    isValid = false;
  }
  if (!isValid) {
    notify("Please enter a valid URL", "red");
    return;
  }

  fetch("/shrink", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ target: target })
  })
    .then((response) => {
      if (!response.ok) {
        notify("Failed to shorten URL", "red");
        return "";
      }
      return response.json();
    })
    .then((json) => {
      const url = json.url;
      navigator.clipboard.writeText(url);
      document.getElementById("input").value = url;
      notify("Copied to clipboard", "green");
    })
}
