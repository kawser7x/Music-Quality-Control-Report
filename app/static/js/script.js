document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById("audioFile");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const loading = document.getElementById("loading");
    const resultSection = document.getElementById("resultSection");
    const resultText = document.getElementById("resultText");

    loading.classList.remove("hidden");

    try {
        const response = await axios.post("/upload/audio/", formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });

        loading.classList.add("hidden");
        resultSection.classList.remove("hidden");

        resultText.innerText = response.data.result || "✅ QC Passed. But no result returned.";

    } catch (error) {
        loading.classList.add("hidden");
        alert("QC failed: " + (error.response?.data?.detail || error.message));
    }
});

// 📋 Copy to Clipboard
document.getElementById("copyButton").addEventListener("click", function () {
    const resultText = document.getElementById("resultText").innerText;
    navigator.clipboard.writeText(resultText)
        .then(() => alert("✅ QC report copied to clipboard!"))
        .catch(() => alert("❌ Failed to copy QC report."));
});

// 📄 Download as PDF
document.getElementById("downloadPdf").addEventListener("click", function () {
    const { jsPDF } = window.jspdf || {};
    if (!jsPDF) {
        alert("PDF library not loaded.");
        return;
    }

    const doc = new jsPDF();
    const text = document.getElementById("resultText").innerText;
    const lines = doc.splitTextToSize(text, 180);

    doc.setFontSize(12);
    doc.text("🎧 TrackVerify - Music QC Report", 10, 10);
    doc.text(lines, 10, 20);
    doc.save("trackverify_qc_report.pdf");
});