var dividers = [];
var $submissionContainer;

$(document).ready(function() {
    $submissionContainer = $("#submission-container");

    $("#submission-img").click(function(e) {
        var $this = $(this);
        var clickY = e.pageY - $this.offset().top;
        var clickYProp = clickY / $this.height();
        addDivider(clickYProp);
        console.log(getDividerYs());
    });
});

function addDivider(yProp) {
    var $divider = $("<hr class='divider'>");
    $divider.css("top", yProp*100 + "%");
    var $label = $("<div class='divider-label'></div>")
    $label.css("top", yProp*100 + "%");
    dividers.push({
        yProp: yProp,
        divider: $divider,
        label: $label
    });
    updateLabels();
    $submissionContainer.append($divider);
    $submissionContainer.append($label);
}

function updateLabels() {
    dividers.sort(function(a, b) {
        return a.yProp - b.yProp;
    });
    for (var i = 0; i < dividers.length; i++) {
        dividers[i].label.text("Part " + (i + 1));
    }
}

function getDividerYs() {
    dividerYs = [];
    for (var i = 0; i < dividers.length; i++) {
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
        success: function(data) {
            alert("Saved dividers.");
            window.location.href = "/divider_display/" + data.submission_id;
        },
        error: function() {
            alert("An error occurred.");
        }
    });
}
