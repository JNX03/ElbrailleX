console.log('hello world');
const video = document.getElementById('video-element');
const image = document.getElementById('img-element');


startVideo();
video.play();

function startVideo() {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
        const { height, width } = stream.getTracks()[0].getSettings();
        console.log("phase1")

        // Delay photo capture by 5 seconds
        setTimeout(() => {
            const track = stream.getVideoTracks()[0];
            const imageCapture = new ImageCapture(track);
            console.log(imageCapture);

            imageCapture.takePhoto().then(blob => {
                console.log("took photo:", blob);
                const img = new Image(width, height);
                img.src = URL.createObjectURL(blob);
                // image.append(img);

                video.classList.add('not-visible');

                blob.arrayBuffer().then((buf) => {
                    fetch("/process_photo", {
                        body: buf,
                        headers: {
                            "Content-Type": blob.type
                        },
                        method: "POST"
                    }).then((response) => {
                        console.log(response);
                        nextPage();
                        return response.json();
                    }).then(console.log);
                });
            }).catch(error => {
                console.log('takePhoto() error: ', error);
            });
        }, 5000); // 5000 milliseconds = 5 seconds
    })
    .catch(error => {
        console.log("Something went wrong!", error);
    });
}


function nextPage() {
    fetch("/home/")
        .then((response) => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then((html) => {
            document.open();
            document.write(html);
            document.close();
        })
        .catch((error) => {
            console.log("Error fetching the next page:", error);
        });
}