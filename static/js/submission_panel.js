$(document).ready(function() {
    var $submissionContainer = $("#submission-container");
    $("#submission-zoomin-btn").click(function() {
        $submissionContainer.width($submissionContainer.width() * 1.1);
    });
    $("#submission-zoomout-btn").click(function() {
        $submissionContainer.width($submissionContainer.width() / 1.1);
    })
});

