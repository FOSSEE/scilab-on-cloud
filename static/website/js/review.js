$(document).ready(function() {

	// var reviewEditor = CodeMirror.fromTextArea(document.getElementById("review-code"), {
 //        lineNumbers: true,
 //        lineWrapping: true,
 //        theme: "default",
 //        extraKeys: {
 //           "F11": function(cm) {
 //            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
 //           },
 //           "Esc": function(cm) {
 //            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
 //           }
 //         }
 //    });

    var reviewResult = CodeMirror.fromTextArea(document.getElementById("result"), {
        lineWrapping: true,
        theme: "default",
        extraKeys: {
           "F11": function(cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
           },
           "Esc": function(cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
           }
         }
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
	
	$(document).on("change", "#review-revisions", function() {
		ajax_loader(this);
		Dajaxice.website.revision_check(function(data) {
            $("#review-code").val(data.code)
            ajax_loader("clear");
        }, {revision_id: $(this).val()});
	});

});