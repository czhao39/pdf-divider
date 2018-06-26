var dividers = [];

$(document).ready(function() {
    var $submissionContainer = $("#submission-container");

    $("#submission-img").click(function(e) {
        var $this = $(this);
        var clickY = e.pageY - $this.offset().top;
        var clickYProp = clickY / $this.height();
        console.log(clickYProp);

        var $divider = $("<hr class='divider'>");
        $divider.yProp = clickYProp;
        $divider.css("top", clickYProp*100 + "%");
        dividers.push($divider);
        $submissionContainer.append($divider);
        console.log(getDividerYs());
    });
});

function getDividerYs() {
    dividerYs = [];
    for (i = 0; i < dividers.length; i++) {
        dividerYs.push(dividers[i].yProp);
    }
    return dividerYs;
}

function submit() {
    var data = {
        "dividerYs": getDividerYs()
    };
    $.ajax({
        url: "/submit_dividers",
        method: "POST",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify(data),
        dataType: "text",
        success: function() {
            alert("Saved dividers.");
            window.location.href = "/divider_display"
        },
        error: function() {
            alert("An error occurred.");
        }
    });
}
