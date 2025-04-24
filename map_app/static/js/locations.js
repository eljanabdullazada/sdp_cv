document.addEventListener("DOMContentLoaded", function () {
    if (!VIDEO_ID) return;

    fetch(`/locations_data/${VIDEO_ID}`)
        .then(response => response.json())
        .then(locations => {
            if (locations.length === 0) {
                document.getElementById('error-message').style.display = 'block';
                document.getElementById('error-message').textContent = "No locations found for the given video ID.";
                return;
            }

            document.getElementById('error-message').style.display = 'none';

            const map = L.map('map').setView([40.4093, 49.8671], 12);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            const customCoords = {
    "banner_30_best.jpg": [40.393861, 49.846307],
    "banner_28_best.jpg": [40.374091, 49.846669],
    "banner_1_best.jpg": [40.404734, 49.836355],
    "banner_2_best.jpg": [40.404975, 49.836737],
    "banner_19_best.jpg": [40.404856, 49.836315],
    "banner_3_best.jpg": [40.404844, 49.836313]
};


            locations.forEach(loc => {
                const imageName = loc.image_link.split("/").pop();
                let lat = loc.lat;
                let lng = loc.lng;

                if (customCoords[imageName]) {
                    [lat, lng] = customCoords[imageName];
                }

                const marker = L.marker([lat, lng]).addTo(map);

                marker.on('click', function () {
                    fetch(`/location/${loc.id}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.image_link) {
                                const imageUrl = "/" + data.image_link;
                                document.getElementById('imageDisplay').innerHTML =
                                    `<img src="${imageUrl}" alt="Location Image" style="width:100%; height:100%;">`;
                            } else {
                                alert('Image not found');
                            }
                        })
                        .catch(error => console.error('Error fetching image:', error));
                });
            });

            window.addEventListener('resize', function () {
                map.invalidateSize();
            });
        })
        .catch(error => {
            console.error('Error fetching locations:', error);
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('error-message').textContent = "An error occurred while fetching locations.";
        });
});
