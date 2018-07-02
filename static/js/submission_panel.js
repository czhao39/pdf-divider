$(document).ready(function() {
    var $submissionContainer = $("#submission-container");
    var $panelBody = $("#submission-panel > .panel-body");
    $("#submission-zoomin-btn").click(function() {
        $submissionContainer.width($submissionContainer.width() * 1.1);
        $panelBody.scrollspy("refresh");
    });
    $("#submission-zoomout-btn").click(function() {
        $submissionContainer.width($submissionContainer.width() / 1.1);
        $panelBody.scrollspy("refresh");
    })
});

