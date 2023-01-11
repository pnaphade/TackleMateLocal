document.getElementById("file").addEventListener("change", function() {
    var media = URL.createObjectURL(this.files[0]);
    var video = document.getElementById("video");
    var video_msg = document.getElementById("video msg")
    video.src = media;
    video.style.display = "block";
    video.play();
    video_msg.innerHTML = "<strong> Please pause the video at the point when you make contact with the pad. </strong>"

  });

function uploadVideo(form){
    const formData = new FormData(form);

    // if name of video is not set, prompt user to upload
    if(!formData.get("video_file").name) {
        alert("Please select a video to upload")
        return
    }

    if(! (document.getElementById('left').checked && document.getElementById('right'))) {
        alert("Please indicate which shoulder is closest to the camera")
    }

    paused = document.getElementById("video").paused
            ended = document.getElementById("video").ended
            if((!paused) || ended) {
                alert("Please pause the video at the point when you make contact with the pad")
                return
            }

    var upload_status = document.getElementById("upload status")
    var analyze_status = document.getElementById("analyze status")

    // create new post request
    var oReq = new XMLHttpRequest();
    oReq.open("POST", "upload_video", true);

    // handle response of python server
    oReq.onload = function(oEvent) {
        if (oReq.status == 200) {
            upload_status.innerHTML = "Video uploaded!";
            resp = JSON.parse(oReq.responseText)
            console.log(resp)

            // redirect user to get_scores server function
            // note: window.location.href uses GET, but really should
            // be using POST here...

            var side = document.querySelector('input[name="side"]:checked').value;
            timestamp = document.getElementById("video").currentTime
            var side = document.querySelector('input[name="side"]:checked').value;
            score_url = "/get_scores?fn="
            score_url += encodeURIComponent(resp.filename)
            score_url += "&timestamp="
            score_url += encodeURIComponent(timestamp)
            score_url += "&side="
            score_url += encodeURIComponent(side)
            analyze_status.innerHTML = "Analyzing video..."
            window.location.href = score_url;}

        else {
            upload_status.innerHTML = "An error occurred when trying to upload your video. Please try again. <br>";
            }
        };

    // send user's video to python server
    upload_status.innerHTML = "Uploading video...";
    console.log("Uploading video...")
    oReq.send(formData);
}