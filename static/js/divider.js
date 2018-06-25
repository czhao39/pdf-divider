$(document).ready(function() {
    var $submissionContainer = $("#submission-container");

    $("#submission-img").click(function(e) {
        var $this = $(this);
        var clickY = e.pageY - $this.offset().top;
        var clickYProp = clickY / $this.height();
        console.log(clickYProp);

        var $divider = $("<hr class='divider'>");
        $submissionContainer.append($divider);
        $divider.css("top", clickYProp*100 + "%");
    });
});
