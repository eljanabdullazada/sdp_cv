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
    fileLabel.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : "Choose a file";
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

function startStream() {
    if (!selectedVideo) return;
    const stream = document.getElementById("videoStream");
    stream.src = `/video_feed?filename=${encodeURIComponent(selectedVideo)}`;
    document.getElementById("streamContainer").style.display = "block";
}

function detectBanners() {
    if (!selectedVideo) return alert("No video selected!");

    const detectBtn = document.querySelector("button[onclick='detectBanners()']");
    detectBtn.disabled = true;
    detectBtn.textContent = "Detecting...";

    startStream(); // Show live detection stream while processing

    fetch("/detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: selectedVideo })
    })
    .then(res => res.json())
    .then(data => {
        const video = document.getElementById("videoPlayer");
        video.src = `/processed/${data.processed}`;
        video.hidden = false;
        video.play();
        document.getElementById("streamContainer").style.display = "none"; // Hide stream after processing
    })
    .catch(() => alert("Detection failed!"))
    .finally(() => {
        detectBtn.disabled = false;
        detectBtn.textContent = "Detect Banners";
    });
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

    // Tell server to delete the video file from the server
    fetch("/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename: selectedVideo })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Video deleted from server.");
            updateVideoList();  // Refresh the video list
            stopVideo();  // Stop video if it was playing
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(err => {
        alert("Error deleting video from server.");
        console.error("Delete error:", err);
    });
}



// function detectBanners() {
//     if (!selectedVideo) return alert("No video selected!");
//
//     const detectBtn = document.querySelector("button[onclick='detectBanners()']");
//     detectBtn.disabled = true;
//     detectBtn.textContent = "Detecting...";
//
//     // Show loading indicator
//     document.getElementById("loading").style.display = "block";
//
//     fetch("/detect", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ filename: selectedVideo })
//     })
//     .then(res => res.json())
//     .then(data => {
//         const video = document.getElementById("videoPlayer");
//         video.src = `/processed/${data.processed}`;
//         video.hidden = false;
//         video.play();
//     })
//     .catch(() => alert("Detection failed!"))
//     .finally(() => {
//         detectBtn.disabled = false;
//         detectBtn.textContent = "Detect Banners";
//         // Hide loading indicator
//         document.getElementById("loading").style.display = "none";
//     });
// }


window.addEventListener("load", () => {
    // Fetch existing videos from the server (in case localStorage is empty)
    fetch('/videos')
        .then(res => res.json())
        .then(existingVideos => {
            uploadedVideos = existingVideos;  // Update the uploadedVideos array with the server response
            selectedVideo = localStorage.getItem("selectedVideo") || "";
            updateVideoList();

            if (selectedVideo && uploadedVideos.includes(selectedVideo)) {
                const video = document.getElementById("videoPlayer");
                video.src = `/video/${selectedVideo}`;
            }
        })
        .catch(err => {
            console.error('Error fetching videos from server:', err);
        });
});

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

function stopDetection() {
    fetch('/stop_detection', { method: 'POST' })
        .then(() => {
            document.getElementById("streamContainer").style.display = "none";
            document.getElementById("videoStream").src = ""; // Kill stream
            alert("Detection stopped.");
        })
        .catch(err => {
            console.error("Error stopping detection:", err);
        });
}
