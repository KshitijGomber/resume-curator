document.getElementById("submitBtn").addEventListener("click", async function() {
  const fileInput = document.getElementById("resumeUpload");
  const jobDesc = document.getElementById("jobDesc").value;
  const loadingIndicator = document.getElementById("loading");
  const outputContainer = document.getElementById("output-container");
  const optimizedResume = document.getElementById("optimizedResume");

  // Basic validation
  if (!fileInput.files.length || !jobDesc) {
    alert("Please upload a resume and enter a job description.");
    return;
  }

  // Prepare form data
  const formData = new FormData();
  formData.append("resume", fileInput.files[0]);
  formData.append("jobDesc", jobDesc);

  try {
    // Show loading spinner
    loadingIndicator.classList.remove("d-none");
    outputContainer.classList.add("d-none");

    // Send POST request to FastAPI
    // const response = await fetch("http://127.0.0.1:5438/upload", {  // ✅ Added /upload
    //   method: "POST",
    //   body: formData
    // });
    const response = await fetch("https://resume-curator.onrender.com/upload", {  
      method: "POST",
      body: formData
    });
    
    
    // const response = await fetch("http://3.147.54.116:5438/upload", {  
    //   method: "POST",
    //   body: formData
    // });
    if (!response.ok) throw new Error("Server error");
    
    // Parse JSON
    const data = await response.json();

    // data.highlighted_resume is from your OpenAI approach
    // or if you have "data.optimized_text" from Gemini, adapt accordingly:
    // e.g.: 
    // optimizedResume.innerHTML = marked.parse(data.optimized_text);

    optimizedResume.innerHTML = marked.parse(data.highlighted_resume);

    // Show output
    outputContainer.classList.remove("d-none");

  } catch (error) {
    console.error("Error:", error);
    alert("Failed to process the resume.");
  } finally {
    // Hide loading spinner
    loadingIndicator.classList.add("d-none");
  }
});
