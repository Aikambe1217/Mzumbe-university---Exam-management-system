document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded")

  // DOM Elements
  const sidebar = document.getElementById("sidebar")
  const toggleSidebar = document.getElementById("toggle-sidebar")
  const closeSidebar = document.getElementById("close-sidebar")
  const overlay = document.getElementById("overlay")
  const addLecturerBtn = document.getElementById("addLecturerBtn")
  const addLecturerModal = document.getElementById("addLecturerModal")
  const closeModalBtn = document.querySelector(".close-modal")
  const cancelBtn = document.querySelector(".cancel-btn")
  const addLecturerForm = document.getElementById("addLecturerForm")
  const notification = document.getElementById("notification")
  const recordSubmissionForm = document.getElementById("recordSubmissionForm")
  const fileUpload = document.getElementById("fileUpload")
  const fileList = document.getElementById("fileList")
  const recordCollectionForm = document.getElementById("recordCollectionForm")
  const missingBooklets = document.getElementById("missingBooklets")
  const missingBookletsSection = document.getElementById("missingBookletsSection")
  const searchRecordBtn = document.getElementById("searchRecordBtn")
  const returnForm = document.getElementById("returnForm")
  const reportFiltersForm = document.getElementById("reportFiltersForm")

  console.log("Sidebar element:", sidebar)
  console.log("Toggle sidebar button:", toggleSidebar)

  // Toggle sidebar on mobile
  if (toggleSidebar) {
    console.log("Adding click event to toggle sidebar button")
    toggleSidebar.addEventListener("click", (e) => {
      e.preventDefault()
      console.log("Toggle sidebar clicked")
      if (sidebar) {
        sidebar.classList.toggle("active")
        overlay.classList.toggle("active")
        document.body.style.overflow = sidebar.classList.contains("active") ? "hidden" : ""
        console.log("Sidebar active state:", sidebar.classList.contains("active"))
      }
    })
  }

  // Close sidebar
  if (closeSidebar) {
    closeSidebar.addEventListener("click", (e) => {
      e.preventDefault()
      console.log("Close sidebar clicked")
      if (sidebar) {
        sidebar.classList.remove("active")
        overlay.classList.remove("active")
        document.body.style.overflow = ""
      }
    })
  }

  // Close sidebar when clicking on overlay
  if (overlay) {
    overlay.addEventListener("click", () => {
      if (sidebar) {
        sidebar.classList.remove("active")
      }
      overlay.classList.remove("active")
      document.body.style.overflow = ""

      if (addLecturerModal) {
        addLecturerModal.classList.remove("active")
      }
    })
  }

  // Open Add Lecturer Modal
  if (addLecturerBtn && addLecturerModal) {
    addLecturerBtn.addEventListener("click", () => {
      addLecturerModal.classList.add("active")
    })
  }

  // Close Modal
  if (closeModalBtn && addLecturerModal) {
    closeModalBtn.addEventListener("click", () => {
      addLecturerModal.classList.remove("active")
    })
  }

  // Cancel Button in Modal
  if (cancelBtn && addLecturerModal) {
    cancelBtn.addEventListener("click", () => {
      addLecturerModal.classList.remove("active")
    })
  }

  // Add Lecturer Form Submission
  if (addLecturerForm) {
    addLecturerForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Get form values
      const name = document.getElementById("lecturerName").value
      const department = document.getElementById("department").value
      const phone = document.getElementById("phoneNumber").value
      const email = document.getElementById("email").value

      // Create new lecturer row
      const tableBody = document.getElementById("lecturersTableBody")
      const newRow = document.createElement("tr")

      newRow.innerHTML = `
              <td>${name}</td>
              <td>${department}</td>
              <td>${phone}</td>
              <td>${email}</td>
              <td>0</td>
              <td><span class="status good">Good</span></td>
              <td class="actions">
                  <button class="view-btn" title="View Details"><i class="fas fa-eye"></i></button>
                  <button class="edit-btn" title="Edit"><i class="fas fa-edit"></i></button>
              </td>
          `

      // Add row to table
      if (tableBody) {
        tableBody.appendChild(newRow)
      }

      // Close modal and show notification
      addLecturerModal.classList.remove("active")
      showNotification("Lecturer added successfully!")

      // Reset form
      addLecturerForm.reset()
    })
  }

  // Record Submission Form
  if (recordSubmissionForm) {
    recordSubmissionForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Show notification
      showNotification("Record submitted successfully!")

      // Reset form
      recordSubmissionForm.reset()
      if (fileList) {
        fileList.innerHTML = ""
      }
    })
  }

  // Record Collection Form
  if (recordCollectionForm) {
    recordCollectionForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Get form values
      const lectureName = document.getElementById("lectureName").value
      const bookletCount = document.getElementById("bookletCount").value
      const phoneNumber = document.getElementById("phoneNumber").value
      const returnDate = document.getElementById("returnDate").value

      // Create new collection item
      const recentCollections = document.getElementById("recentCollections")
      const newCollection = document.createElement("div")
      newCollection.className = "collection-item"

      // Format the return date
      const formattedDate = new Date(returnDate).toLocaleDateString("en-US", {
        day: "numeric",
        month: "short",
        year: "numeric",
      })

      newCollection.innerHTML = `
        <div class="collection-details">
          <h4>${lectureName}</h4>
          <p><i class="fas fa-book"></i> ${bookletCount} Booklets</p>
          <p><i class="fas fa-phone"></i> ${phoneNumber}</p>
          <p><i class="fas fa-calendar-alt"></i> Return by: ${formattedDate}</p>
        </div>
        <div class="collection-status">
          <span class="status-badge pending">Pending Return</span>
        </div>
      `

      // Add to recent collections
      if (recentCollections) {
        // Insert at the beginning
        recentCollections.insertBefore(newCollection, recentCollections.firstChild)
      }

      // Show notification
      showNotification("Collection recorded successfully!")

      // Reset form
      recordCollectionForm.reset()
    })
  }

  // Return Form
  if (returnForm) {
    returnForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Show notification
      showNotification("Return processed successfully!")

      // Reset form
      returnForm.reset()

      // Reset preview
      const previewElements = document.querySelectorAll("#recordDetails .detail-value")
      previewElements.forEach((el) => {
        el.textContent = "--"
      })

      if (missingBookletsSection) {
        missingBookletsSection.style.display = "none"
      }
    })
  }

  // Search Record Button
  if (searchRecordBtn) {
    searchRecordBtn.addEventListener("click", () => {
      const recordId = document.getElementById("recordId").value

      if (recordId) {
        // Simulate finding record data
        document.getElementById("previewCourse").textContent = "CS301 - Data Structures"
        document.getElementById("previewLecturer").textContent = "Dr. Johnson"
        document.getElementById("previewCollectionDate").textContent = "15 Jun 2023"
        document.getElementById("previewBooklets").textContent = "42"

        showNotification("Record found!")
      } else {
        showNotification("Please enter a Record ID")
      }
    })
  }

  // Missing Booklets Checkbox
  if (missingBooklets && missingBookletsSection) {
    missingBooklets.addEventListener("change", function () {
      missingBookletsSection.style.display = this.checked ? "block" : "none"
    })
  }

  // Report Filters Form
  if (reportFiltersForm) {
    reportFiltersForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Show notification
      showNotification("Report generated successfully!")
    })
  }

  // File Upload
  if (fileUpload && fileList) {
    fileUpload.addEventListener("change", function () {
      fileList.innerHTML = ""

      if (this.files.length > 0) {
        for (let i = 0; i < this.files.length; i++) {
          const file = this.files[i]
          const fileItem = document.createElement("div")
          fileItem.className = "file-item"
          fileItem.innerHTML = `
                      <i class="fas fa-file"></i>
                      <span>${file.name}</span>
                  `
          fileList.appendChild(fileItem)
        }
      }
    })
  }

  // Show notification function
  function showNotification(message) {
    if (notification) {
      const notificationMessage = document.getElementById("notificationMessage")
      if (notificationMessage) {
        notificationMessage.textContent = message
      }

      notification.classList.add("active")

      setTimeout(() => {
        notification.classList.remove("active")
      }, 3000)
    }
  }

  // Search functionality for lecturers
  const searchLecturers = document.getElementById("searchLecturers")
  if (searchLecturers) {
    searchLecturers.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase()
      const rows = document.querySelectorAll("#lecturersTableBody tr")

      rows.forEach((row) => {
        const text = row.textContent.toLowerCase()
        if (text.includes(searchTerm)) {
          row.style.display = ""
        } else {
          row.style.display = "none"
        }
      })
    })
  }

  // Handle active navigation links
  const currentPage = window.location.pathname.split("/").pop()
  const navLinks = document.querySelectorAll(".sidebar-menu a")

  navLinks.forEach((link) => {
    const linkPage = link.getAttribute("href")
    if (currentPage === linkPage || (currentPage === "" && linkPage === "index.html")) {
      link.classList.add("active")
    } else {
      link.classList.remove("active")
    }
  })

  // Responsive behavior for window resize
  window.addEventListener("resize", () => {
    if (window.innerWidth > 768) {
      if (sidebar) {
        sidebar.classList.remove("active")
      }
      if (overlay) {
        overlay.classList.remove("active")
      }
      document.body.style.overflow = ""
    }
  })
})

// profile



