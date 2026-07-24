import { useState } from "react";

const MAX_FILE_SIZE = 5 * 1024 * 1024;

const ALLOWED_TYPES = [
  "application/pdf",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

function ResumeUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const ACCESS_TOKEN = import.meta.env.VITE_ACCESS_TOKEN;

  function handleFileChange(event) {
    const file = event.target.files?.[0] || null;

    setSuccessMessage("");
    setErrorMessage("");

    if (!file) {
      setSelectedFile(null);
      return;
    }

    if (!ALLOWED_TYPES.includes(file.type)) {
      setSelectedFile(null);
      setErrorMessage("Only PDF, DOC, and DOCX files are allowed.");
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setSelectedFile(null);
      setErrorMessage("File size must not exceed 5 MB.");
      return;
    }

    setSelectedFile(file);
  }

  async function handleUpload() {
    if (!selectedFile) {
      setErrorMessage("Please select a resume first.");
      return;
    }

    setLoading(true);
    setSuccessMessage("");
    setErrorMessage("");

    try {
      const urlResponse = await fetch(
        `${API_BASE_URL}/resumes/upload-url`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${ACCESS_TOKEN}`,
          },
          body: JSON.stringify({
            userId: "user_123",
            filename: selectedFile.name,
            contentType: selectedFile.type,
            fileSize: selectedFile.size,
          }),
        }
      );

      const urlData = await urlResponse.json();

      if (!urlResponse.ok) {
        throw new Error(
          urlData.error ||
            urlData.message ||
            "Unable to prepare upload"
        );
      }

      const uploadResponse = await fetch(urlData.uploadUrl, {
        method: "PUT",
        headers: {
          "Content-Type": selectedFile.type,
        },
        body: selectedFile,
      });

      if (!uploadResponse.ok) {
        throw new Error("Resume upload failed");
      }

      setSuccessMessage("Resume uploaded successfully!");
      setSelectedFile(null);
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="resume-upload">
      <h2>Upload Resume</h2>

      <input
        type="file"
        accept=".pdf,.doc,.docx"
        onChange={handleFileChange}
      />

      <button
        type="button"
        onClick={handleUpload}
        disabled={loading || !selectedFile}
      >
        {loading ? "Uploading..." : "Upload Resume"}
      </button>

      {successMessage && (
        <p className="success-message">{successMessage}</p>
      )}

      {errorMessage && (
        <p className="error-message">{errorMessage}</p>
      )}
    </section>
  );
}

export default ResumeUpload;