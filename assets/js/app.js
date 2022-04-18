"use strict"

// Query-selectors
function ONE(selector, element = document) {
  return element.querySelector(`${selector}`)
}
function ALL(selector, element = document) {
  return element.querySelectorAll(`${selector}`)
}




// Input-field length counter
function countInputLength(input = event.target) {
  const parent = input.parentElement
  const inputLength = input.value.length
  const counter = ONE(".counter span", parent)
  counter.textContent = inputLength
}



// Form validation
function formValidation(callback) {
  event.preventDefault()
  const form = event.target.form
  const isValid = form.checkValidity()

  if (isValid) {
    callback(form)
  }
}




// Text area validation
function validateTextArea() {
  const textArea = event.target
  const string = textArea.value
  // No blank start
  if (string == " " || string == "\n") textArea.value = ""
  // No double-space or line-breaks
  if (string.includes("  ") || string.includes("\n")) textArea.value = string.substring(0, string.length - 1)

  resizeTextArea(textArea)
  countInputLength(textArea)
}
function resizeTextArea(textArea) {
  textArea.style.height = "auto"
  textArea.style.height = textArea.scrollHeight + "px"
}




// When uploading tweeb image
function loadTweebImage() {
  const form = event.target.form

  // If change-event triggered by removing the img - return
  if (!event.target.value) return

  // If an uploaded image already shown - remove
  if (ONE(".image_container", form)) ONE(".image_container", form).remove()

  // Create and insert new img
  const newImg = `
  <div class="image_container">
    <img src="${URL.createObjectURL(event.target.files[0])}">
    <div class="x" onclick="removeTweebImage()">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g><path d="M13.414 12l5.793-5.793c.39-.39.39-1.023 0-1.414s-1.023-.39-1.414 0L12 10.586 6.207 4.793c-.39-.39-1.023-.39-1.414 0s-.39 1.023 0 1.414L10.586 12l-5.793 5.793c-.39.39-.39 1.023 0 1.414.195.195.45.293.707.293s.512-.098.707-.293L12 13.414l5.793 5.793c.195.195.45.293.707.293s.512-.098.707-.293c.39-.39.39-1.023 0-1.414L13.414 12z"></path></g></svg>
    </div>
  </div>
  ` 
  ONE("label", form).insertAdjacentHTML("afterend", newImg)
}

// Removing tweeb image
function removeTweebImage() {
  const form = event.target.form
  ONE(".image_container", form).remove()
  ONE("[name='tweeb_image']", form).value = ""
}




// Is email in DB?
async function doesEmailExist() {
  const field = event.target
  const email = field.value
  const form = field.form

  // Make field invalid untill the result is found
  field.setCustomValidity("Invalid")

  // Don't throw error if field is empty
  if (!email) {
    return
  }

  // Look for email in db 
  const conn = await fetch(`/get-user-by-email/${email}`, {
    method : "GET",
  })
  if (!conn.ok) {
    console.log(conn)
  }

  // if exist
  if (conn.status == 200) {
    const error = {
      error_key : "user_email",
      error_message : "Email already registered"
    }
    handleServerValidation(error, form)

  }  else (field.setCustomValidity(""))
}




// #########################
// SPA


// SET INIT STATE
let memoUrl = getUrlPath()
history.replaceState({ spaUrl: memoUrl, initPage: true }, "", memoUrl)

// Returns current url-path widthout domain-name
function getUrlPath() {
  const href = window.location.href
  const idxOfSlash = href.indexOf("/", 8)
  return href.substring(idxOfSlash)
}

// Set anchor for current page as "current"
if (ONE(`#left [href="${memoUrl}"]:not(.logo)`)) {
  ONE(`#left [href="${memoUrl}"]:not(.logo)`).classList.add("current")
}

function highligtCurrentAnchor (spaUrl) {
  if(ONE(`#left a.current`)) {
    ONE(`#left a.current`).classList.remove("current")
  }
  if (ONE(`#left [href="${spaUrl}"]:not(.logo)`)) {
    ONE(`#left [href="${spaUrl}"]:not(.logo)`).classList.add("current")
  }
}



// MAIN SPA HANDLER
async function spa(spaUrl, parent ="#feed", doPushState = true) {
  // Prevent default for anchor tags
  event.preventDefault()

  // Do nothing if requested url is same as current url
  if (spaUrl == memoUrl) {
    return
  }

  // Don't push state when popstate-event
  if (doPushState) {
    history.pushState({ spaUrl: spaUrl }, "", spaUrl)
  }

  const existingModule = ONE(`[data-spa_url="${spaUrl}"]`)
  const prevSpaModule = ONE(`[data-spa_url="${memoUrl}"]`)

  
  // If module don't exist fetch
  // Or if switching beetween feeds - fetch new to update the content
  if (!existingModule 
    || parent == "#feed" && prevSpaModule.dataset.spa_type == "feed"
    || spaUrl.includes("update")) {
    if (existingModule) existingModule.remove()
    const html = await getSpaModule(spaUrl)
    ONE(parent).insertAdjacentHTML("afterbegin", html)
  } 
  
  else {
    ONE(`[data-spa_url="${spaUrl}"]`).classList.remove("hide")
  }

  hidePrevSpaModules(spaUrl)
  if (parent == "#feed") highligtCurrentAnchor(spaUrl)

  // memorize url for popstate-events
  memoUrl = spaUrl
}

function hidePrevSpaModules(spaUrl) {
  const prevSpaModule = ONE(`[data-spa_url="${memoUrl}"]`)
  const newSpaModule = ONE(`[data-spa_url="${spaUrl}"]`)

  // Feeds remove feeds to update the content
  if (newSpaModule.dataset.spa_type == "feed" && prevSpaModule.dataset.spa_type == "feed") {
    prevSpaModule.classList.add("hide")
  }

  // All spa_types hide modals    
  if (prevSpaModule.dataset.spa_type == "modal") {
    const form = ONE("form", prevSpaModule)
    prevSpaModule.classList.add("hide")
    resetForm(form)
  }
}


async function getSpaModule(spaUrl) {
  const conn = await fetch(spaUrl, {
    method: "GET",
    headers: { spa: true },
  })

  const res = await conn.text()

  // If response can be parsed as JSON, it's an error that needs action
  try {
    const error = JSON.parse(res)
    location.href = error.error_url
  }

  catch {
    return res
  }
}





function resetForm (form) {

  const counters = ALL(".counter span", form)
  counters.forEach((elm) => elm.textContent = 0)

  const customErrors = ALL(".custom_error", form)
  customErrors.forEach((elm) => elm.remove())

  const labels = ALL("label", form)
  labels.forEach((elm) => elm.classList.remove("error_400"))

  const defaultErrors = ALL(".error_message", form)
  defaultErrors.forEach((elm) => elm.classList.remove("hide"))

  form.reset()
}





// HISTORY BACK / FORWARD
window.addEventListener("popstate", (event) => {
  // Full page reload if prev elm doesnt exist
  // This only happens if user deleted som HTML, or hits a bridge
  if (!ONE(`[data-spa_url="${event.state.spaUrl}"]`))  {
    location.reload()
  }
  const parent = ONE(`[data-spa_url="${event.state.spaUrl}"]`).dataset.spa_parent

  spa(event.state.spaUrl, parent, false)
})


// Modal close btn
function closeSpaModal() {
  if (history.state.initPage) {
    console.log(history.state.spaUrl)
    console.log(memoUrl)
    // If modal is first state, push its origin page
    const url = ONE(`[data-spa_url="${memoUrl}"]`).dataset.spa_url_origin

    spa(url, "body")
  } else {
    history.back()
  }
}



// #########################
// API calls


// POST TWEEB
async function postTweeb (form) {
  const conn = await fetch("/tweebs", {
    method : "POST",
    body : new FormData(form)
  })

  if (!conn.ok) {
    console.log(conn)
    const error = await conn.json()
    if ( conn.status == 400 ) handleServerValidation(error, form)
    return
  }

  const tweeb = await conn.text()
  const currentPage = ONE("a.current")
  if (currentPage.classList.contains("home") || currentPage.classList.contains("profile")) {
    ONE("#feed .tweebs").insertAdjacentHTML("afterbegin", tweeb)
  }

  // FINALLY reset the form
  resetForm(form)

  // Remove image container if exists
  if (ONE(".image_container", form)) {
    ONE(".image_container", form).remove()
  }

  // If posted via modal
  if (ONE(`[data-spa_url="${memoUrl}"]`).dataset.spa_type == "modal") {
    closeSpaModal()
  } 
}



// POST USER / sign up
async function postUser (form) {
  const conn = await fetch("/users", {
    method : "POST",
    body : new FormData(form)
  })

  if (!conn.ok) {
    const error = await conn.json()
    if ( conn.status == 400 ) handleServerValidation(error, form)
    return
  }

  // SUCCES go to /home
  window.location.href = "/home"
}



// POST SESSION / sign in
async function postSession (form) {
  const conn = await fetch("/sessions", {
    method : "POST",
    body : new FormData(form)
  })

  if (!conn.ok) {
    const error = await conn.json()
    if ( conn.status == 400 ) handleServerValidation(error, form)
    return
  }

  console.log(conn)
  // SUCCES go to /home
  window.location.href = "/home"
}



// POST FOLLOW
async function postFollow() {
  event.preventDefault()
  const form = event.target.form
  const btn = event.target

  const conn = await fetch("/follows", {
    method : "POST",
    body : new FormData(form)
  })

  if (!conn.ok) {
    console.log(conn)
    const error = await conn.text()
    console.log(error)
    return
  }

  // SUCCES
  const newBtn = "<button class='unfollow' onclick='deleteFollow()'>Following</button>"
  btn.remove()
  form.insertAdjacentHTML("afterbegin", newBtn)
}


// DELETE FOLLOW
async function deleteFollow() {
  event.preventDefault()
  const form = event.target.form
  const btn = event.target
  
  const conn = await fetch("/follows", {
    method : "DELETE",
    body : new FormData(form)
  })

  if (!conn.ok) {
    console.log(conn)
    return
  }

  // SUCCES
  const newBtn = "<button onclick='postFollow()'>Follow</button>"
  btn.remove()
  form.insertAdjacentHTML("afterbegin", newBtn)
}





// DELETE TWEEB
async function deleteTweeb () {
  event.preventDefault()
  const form = event.target.form
  const tweebId = form.tweeb_id.value

  const conn = await fetch(`/tweebs/${tweebId}`,{
    method : "DELETE"
  })

  if (!conn.ok) {
    const error = await conn.json()
    if ( conn.status == 400 ) handleServerValidation(error, form)
    return
  }

  // Conn ok, but nothing were deleted
  if (conn.status == 204) return

  // Succes - remove the tweeb from DOM
  form.remove()
}





// UPDATE TWEEB
async function updateTweeb() {
  const form = event.target.form
  const conn = await fetch("/tweebs", {
    method : "PUT",
    body : new FormData(form)
  })
  
  if (!conn.ok) {
    console.log(conn)
    const error = await conn.json()
    console.log(error)
  }

  if (conn.status == 204) {
    closeSpaModal()
    return
  }

  const updatedTweeb = await conn.text()
  const tweeb_id = form.tweeb_id.value
  const tweeb = ONE(`.tweeb [value="${tweeb_id}"]`).form
  tweeb.outerHTML = updatedTweeb
  closeSpaModal()
}





// VALIDATION FROM SERVER
// Takes array of error_key, error_url, error_message + the form-element
function handleServerValidation(error, form) {

  // Server error that requires redirect
  if (error.error_url) {
    location.href = error.error_url
  }

  const field = ONE(`[name="${error.error_key}"]`, form)
  const parent = field.parentElement
  parent.classList.add("error_400")
  field.setCustomValidity("Invalid")

  
  // Custom error form server
  if (error.error_message) {
    // Hide default error if exist
    if (ONE(".error_message", parent)) ONE(".error_message", parent).classList.add("hide")

    // Append custom error
    const customError = `<p class="custom_error" >${error.error_message}</p>`
    parent.insertAdjacentHTML("beforeend", customError)
  }


  field.addEventListener("input", rmCustomError)

  function rmCustomError() {
    field.removeEventListener("input", rmCustomError)
    field.setCustomValidity("")
    parent.classList.remove("error_400")

    // Remove costum error and reset styling for default error - if exist
    if (ONE(".custom_error", parent)) ONE(".custom_error", parent).remove()
    if (ONE(".error_message", parent)) ONE(".error_message", parent).classList.remove("hide")
  } 
}

