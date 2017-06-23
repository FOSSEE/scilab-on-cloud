$(document).ready(function() {
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        lineNumbers: true,
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

    var result = CodeMirror.fromTextArea(document.getElementById("result"), {
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

    var initial_code = '';

    // hide revision submit button initially
    $("#submit-revision").hide()

    /* Code Mirror Controls */
    $fullscreen_code = $("#fullscreen-code");
    $toggle_code = $("#toggle-code");

    $fullscreen_code.click(function(e) {
        editor.setOption("fullScreen", !editor.getOption("fullScreen"));
        editor.focus();
        e.preventDefault();
    });

    $toggle_code.click(function(e) {
        if(editor.getOption("theme") == "monokai") {
            editor.setOption("theme", "default");
        } else{
            editor.setOption("theme", "monokai");
        }
        e.preventDefault();
    });

    $fullscreen_result = $("#fullscreen-result");
    $toggle_result = $("#toggle-result");

    $fullscreen_result.click(function(e) {
        result.setOption("fullScreen", !result.getOption("fullScreen"));
        result.focus();
        e.preventDefault();
    });

    $toggle_result.click(function(e) {
        if(result.getOption("theme") == "monokai") {
            result.setOption("theme", "default");
        } else{
            result.setOption("theme", "monokai");
        }
        e.preventDefault();
    });

    /* 
     * Selectors function 
     * Write the queries using .on()
    */
    $(document).on("change", "#categories", function() {
        $("#books-wrapper").html("");
        $("#chapters-wrapper").html("");
        $("#examples-wrapper").html("");
        $("#revisions-wrapper").html("");
        $("#contributor").hide();

        // hide revision submit button if one selects different category
        $("#submit-revision").hide()

        ajax_loader(this);
        Dajaxice.website.books(function(data) {
            Dajax.process(data);
            ajax_loader("clear");
        }, {category_id: $(this).val()});
    });

    $(document).on("change", "#books", function() {
        $("#chapters-wrapper").html("");
        $("#examples-wrapper").html("");
        $("#revisions-wrapper").html("");
        $("#contributor").show();
        $("#download-book").show();

        // hide revision submit button if one selects different book
        $("#submit-revision").hide()

        ajax_loader(this);
        Dajaxice.website.chapters(function(data) { 
            Dajax.process(data);
            ajax_loader("clear");
        }, {book_id: $(this).val()});
    });

    $(document).on("change", "#chapters", function() {
        $("#examples-wrapper").html("");
        $("#revisions-wrapper").html("");
        $("#download-chapter").show();

        // hide revision submit button if one selects different chapter
        $("#submit-revision").hide()

        ajax_loader(this);
        Dajaxice.website.examples(function(data) { 
            Dajax.process(data);
            ajax_loader("clear");
        }, {chapter_id: $(this).val()});
    });

    $(document).on("change", "#examples", function() {
        $("#revisions-wrapper").html("");
        $("#download-example").show();

        // hide revision submit button if one selects different example
        $("#submit-revision").hide()

        ajax_loader(this);
        Dajaxice.website.revisions(function(data) { 
            Dajax.process(data);
            ajax_loader("clear");
        }, {example_id: $(this).val()});
    });

    $(document).on("change", "#revisions", function() {
        
        ajax_loader(this);
        Dajaxice.website.code(function(data) {
            editor.setValue(data.code);
            initial_code = editor.getValue()
            ajax_loader("clear");

            // show revision submit button when a revision is loaded
            $("#submit-revision").show()

        }, {commit_sha: $(this).val()});
    });

    /* Execute the code */
    $plotbox_wrapper  = $("#plotbox-wrapper");
    $plotbox = $("#plotbox");

    $(document).on("click", "#execute", function() {
        $("#execute-inner").html("Executing...");
        Dajaxice.website.execute(function(data) {
            $("#execute-inner").html("Execute");
            result.setValue(data.output);
            if(data.plot_path) {
                $plot = $("<img>");
                $plot.attr({
                    src: data.plot_path,
                    width: 400
                });
                $plotbox.html($plot);
                $plotbox_wrapper.lightbox_me({centered: true});
            }
        }, {
            token: $("[name='csrfmiddlewaretoken']").val(),
            code: editor.getValue(),
            book_id: $("#books").val() || 0,
            chapter_id: $("#chapters").val() || 0,
            example_id: $("#examples").val() || 0
        });
    });

    /* Download book, chapter, example */
    $(document).on("click", "#download-book", function(e) {
        window.location = "http://scilab.in/download/book/" + $("#books").val();
        e.preventDefault();
    });

    $(document).on("click", "#download-chapter", function(e) {
        window.location = "http://scilab.in/download/chapter/" + $("#chapters").val();
        e.preventDefault();
    });

    $(document).on("click", "#download-example", function(e) {
        window.location = "http://scilab.in/download/example/" + $("#examples").val();
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

    /* Contributor details */
    $(document).on("click", "#contributor", function(e) {
        Dajaxice.website.contributor(function(data) {
            Dajax.process(data);
            $("#databox-wrapper").lightbox_me({centered: true});
        }, {book_id: $("#books").val()});
        e.preventDefault();
    });

    $(document).on("click", ".node", function(e){
        Dajaxice.website.node(function(data) {
            Dajax.process(data);
            $("#databox-wrapper").lightbox_me({centered: true});
        }, {key: $(this).data("key")});
        e.preventDefault();
    });

    
    /* Bug form handling */
    $(document).on("click", "#bug", function(e) {
        Dajaxice.website.bug_form(function(data){
            Dajax.process(data);
            $("#bug-form-wrapper").lightbox_me({centered: false});
        });
        e.preventDefault();
    });

    $(document).on("click", "#bug-form-submit", function(e){
        Dajaxice.website.bug_form_submit(Dajax.process, {form: $("#bug-form").serialize(true)});
        e.preventDefault();
    });

    $(document).on("click", "#bug-form #id_notify", function() {
        $("#id_email_wrapper").toggle(this.checked);
    });

    // submit revision handling
    $(document).on("click", "#submit-revision", function(e) {
        if (editor.getValue() == initial_code) {
            Dajaxice.website.revision_error(function(data) {
                Dajax.process(data);
                $("#submit-revision-error-wrapper").lightbox_me({centered: false});
            });
        } else {
            Dajaxice.website.revision_form(function(data) {
                Dajax.process(data);
                $("#submit-revision-wrapper").lightbox_me({centered: false});
            });
        }
        e.preventDefault();
    });

    // onclick callback for revision-submit button click
    $(document).on("click", "#revision-form-submit", function(e) {
        ajax_loader(this);
        Dajaxice.website.revision_form_submit(
            Dajax.process, {
                form: $('#revision-form').serialize(true),
                code: editor.getValue(),
            }
        );
        e.preventDefault();
    });
});












