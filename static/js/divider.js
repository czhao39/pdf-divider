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
    $divider.click(deleteDivider)
    var $label = $("<div class='divider-label'></div>")
    $label.css("top", yProp*100 + "%");
    $label.click(deleteDivider)
    dividers.push({
        yProp: yProp,
        divider: $divider,
        label: $label
    });
    updateIndices();
    $submissionContainer.append($divider);
    $submissionContainer.append($label);
}

/* Updates divider indices based on Y position, and accordingly updates labels */
function updateIndices() {
    dividers.sort(function(a, b) {
        return a.yProp - b.yProp;
    });
    for (var i = 0; i < dividers.length; i++) {
        dividers[i].divider.data("index", i);
        dividers[i].label.data("index", i);
        dividers[i].label.text("Part " + (i + 1));
    }
}

function deleteDivider() {
    var index = $(this).data("index");
    console.log(index);
    dividers[index].divider.remove();
    dividers[index].label.remove();
    dividers.splice(index, 1);
    updateIndices();
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
