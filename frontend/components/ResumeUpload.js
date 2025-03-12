import { useState } from "react";

export default function ResumeUpload({ onUpload }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (
      selectedFile &&
      (selectedFile.type === "application/pdf" ||
        selectedFile.type ===
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    ) {
      setFile(selectedFile);
      onUpload(selectedFile);
    } else {
      alert("Only PDF and DOCX files are allowed.");
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} className="mt-2" />
      {file && <p className="mt-2 text-sm">{file.name}</p>}
    </div>
  );
}
