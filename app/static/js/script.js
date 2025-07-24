document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const fileInput = document.getElementById("audioFile");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    document.getElementById("loading").classList.remove("hidden");

    try {
        const response = await axios.post("/upload/audio/", formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });

        document.getElementById("loading").classList.add("hidden");
        document.getElementById("resultSection").classList.remove("hidden");
        document.getElementById("resultText").innerText = response.data.result;

    } catch (error) {
        alert("QC failed: " + (error.response?.data?.detail || error.message));
        document.getElementById("loading").classList.add("hidden");
    }
});

document.getElementById("copyButton").addEventListener("click", () => {
    const resultText = document.getElementById("resultText").innerText;
    navigator.clipboard.writeText(resultText).then(() => {
        alert("Copied!");
    });
});