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

            locations.forEach(loc => {
                const lat = loc.lat;
                const lng = loc.lng;

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
