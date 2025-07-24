document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById("audioFile");
    const file = fileInput.files[0];
    if (!file) return alert("Please select a file.");

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("loading").classList.remove("hidden");

    try {
        const response = await fetch("/upload-audio", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        document.getElementById("loading").classList.add("hidden");

        const resultSection = document.getElementById("resultSection");
        const resultText = document.getElementById("resultText");

        resultText.innerText = data.result;
        resultSection.classList.remove("hidden");
    } catch (err) {
        document.getElementById("loading").classList.add("hidden");
        alert("❌ Error occurred while uploading the file.");
        console.error(err);
    }
});

// 📋 Copy Report Button
document.getElementById("copyButton").addEventListener("click", () => {
    const result = document.getElementById("resultText").innerText;
    navigator.clipboard.writeText(result).then(() => {
        alert("✅ Report copied to clipboard.");
    });
});

// 📄 Download PDF Button
document.getElementById("downloadPdf").addEventListener("click", async () => {
    const result = document.getElementById("resultText").innerText;

    const response = await fetch("/generate-pdf", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content: result })
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "TrackVerify_QC_Report.pdf";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } else {
        alert("❌ Failed to generate PDF.");
    }
});