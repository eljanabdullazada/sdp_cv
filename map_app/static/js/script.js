let uploadedVideos = JSON.parse(localStorage.getItem("uploadedVideos")) || [];
let selectedVideo = "";

function uploadVideo() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("video", file);

    fetch("/upload", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            uploadedVideos.push(data.filename);
            localStorage.setItem("uploadedVideos", JSON.stringify(uploadedVideos));
            selectedVideo = data.filename;
            localStorage.setItem("selectedVideo", selectedVideo);
            updateVideoList();
            alert("Upload successful!");
        });
}

function updateFileName() {
    const fileInput = document.getElementById("fileInput");
    const fileLabel = document.getElementById("fileLabel");

    // If a file is selected, display its name on the label
    if (fileInput.files.length > 0) {
        fileLabel.textContent = fileInput.files[0].name;
    } else {
        fileLabel.textContent = "Choose a file";
    }
}

function updateVideoList() {
    const dropdown = document.getElementById("videoList");
    dropdown.innerHTML = "";

    uploadedVideos.forEach(filename => {
        const option = document.createElement("option");
        option.value = filename;
        option.textContent = filename;
        if (filename === selectedVideo) option.selected = true;
        dropdown.appendChild(option);
    });
}

function selectVideo() {
    const dropdown = document.getElementById("videoList");
    selectedVideo = dropdown.value;
    localStorage.setItem("selectedVideo", selectedVideo);
}

function playVideo() {
    if (!selectedVideo) return alert("Select a video first!");
    const video = document.getElementById("videoPlayer");
    video.src = `/video/${selectedVideo}`;
    video.hidden = false;
    video.play();
}

function stopVideo() {
    const video = document.getElementById("videoPlayer");
    video.pause();
    video.hidden = true;
}

function detectBanners() {
    if (!selectedVideo) return alert("No video selected!");
    fetch("/detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: selectedVideo })
    }).then(() => alert("Detection complete!"));
}

function showLocations() {
    if (!selectedVideo) return alert("No video selected!");
    window.location.href = `/locations?video=${encodeURIComponent(selectedVideo)}`;
}

function deleteVideo() {
    if (!selectedVideo) return alert("No video selected!");

    const confirmDelete = confirm(`Are you sure you want to delete "${selectedVideo}"?`);
    if (!confirmDelete) return;

    // Remove from uploadedVideos array
    uploadedVideos = uploadedVideos.filter(video => video !== selectedVideo);

    // Update localStorage
    localStorage.setItem("uploadedVideos", JSON.stringify(uploadedVideos));

    // Remove selectedVideo from localStorage if it was the deleted one
    if (uploadedVideos.length > 0) {
        selectedVideo = uploadedVideos[0];
    } else {
        selectedVideo = "";
    }
    localStorage.setItem("selectedVideo", selectedVideo);

    // Optionally: tell server to delete it (if implemented on backend)
    fetch("/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: selectedVideo })
    });

    updateVideoList();
    stopVideo();
    alert("Video deleted.");
}


window.addEventListener("load", () => {
    uploadedVideos = JSON.parse(localStorage.getItem("uploadedVideos")) || [];
    selectedVideo = localStorage.getItem("selectedVideo") || "";
    updateVideoList();

    if (selectedVideo) {
        const video = document.getElementById("videoPlayer");
        video.src = `/video/${selectedVideo}`;
    }
});
