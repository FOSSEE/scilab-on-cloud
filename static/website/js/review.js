$(document).ready(function() {

    var reviewEditor = CodeMirror.fromTextArea(document.getElementById(
        "review-code"), {
        lineNumbers: true,
        lineWrapping: true,
        theme: "monokai",
        readOnly: true,
        extraKeys: {
            "F11": function(cm) {
                cm.setOption("fullScreen", !cm.getOption(
                    "fullScreen"));
            },
            "Esc": function(cm) {
                if (cm.getOption("fullScreen")) cm
                    .setOption("fullScreen",
                        false);
            }
        }
    });

    var reviewResult = CodeMirror.fromTextArea(document.getElementById(
        "review-result"), {
        lineWrapping: true,
        theme: "monokai",
        readOnly: true,
        extraKeys: {
            "F11": function(cm) {
                cm.setOption("fullScreen", !cm.getOption(
                    "fullScreen"));
            },
            "Esc": function(cm) {
                if (cm.getOption("fullScreen")) cm
                    .setOption("fullScreen",
                        false);
            }
        }
    });

    /* Code Mirror Controls */
    $fullscreen_code = $("#review-fullscreen-code");
    $toggle_code = $("#review-toggle-code");

    $fullscreen_code.click(function(e) {
        reviewEditor.setOption("fullScreen", !
            reviewEditor.getOption("fullScreen"));
        reviewEditor.focus();
        e.preventDefault();
    });

    $toggle_code.click(function(e) {
        if (reviewEditor.getOption("theme") ==
            "monokai") {
            reviewEditor.setOption("theme", "default");
        } else {
            reviewEditor.setOption("theme", "monokai");
        }
        e.preventDefault();
    });

    $fullscreen_result = $("#review-fullscreen-result");
    $toggle_result = $("#review-toggle-result");

    $fullscreen_result.click(function(e) {
        reviewResult.setOption("fullScreen", !
            reviewResult.getOption("fullScreen"));
        reviewResult.focus();
        e.preventDefault();
    });

    $toggle_result.click(function(e) {
        if (reviewResult.getOption("theme") ==
            "monokai") {
            reviewResult.setOption("theme", "default");
        } else {
            reviewResult.setOption("theme", "monokai");
        }
        e.preventDefault();
    });
    $(document).on("click", "#execute-revision", function() {
        $("#execute-inner").html("Executing...");
        console.log(reviewEditor.getValue());

        var send_data = {
            token: $(
                "[name='csrfmiddlewaretoken']"
            ).val(),
            code: reviewEditor.getValue(),
            book_id: $("#books").val() || 0,
            chapter_id: $("#chapters").val() || 0,
            example_id: $("#examples").val() || 0
        };
        $.post("/execute-code", send_data,
            function(data) {
                $("#execute-inner").html(
                    "Execute");
                reviewResult.setValue(data.output);

                if (data.plot_path) {
                    $plot = $("<img>");
                    $plot.attr({
                        src: data.plot_path,
                        width: '90%'
                    });
                    $plotbox.html($plot);
                    $plotbox_wrapper.lightbox_me({
                        centered: true
                    });
                    var dt = $(
                        "#examples option:selected"
                    ).text();
                    $("#plot_download").show();
                    $("#plot_download").attr(
                        "download", dt +
                        '.png');
                    $("#plot_download").attr(
                        "href", data.plot_path
                    );
                }
            });
    });

    /* Ajax loader */
    function ajax_loader(key) {
        if (key == "clear") {
            $(".ajax-loader").remove();
        } else {
            $(".ajax-loader").remove();
            $(key).after("<span class='ajax-loader'></span>");
        }
    }

    $("#review-control-buttons").hide()

    //  -----------------------------------------------------

    // callback when revision selection changes
    $(document).on("change", "#review-revisions", function() {

        $("#category").html("")
        $("#book").html("")
        $("#chapter").html("")
        $("#example").html("")
        $("#commit-message").html("")

        $("#review-control-buttons").hide()
        reviewEditor.setValue("")
        reviewResult.setValue("")

        if ($(this).val()) {
            ajax_loader(this);
            $.ajax({
                url: 'get_review_revision/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    revision_id: $(this).val()
                },
                success: function(data) {
                    reviewEditor.setValue(
                        data.code)
                    console.log(data)
                    $("#category").html(
                        `<span><strong>Category: </strong></span>` +
                        data.category
                    )
                    $("#book").html(
                        `<span><strong>Textbook: </strong></span>` +
                        data.book.book
                    )
                    $("#chapter").html(
                        `<span><strong>Chapter: </strong></span>` +
                        data.chapter.name
                    )
                    $("#example").html(
                        `<span><strong>Example: </strong></span>` +
                        data.example.caption
                    )
                    $("#commit-message").html(
                        `<span><strong>Commit Message: </strong></span>` +
                        data.revision
                        .commit_message
                    )

                    $(
                        "#review-control-buttons"
                    ).show()

                    ajax_loader("clear");
                }
            });
        }
    });

    // callback on pressing push button
    $(document).on("click", "#push", function() {
        $(this).html("pushing..")

        $.ajax({
            url: 'get_push_revision/',
            dataType: 'JSON',
            type: 'GET',
            data: {
                code: reviewEditor.getValue(),
            },
            success: function(data) {
                $(this).html(
                    'Push revision')
                alert(data);
                location.reload();
            }
        });
    });

    // callback on pressing remove button
    $(document).on("click", "#remove", function() {
        $(this).html("removing..")

        $.ajax({
            url: 'get_remove_revision/',
            dataType: 'JSON',
            type: 'GET',
            data: {},
            success: function(data) {
                $(this).html(
                    'Remove revision'
                );
                alert(data);
                location.reload();
            }
        });
    });
});
