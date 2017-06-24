$(document).ready(function() {

	var reviewEditor = CodeMirror.fromTextArea(document.getElementById("review-code"), {
        lineNumbers: true,
        lineWrapping: true,
        theme: "monokai",
        readOnly: true,
        extraKeys: {
           "F11": function(cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
           },
           "Esc": function(cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
           }
         }
    });

    var reviewResult = CodeMirror.fromTextArea(document.getElementById("review-result"), {
        lineWrapping: true,
        theme: "monokai",
        readOnly: true,
        extraKeys: {
           "F11": function(cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
           },
           "Esc": function(cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
           }
         }
    });

    /* Code Mirror Controls */
    $fullscreen_code = $("#review-fullscreen-code");
    $toggle_code = $("#review-toggle-code");

    $fullscreen_code.click(function(e) {
        reviewEditor.setOption("fullScreen", !reviewEditor.getOption("fullScreen"));
        reviewEditor.focus();
        e.preventDefault();
    });

    $toggle_code.click(function(e) {
        if(reviewEditor.getOption("theme") == "monokai") {
            reviewEditor.setOption("theme", "default");
        } else{
            reviewEditor.setOption("theme", "monokai");
        }
        e.preventDefault();
    });

    $fullscreen_result = $("#review-fullscreen-result");
    $toggle_result = $("#review-toggle-result");

    $fullscreen_result.click(function(e) {
        reviewResult.setOption("fullScreen", !reviewResult.getOption("fullScreen"));
        reviewResult.focus();
        e.preventDefault();
    });

    $toggle_result.click(function(e) {
        if(reviewResult.getOption("theme") == "monokai") {
            reviewResult.setOption("theme", "default");
        } else{
            reviewResult.setOption("theme", "monokai");
        }
        e.preventDefault();
    });

     /* Ajax loader */
    function ajax_loader(key) {
        if(key == "clear") {
            $(".ajax-loader").remove();
        } else {
            $(".ajax-loader").remove();
            $(key).after("<span class='ajax-loader'></span>");
        }
    }
	
    //  -----------------------------------------------------

    // callback when revision selection changes
	$(document).on("change", "#review-revisions", function() {
		ajax_loader(this);
		Dajaxice.website.review_revision(function(data) {
            reviewEditor.setValue(data.code)
            ajax_loader("clear");
        }, {revision_id: $(this).val()});
	});

    // callback on pressing push button
    $(document).on("click", "#push", function() {
        ajax_loader(this)
        Dajaxice.website.push_revision(function(data) {
            Dajax.process(data);
            ajax_loader("clear");
        }, 
        {
            code: reviewEditor.getValue(),
        }
        );
    });
});