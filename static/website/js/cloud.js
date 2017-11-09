/* Ajax loader */
function ajax_loader(key) {
    if(key == "clear") {
        $(".ajax-loader").remove();
    } else {
        $(".ajax-loader").remove();
        $(key).after("<span class='ajax-loader'></span>");
    }
}
function show_examples(current_element){
    examples_ajax(current_element);
}

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

    var initial_code = '';
    // editor.setValue("");
    // result.setValue("");
    // editor.clearHistory();

    // hide revision submit button initially
    // $("#submit-revision").show()

    /* Code Mirror Controls
    $fullscreen_code = $("#fullscreen-code");

    $fullscreen_code.click(function(e) {
        editor.setOption("fullScreen", !editor.getOption("fullScreen"));
        editor.focus();
        e.preventDefault();
    });

    $fullscreen_result = $("#fullscreen-result");

    $fullscreen_result.click(function(e) {
        result.setOption("fullScreen", !result.getOption("fullScreen"));
        result.focus();
        e.preventDefault();
    });

     * Selectors function
     * Write the queries using .on()
     */
    $("#plot_download").hide();
    /*
    Not needed -
    $(document).on("change", "#categories", function() {
        if ($("#categories").val() == 0) {
            $("#download-book").hide();
            $("#books-wrapper").hide();
            editor.setValue("");
            result.setValue("");
            editor.clearHistory();
            $("#review").hide();
        } else {
            $("#books-wrapper").show();
        }

        $("#books-wrapper").html("");
        $("#chapters-wrapper").html("");
        $("#examples-wrapper").html("");
        $("#contributor").hide();
        $("#revisions-wrapper").html("");

        // hide revision submit button if one selects different category
        // $("#submit-revision").hide()

        if ($("#categories").val()) {
            ajax_loader("#categories");
            Dajaxice.website.books(function(data) {
                Dajax.process(data);
                ajax_loader("clear");
            }, {category_id: $("#categories").val()});
        }
    });

    NOT NEEDED
    $(document).on("change", "#books", function() {
        $("#chapters-wrapper").html("");
        $("#examples-wrapper").html("");
        $("#revisions-wrapper").html("");

        $("#contributor").show();
        $("#download-book").show();

        if ($("#books").val() == 0) {
            $("#chapters-wrapper").hide();
            $("#download-book").hide();
            editor.setValue("");
            result.setValue("");
            editor.clearHistory();
            $("#review").hide();
        } else {
            $("#chapters-wrapper").show();
        }

        // hide revision submit button if one selects different book
        // $("#submit-revision").hide()

        if ($("#books").val()) {
            ajax_loader("#books");
            Dajaxice.website.chapters(function(data) {
                Dajax.process(data);
                ajax_loader("clear");
            }, {book_id: $("#books").val()});
        }
    });
    */

    $(".mmbooks").click( function() {
        editor.setValue("");
        result.setValue("");
        editor.clearHistory();
        ajax_loader(this);
        Dajaxice.website.chapters(function(data) {
            Dajax.process(data);
            ajax_loader("clear");
        }, {book_id: $(this).attr('id')});
    });

    examples_ajax = function(current_element){
        editor.setValue("");
        result.setValue("");
        editor.clearHistory();
        $("#examples-wrapper").html("");
        ajax_loader(current_element);
        Dajaxice.website.examples(function(data) {
            Dajax.process(data);
            ajax_loader("clear");
        }, {chapter_id: $(current_element).attr('id')});
              $('#intro-page').hide(300);
              $('#examples-wrapper').show(300);
  }

    /*
    NOT NEEDED
    $(document).on("change", "#chapters", function() {
        $("#examples-wrapper").html("");
        $("#revisions-wrapper").html("");
        $("#download-chapter").show();

        // hide revision submit button if one selects different chapter
        // $("#submit-revision").hide()

        if ($("#chapters").val() == 0) {
            $("#examples-wrapper").hide();
            $("#download-chapter").hide();
            editor.setValue("");
            result.setValue("");
            editor.clearHistory();
            $("#review").hide();
        } else {
            $("#examples-wrapper").show();
        }

        if ($(this).val()) {
            ajax_loader(this);
            Dajaxice.website.examples(function(data) {
                Dajax.process(data);
                ajax_loader("clear");
            }, {chapter_id: $(this).val()});
        }
    });
    */
    $(document).on("click", ".exmp", function() {
        editor.setValue("");
        document.getElementById($(".exmp_id").attr('id')).className = document.getElementById($(".exmp_id").attr('id')).className.replace( /(?:^|\s)active(?!\S)/g , '' );
        document.getElementById(this.id).className += " active";
        $("#revisions-wrapper").html("");
        $(".download-example").show();
        $('.exmpid').attr('id', this.id);
        $('.exmp_id').attr('id', this.id);
        result.setValue("");

        // hide revision submit button if one selects different example
        // $("#submit-revision").hide()

        if ($(this).attr('id') == 0) {
            $(".download-example").hide();
            editor.setValue("");
            result.setValue("");
            editor.clearHistory();
            $("#review").hide();
        }

        if ($(this).attr('id')) {
            ajax_loader(this);
            Dajaxice.website.revisions(function(data) {
                Dajax.process(data);
                ajax_loader("clear");
                $("#revisions-two").hide()
                $('#revisions option:eq(1)').prop('selected', true)
                ajax_loader('#revisions');
                Dajaxice.website.code(function(data) {
                    editor.setValue(data.code);
                    initial_code = editor.getValue()

                    if (data.review != 0) {
                        $("#review").show();
                        $("#review").attr("href", data.review_url);
                        $("#review").text(data.review + " " + "Review");
                    } else {
                        $("#review").hide();
                    }

                    ajax_loader("clear");
                    $("#submit-revision").show()
                    $("#revisions-two").show()
                }, {commit_sha: $('#revisions').val()});

            }, {example_id: this.id});
        }
    });

    $(document).on("change", "#revisions", function() {
        $("#revisions-two").hide()
        if ($(this).val()) {
            ajax_loader(this);
            Dajaxice.website.code(function(data) {
                editor.setValue(data.code);
                initial_code = editor.getValue()

                if (data.review != 0) {
                    $("#review").show();
                    $("#review").attr("href", data.review_url);
                    $("#review").text(data.review + " " + "Review");
                } else {
                    $("#review").hide();
                }

                ajax_loader("clear");

                // show revision submit button when a revision is loaded
                $("#submit-revision").show()
                $("#revisions-two").show()

            }, {commit_sha: $(this).val()});
        }
    });

    $(document).on("click", "#revisions-diff", function(e) {
        if ($(this).val()) {
            ajax_loader(this);
            var revName = $("#revisions-diff").find(":selected").text();
            Dajaxice.website.diff(function(data) {
                Dajax.process(data.dajax)
                ajax_loader("clear");
                $("#diff-wrapper").lightbox_me({centered: false});
                $("#diff-area").html(diffString(editor.getValue(), data.code2))

                $("#diff-first").html('editor code')
                $("#diff-second").html(revName)
            }, {
                diff_commit_sha: $(this).val(),
                editor_code: editor.getValue(),
            });
            e.preventDefault();
        }
    });


    /* Execute the code */
    $plotbox_wrapper = $("#plotbox-wrapper");
    $plotbox = $("#plotbox");

    $(document).on("click", "#execute", function() {
        $("#execute-inner").html("Executing...");
        ajax_loader("clear");
        var send_data = {
            token: $("[name='csrfmiddlewaretoken']").val(),
            code: editor.getValue(),
            book_id: $(".bks_id").attr("ID") || 0,
            chapter_id: $(".chp_id").attr("ID") || 0,
            example_id: $(".ex_id").attr("ID") || 0

        };
        $.post("/execute-code", send_data,
        function(data){
            $("#execute-inner").html("Execute");
            result.setValue(data.output);

            if(data.plot_path){
                $plot = $("<img>");
                $plot.attr({
                    src: data.plot_path,
                    width: '100%'
                });
                $plotbox.html($plot);
                $plotbox_wrapper.lightbox_me({
                    centered: true
                });
                var dt = new Date().getTime();
                $("#plot_download").show();
                $("#plot_download").attr("download", dt+'.png');
                $("#plot_download").attr("href", data.plot_path);
            }
        });
    });
    /* Download book, chapter, example */
    $(document).on("click", "#download-book", function(e) {
        window.location = "http://scilab.in/download/book/" + $(this).attr('value');
        e.preventDefault();
    });

    $(document).on("click", "#download-chapter", function(e) {
        window.location = "http://scilab.in/download/chapter/" + $(".chp_id").attr('id');
        e.preventDefault();
    });

    $(document).on("click", ".exmpid", function(e) {
      if ($('.exmpid').attr('id')){
        window.location = "http://scilab.in/download/example/" + $('.exmpid').attr('id');
        e.preventDefault();
    }});


    /* Contributor details */
    $(document).on("click", "#contributor", function(e) {
        Dajaxice.website.contributor(function(data) {
            Dajax.process(data);
            $("#databox-wrapper").lightbox_me({
                centered: true
            });
        }, {
            book_id: $("#books").val()
        });
        e.preventDefault();
    });

    $(document).on("click", ".node", function(e) {
        Dajaxice.website.node(function(data) {
            Dajax.process(data);
            $("#databox-wrapper").lightbox_me({
                centered: true
            });
        }, {
            key: $(this).data("key")
        });
        e.preventDefault();
    });

    /* Bug form handling */
    $(document).on("click", "#bug", function(e) {
        Dajaxice.website.bug_form(function(data) {
            Dajax.process(data);
            $("#bug-form-wrapper").lightbox_me({
                centered: false
            });
        });
        e.preventDefault();
    });

    $(document).on("click", "#bug-form-submit", function(e) {
        cat_id = $(".ct_id").attr('id') || 0;
        book_id = $(".bk_id").attr('id') || 0;
        chapter_id = $(".cp_id").attr('id') || 0;
        ex_id = $(".ex_id").attr('id') || 0;
        if (!ex_id) {
            ex_id = "NULL";
        }
        Dajaxice.website.bug_form_submit(Dajax.process, {
            form: $("#bug-form").serialize(true),
            cat_id: cat_id,
            book_id: book_id,
            chapter_id: chapter_id,
            ex_id: ex_id,
        });
        e.preventDefault();
    });

    // $(document).on("click", "#bug-form #id_notify", function() {
    //     $("#id_email_wrapper").toggle(this.checked);
    // });

    // submit revision handling
    $(document).on("click", "#submit-revision", function(e) {
        // if (editor.getValue() == initial_code) {
        //     Dajaxice.website.revision_error(function(data) {
        //         Dajax.process(data);
        //         $("#submit-revision-error-wrapper").lightbox_me({centered: false});
        //     });
        // } else {
            Dajaxice.website.revision_form(function(data) {
                Dajax.process(data);
                $("#submit-revision-wrapper").lightbox_me({centered: false});
            },{code: editor.getValue(),
               initial_code: initial_code});
        // }
        e.preventDefault();
    });

    // onclick callback for revision-submit button click
    $(document).on("click", "#revision-form-submit", function(e) {
        ajax_loader(this);
        Dajaxice.website.revision_form_submit(function(data) {
                Dajax.process(data);
                initial_code = editor.getValue()
            },
            {
                form: $('#revision-form').serialize(true),
                code: editor.getValue(),
            }
        );
        e.preventDefault();
    });

 $(document).on("click", "#close-panel,#plotbox", function(e){

    $("#plotbox, #plotbox-wrapper").trigger('close');

 });

});
