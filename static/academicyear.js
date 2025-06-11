// Debug function to help troubleshoot
function debug(message, data) {
    console.log(`DEBUG: ${message}`, data)
  }
  
  function getCurrentAcademicYear() {
    const today = new Date()
    const currentMonth = today.getMonth() + 1
    const currentYear = today.getFullYear()
  
    let academicYear
    if (currentMonth >= 10) {
      academicYear = `${currentYear}/${String(currentYear + 1).slice(2)}`
    } else if (currentMonth <= 7) {
      academicYear = `${currentYear - 1}/${String(currentYear).slice(2)}`
    } else {
      academicYear = `${currentYear}/${String(currentYear + 1).slice(2)}`
    }
  
    debug("Calculated academic year", academicYear)
    return academicYear
  }
  
  function getCurrentSemester() {
    const today = new Date()
    const currentMonth = today.getMonth() + 1
  
    let semesterNumber
    if (currentMonth >= 10 || currentMonth <= 2) {
      semesterNumber = 1
    } else if (currentMonth >= 3 && currentMonth <= 7) {
      semesterNumber = 2
    } else {
      semesterNumber = null
    }
  
    debug("Calculated semester number", semesterNumber)
    return semesterNumber
  }
  
  function getSemesterName(semesterNumber) {
    let name
    if (semesterNumber === 1) name = "Semester"
    else if (semesterNumber === 2) name = "Semester"
    else name = "Preparation Period"
  
    debug("Semester name for number " + semesterNumber, name)
    return name
  }
  
  function getSemesterDateRange(semesterNumber) {
    const today = new Date()
    const currentYear = today.getFullYear()
    const currentMonth = today.getMonth() + 1
  
    let dateRange
    if (semesterNumber === 1) {
      let startYear = currentYear
      if (currentMonth <= 7) startYear = currentYear - 1
      dateRange = `October 1, ${startYear} - February 28, ${currentMonth <= 7 ? currentYear : currentYear + 1}`
    } else if (semesterNumber === 2) {
      dateRange = `March 1, ${currentYear} - July 31, ${currentYear}`
    } else {
      dateRange = `August 1, ${currentYear} - September 30, ${currentYear}`
    }
  
    debug("Date range for semester " + semesterNumber, dateRange)
    return dateRange
  }
  
  function updateAcademicInfo() {
    debug("Starting updateAcademicInfo function", null)
  
    const academicYear = getCurrentAcademicYear()
    const semesterNumber = getCurrentSemester()
    const semesterName = getSemesterName(semesterNumber)
    const dateRange = getSemesterDateRange(semesterNumber)
  
    // Check if elements exist before updating them
    const updateElement = (id, value, attribute = "textContent") => {
      const element = document.getElementById(id)
      if (element) {
        element[attribute] = value
        debug(`Updated ${id} with ${value}`, element)
      } else {
        console.error(`Element with ID '${id}' not found!`)
      }
    }
  
    // Display on page
    updateElement("academicYear", `Academic Year: ${academicYear}`)
    updateElement("semester", semesterNumber ? `${semesterName} (${semesterNumber})` : semesterName)
    updateElement("dateInfo", dateRange)
    updateElement("badgeYear", academicYear)
    updateElement("badgeSemester", semesterNumber ? `Semester ${semesterNumber}` : "Prep Period")
  
    // Set values in hidden inputs
    updateElement("academic_year", academicYear, "value")
    updateElement("semester_number", semesterNumber, "value")
    updateElement("semester_name", semesterName, "value")
  
    // Also set values as data attributes on the form for backup
    // FIXED: Changed from "submission-form" to "recordSubmissionForm"
    const form = document.getElementById("recordSubmissionForm")
    if (form) {
      form.dataset.academicYear = academicYear
      form.dataset.semesterNumber = semesterNumber
      form.dataset.semesterName = semesterName
      debug("Set data attributes on form", form.dataset)
    } else {
      console.error("Form with ID 'recordSubmissionForm' not found!")
    }
  
    return {
      academicYear,
      semesterNumber,
      semesterName,
    }
  }
  
  // CSRF helper
  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }
  
  // Make sure the DOM is fully loaded
  document.addEventListener("DOMContentLoaded", () => {
    debug("DOM fully loaded", null)
  
    try {
      const academicInfo = updateAcademicInfo()
      debug("Academic info calculated", academicInfo)
  
      // Send academic info to server
      fetch("/submission/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          academic_year: academicInfo.academicYear,
          semester_number: academicInfo.semesterNumber,
          semester_name: academicInfo.semesterName,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          debug("Server response for academic info", data)
        })
        .catch((error) => {
          console.error("Error sending academic info:", error)
        })
  
      // Handle form submission
      // FIXED: Changed from "submission-form" to "recordSubmissionForm"
      const form = document.getElementById("recordSubmissionForm")
      if (form) {
        debug("Found submission form", form)
  
        form.addEventListener("submit", (e) => {
          // Ensure hidden fields have values before submission
          const academicYearInput = document.getElementById("academic_year")
          const semesterNumberInput = document.getElementById("semester_number")
          const semesterNameInput = document.getElementById("semester_name")
  
          // If hidden fields don't have values, use data attributes as backup
          if (academicYearInput && (!academicYearInput.value || academicYearInput.value === "")) {
            academicYearInput.value = form.dataset.academicYear || academicInfo.academicYear
            debug("Set academic year from backup", academicYearInput.value)
          }
  
          if (semesterNumberInput && (!semesterNumberInput.value || semesterNumberInput.value === "")) {
            semesterNumberInput.value = form.dataset.semesterNumber || academicInfo.semesterNumber
            debug("Set semester number from backup", semesterNumberInput.value)
          }
  
          if (semesterNameInput && (!semesterNameInput.value || semesterNameInput.value === "")) {
            semesterNameInput.value = form.dataset.semesterName || academicInfo.semesterName
            debug("Set semester name from backup", semesterNameInput.value)
          }
  
          debug("Form submitted with academic info", {
            year: academicYearInput ? academicYearInput.value : "not found",
            semester: semesterNumberInput ? semesterNumberInput.value : "not found",
            semesterName: semesterNameInput ? semesterNameInput.value : "not found",
          })
        })
      } else {
        console.error("Form with ID 'recordSubmissionForm' not found for event listener!")
      }
    } catch (error) {
      console.error("Error in initialization:", error)
    }
  })
  
  // Add a fallback in case DOMContentLoaded already fired
  if (document.readyState === "complete" || document.readyState === "interactive") {
    debug("Document already loaded, running init directly", document.readyState)
    setTimeout(() => {
      try {
        updateAcademicInfo()
      } catch (error) {
        console.error("Error in fallback initialization:", error)
      }
    }, 1)
  }
  

  


//   // This is a standalone script to test academic year calculation
// document.addEventListener("DOMContentLoaded", () => {
//     // Create debug container
//     const debugContainer = document.createElement("div")
//     debugContainer.style.position = "fixed"
//     debugContainer.style.bottom = "10px"
//     debugContainer.style.right = "10px"
//     debugContainer.style.backgroundColor = "#ffeeee"
//     debugContainer.style.padding = "10px"
//     debugContainer.style.border = "1px solid #ffcccc"
//     debugContainer.style.borderRadius = "5px"
//     debugContainer.style.zIndex = "9999"
//     debugContainer.style.maxWidth = "300px"
  
//     // Add title
//     const title = document.createElement("h4")
//     title.textContent = "Academic Year Debug"
//     debugContainer.appendChild(title)
  
//     // Calculate values
//     const today = new Date()
//     const currentMonth = today.getMonth() + 1
//     const currentYear = today.getFullYear()
  
//     // Add current date
//     const dateInfo = document.createElement("p")
//     dateInfo.innerHTML = `<strong>Current Date:</strong> ${today.toLocaleDateString()} (Month: ${currentMonth})`
//     debugContainer.appendChild(dateInfo)
  
//     // Calculate academic year
//     let academicYear
//     if (currentMonth >= 10) {
//       academicYear = `${currentYear}/${String(currentYear + 1).slice(2)}`
//     } else if (currentMonth <= 7) {
//       academicYear = `${currentYear - 1}/${String(currentYear).slice(2)}`
//     } else {
//       academicYear = `${currentYear}/${String(currentYear + 1).slice(2)}`
//     }
  
//     const yearInfo = document.createElement("p")
//     yearInfo.innerHTML = `<strong>Academic Year:</strong> ${academicYear}`
//     debugContainer.appendChild(yearInfo)
  
//     // Calculate semester
//     let semesterNumber, semesterName
//     if (currentMonth >= 10 || currentMonth <= 2) {
//       semesterNumber = 1
//       semesterName = "Semester"
//     } else if (currentMonth >= 3 && currentMonth <= 7) {
//       semesterNumber = 2
//       semesterName = "Semester"
//     } else {
//       semesterNumber = null
//       semesterName = "Preparation Period"
//     }
  
//     const semesterInfo = document.createElement("p")
//     semesterInfo.innerHTML = `<strong>Semester:</strong> ${semesterName} (${semesterNumber || "Prep"})`
//     debugContainer.appendChild(semesterInfo)
  
//     // Add close button
//     const closeButton = document.createElement("button")
//     closeButton.textContent = "Close"
//     closeButton.style.marginTop = "10px"
//     closeButton.onclick = () => {
//       document.body.removeChild(debugContainer)
//     }
//     debugContainer.appendChild(closeButton)
  
//     // Add to body
//     document.body.appendChild(debugContainer)
  
//     // Also update form fields directly
//     try {
//       const academicYearInput = document.getElementById("academic_year")
//       const semesterNumberInput = document.getElementById("semester_number")
//       const semesterNameInput = document.getElementById("semester_name")
  
//       if (academicYearInput) academicYearInput.value = academicYear
//       if (semesterNumberInput) semesterNumberInput.value = semesterNumber
//       if (semesterNameInput) semesterNameInput.value = semesterName
  
//       // Update display elements too
//       const academicYearDisplay = document.getElementById("academicYear")
//       const semesterDisplay = document.getElementById("semester")
//       const badgeYearDisplay = document.getElementById("badgeYear")
//       const badgeSemesterDisplay = document.getElementById("badgeSemester")
  
//       if (academicYearDisplay) academicYearDisplay.textContent = `Academic Year: ${academicYear}`
//       if (semesterDisplay)
//         semesterDisplay.textContent = semesterNumber ? `${semesterName} (${semesterNumber})` : semesterName
//       if (badgeYearDisplay) badgeYearDisplay.textContent = academicYear
//       if (badgeSemesterDisplay)
//         badgeSemesterDisplay.textContent = semesterNumber ? `Semester ${semesterNumber}` : "Prep Period"
//     } catch (e) {
//       console.error("Error updating form fields:", e)
//     }
//   })
  
  