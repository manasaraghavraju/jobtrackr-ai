import { useState } from "react";

function Applications() {
  const [formData, setFormData] = useState({
    userId: "user_123",
    company: "",
    role: "",
    status: "Applied",
    appliedDate: "",
    jobLink: "",
    notes: "",
  });

  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const ACCESS_TOKEN = import.meta.env.VITE_ACCESS_TOKEN;

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setSuccessMessage("");
    setErrorMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/applications`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${ACCESS_TOKEN}`,
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setSuccessMessage("Application added successfully!");

      setFormData({
        userId: "user_123",
        company: "",
        role: "",
        status: "Applied",
        appliedDate: "",
        jobLink: "",
        notes: "",
      });
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Applications</h1>
      <p>Add and track your job applications.</p>

      {successMessage && <p className="success-message">{successMessage}</p>}
      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <form className="application-form" onSubmit={handleSubmit}>
        <label>Company</label>
        <input
          type="text"
          name="company"
          value={formData.company}
          onChange={handleChange}
          placeholder="Amazon"
          required
        />

        <label>Role</label>
        <input
          type="text"
          name="role"
          value={formData.role}
          onChange={handleChange}
          placeholder="Software Development Engineer"
          required
        />

        <label>Status</label>
        <select name="status" value={formData.status} onChange={handleChange}>
          <option value="Saved">Saved</option>
          <option value="Applied">Applied</option>
          <option value="Online Assessment">Online Assessment</option>
          <option value="Interview">Interview</option>
          <option value="Rejected">Rejected</option>
          <option value="Offer">Offer</option>
          <option value="Accepted">Accepted</option>
        </select>

        <label>Applied Date</label>
        <input
          type="date"
          name="appliedDate"
          value={formData.appliedDate}
          onChange={handleChange}
        />

        <label>Job Link</label>
        <input
          type="text"
          name="jobLink"
          value={formData.jobLink}
          onChange={handleChange}
          placeholder="https://company.com/job"
        />

        <label>Notes</label>
        <textarea
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          placeholder="Any notes about this application"
        />

        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Add Application"}
        </button>
      </form>
    </div>
  );
}

export default Applications;