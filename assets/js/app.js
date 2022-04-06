"use strict";

// Query-selectors
function ONE(selector, element = document) {
  return element.querySelector(`${selector}`);
}
function ALL(selector, element = document) {
  return element.querySelectorAll(`${selector}`);
}




// Input-field length counter
function countInputLength(input = event.target) {
  const parent = input.parentElement;
  const inputLength = input.value.length;
  const counter = ONE(".counter span", parent);
  counter.textContent = inputLength;
}
function resetCounters(parent) {
  const counters = ALL(".counter span", parent);
  counters.forEach((counter) => {
    counter.textContent = 0;
  });
}




// Form validation
function formValidation(callback) {

  // Prevent automatic valdation and check manually
  event.preventDefault();
  const form = event.target.form;
  const isValid = form.checkValidity();

  // If invalid, set class "error"
  if (!isValid) {
    form.classList.add("error");
    return
  } 

  // Succes, call API
  callback
}




// Text area validation
function validateTextArea() {
  const textArea = event.target;
  const string = textArea.value;
  // No blank start
  if (string == " " || string == "\n") textArea.value = "";
  // No double-space or triple new-lines
  if (string.includes("  ") || string.includes("\n\n\n")) textArea.value = string.substring(0, string.length - 1);

  resizeTextArea(textArea);
  countInputLength(textArea);
}
function resizeTextArea(textArea) {
  textArea.style.height = "auto";
  textArea.style.height = textArea.scrollHeight + "px";
}






// #########################
// SPA


// SET INIT STATE
let memoUrl = getUrlPath();
history.replaceState({ spaUrl: memoUrl, initPage: true }, "", memoUrl);
// Returns current url-path widthout domain-name
function getUrlPath() {
  const href = window.location.href;
  const idxOfSlash = href.indexOf("/", 8);
  return href.substring(idxOfSlash);
}



// MAIN SPA HANDLER
async function spa(spaUrl, parent = "#feed", doPushState = true) {

  if (doPushState) {
    history.pushState({ spaUrl: spaUrl }, "", spaUrl);
  }


  // Get module if not in DOM
  if (!ONE(`[data-spa_url="${spaUrl}"]`)) {
    const conn = await fetch(spaUrl, {
      method: "GET",
      headers: { spa: true },
    });
    const html = await conn.text();
    ONE(parent).insertAdjacentHTML("afterbegin", html);

    // Display module if exist
  } else {
    ONE(`[data-spa_url="${spaUrl}"]`).classList.remove("hide");
  }



  const prevSpaModule = ONE(`[data-spa_url="${memoUrl}"]`);
  const newSpaModule = ONE(`[data-spa_url="${spaUrl}"]`);

  // Feeds hide all exept mains
  if (newSpaModule.dataset.spa_type == "feed" && prevSpaModule.dataset.spa_type != "main") {
    prevSpaModule.classList.add("hide")
  }
  // Modals only hide modals and needs reset
  if (prevSpaModule.dataset.spa_type == "modal") {
    ONE("form", prevSpaModule).reset();
    resetCounters(prevSpaModule);
    prevSpaModule.classList.add("hide");
  }



  // memorize url for popstate
  memoUrl = spaUrl;
}




// HISTORY BACK / FORWARD
window.addEventListener("popstate", (event) => {

  // Full page reload if prev elm doesnt exist
  // This is done to prevent bugs on page-shift between index.html and main.html.
  if (!ONE(`[data-spa_url="${event.state.spaUrl}"]`)) {
    location.reload()
  }
  
  // Parent-elm doesn't matter since the element needs to exist according to the declaration above
  spa(event.state.spaUrl, false, false);
});


// Modal close btn
function closeSpaModal() {
  const modal = ONE(`[data-spa_url="${memoUrl}"]`);

  // Hide if page is the first - history page if not
  if (history.state.initPage) {
    spa("/", "body");
    console.log("initpage");
  } else {
    history.back();
  }

  resetCounters(modal);
}



// #########################


//
// API calls
async function postTweeb () {

  const form = event.target.form
  const conn = await fetch("/tweebs", {
    method: "POST",
    body : new FormData(form)
  })

  if (!conn.ok) {
    console.log(conn);
    return;
  }

  const tweeb = await conn.text();
  console.log(tweeb)
}
