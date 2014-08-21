$(document).ready(function() {
    /* Code Mirror Controls */
    $fullscreen_code = $("#fullscreen-code");
    $toggle_code = $("#toggle-code");

    $fullscreen_code.click(function(e) {
        editor.setOption("fullScreen", !editor.getOption("fullScreen"));
        editor.focus();
    });
    $toggle_code.click(function() {
        if(editor.getOption("theme") == "monokai") {
            editor.setOption("theme", "default");
        } else{
            editor.setOption("theme", "monokai");
        }
    });

    $fullscreen_result = $("#fullscreen-result");
    $toggle_result = $("#toggle-result");

    $fullscreen_result.click(function(e) {
        result.setOption("fullScreen", !result.getOption("fullScreen"));
        result.focus();
    });
    $toggle_result.click(function() {
        if(result.getOption("theme") == "monokai") {
            result.setOption("theme", "default");
        } else{
            result.setOption("theme", "monokai");
        }
    });

    /* 
     * Selectors function 
     * Write the queries using live
    */
    $("#categories").change(function() {
        $("#books-wrapper").html("");
        $("#chapters-wrapper").html("");
        $("#examples-wrapper").html("");

        $.ajax({
            url: "/ajax-books/",
            type: "POST",
            data: {
                category_id: $(this).val()
            },
            dataType: "html",
            success: function(data) {
                $("#books-wrapper").html(data);
            }
        });
    });

    $(document).on("change", "#books", function(){
        $("#chapters-wrapper").html("");
        $("#examples-wrapper").html("");

        $.ajax({
            url: "/ajax-chapters/",
            type: "POST",
            data: {
                book_id: $("#books").val()
            },
            dataType: "html",
            success: function(data) {
                $("#chapters-wrapper").html(data);
            }
        });
    });

    $(document).on("change", "#chapters", function(){
        $("#examples-wrapper").html("");
        $.ajax({
            url: "/ajax-examples/",
            type: "POST",
            data: {
                chapter_id: $("#chapters").val()
            },
            dataType: "html",
            success: function(data) {
                $("#examples-wrapper").html(data);
            }
        });
    });

    $(document).on("change", "#examples", function(){
        $.ajax({
            url: "/ajax-code/",
            type: "POST",
            data: {
                example_id: $("#examples").val()
            },
            dataType: "html",
            success: function(data) {
                editor.setValue(data);
            }
        });
    });

    /* Execute the code */
    $lightbox_wrapper  = $("#lightbox-me-wrapper");
    $lightbox = $("#lightbox-me");
    $("#execute").click(function() {
        var csrfmiddlewaretoken = $("[name='csrfmiddlewaretoken']").val();
        var code = editor.getValue();
        $("body").css("cursor", "wait");
        $.ajax({
            url:"/ajax-execute/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                code: code,
                example_id: $("#examples").val()
            },
            dataType: "text",
            success: function(data) {
                $("body").css("cursor", "auto");
                $data = $(data);
                var output = $data.find("#output").html();
                var plot = $data.find("#plot").html();
                result.setValue(output);
                if(plot) {
                    $lightbox.html(plot);
                    $lightbox_wrapper.lightbox_me({centered: true});
                }
            }
        });
    });

});
