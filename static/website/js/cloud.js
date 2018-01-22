/* Ajax loader */
function ajax_loader(key) {
    if (key == "clear") {
        $(".ajax-loader").remove();
    } else {
        $(".ajax-loader").remove();
        $(key).after("<span class='ajax-loader'></span>");
    }
}

$(document).ready(function() {
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        lineNumbers: true,
        lineWrapping: true,
        theme: "monokai",
        extraKeys: {
            "F11": function(cm) {
                cm.setOption("fullScreen", !cm.getOption(
                    "fullScreen"));
            },
            "Esc": function(cm) {
                if (cm.getOption("fullScreen")) cm.setOption(
                    "fullScreen", false);
            }
        }
    });

    var result = CodeMirror.fromTextArea(document.getElementById(
        "result"), {
        lineWrapping: true,
        theme: "monokai",
        readOnly: true,
        extraKeys: {
            "F11": function(cm) {
                cm.setOption("fullScreen", !cm.getOption(
                    "fullScreen"));
            },
            "Esc": function(cm) {
                if (cm.getOption("fullScreen")) cm.setOption(
                    "fullScreen", false);
            }
        }
    });

    var initial_code = '';
    // editor.setValue("");
    // result.setValue("");
    // editor.clearHistory();

    // hide revision submit button initially
    // $("#submit-revision").show()

    /* Code Mirror Controls */
    $fullscreen_code = $("#fullscreen-code");
    $toggle_code = $("#toggle-code");

    $fullscreen_code.click(function(e) {
        editor.setOption("fullScreen", !editor.getOption(
            "fullScreen"));
        editor.focus();
        e.preventDefault();
    });

    $toggle_code.click(function(e) {
        if (editor.getOption("theme") == "monokai") {
            editor.setOption("theme", "default");
        } else {
            editor.setOption("theme", "monokai");
        }
        e.preventDefault();
    });

    $fullscreen_result = $("#fullscreen-result");
    $toggle_result = $("#toggle-result");

    $fullscreen_result.click(function(e) {
        result.setOption("fullScreen", !result.getOption(
            "fullScreen"));
        result.focus();
        e.preventDefault();
    });

    $toggle_result.click(function(e) {
        if (result.getOption("theme") == "monokai") {
            result.setOption("theme", "default");
        } else {
            result.setOption("theme", "monokai");
        }
        e.preventDefault();
    });

    /* 
     * Selectors function
     * Write the queries using .on()
     */
    $("#plot_download").hide();
    /* Contributor details */



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
        ex_id = $("#examples").val();
        cat_id = $("#categories").val();
        book_id = $("#books").val();
        chapter_id = $("#chapters").val();
        if (!ex_id) {
            ex_id = "NULL";
        }
        console.log(ex_id);
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
            $("#submit-revision-wrapper").lightbox_me({
                centered: false
            });
        }, {
            code: editor.getValue(),
            initial_code: initial_code
        });
        // }
        e.preventDefault();
    });

    // onclick callback for revision-submit button click
    $(document).on("click", "#revision-form-submit", function(e) {
        ajax_loader(this);
        Dajaxice.website.revision_form_submit(function(data) {
            Dajax.process(data);
            initial_code = editor.getValue()
        }, {
            form: $('#revision-form').serialize(true),
            code: editor.getValue(),
        });
        e.preventDefault();
    });
    $("#diff-wrapper").hide();
    if($("#main_categories").val() == 0){
        $("#category-wrapper").hide();
        $("#books-wrapper").hide();
        $("#chapters-wrapper").hide();
        $("#examples-wrapper").hide();
        $("#revisions-wrapper").hide();
        $("#download-book").hide();
        $("#diff-wrapper").hide();
        $("#contributor").hide();
        $("#databox-wrapper").hide();
    }
    if($("#categories").val() == 0){
        $("#books-wrapper").hide();
        $("#chapters-wrapper").hide();
        $("#examples-wrapper").hide();
        $("#revisions-wrapper").hide();
        $("#download-book").hide();
        $("#diff-wrapper").hide();
        $("#contributor").hide();
    }
    if($("#books").val() == 0){
        $("#chapters-wrapper").hide();
        $("#examples-wrapper").hide();
        $("#revisions-wrapper").hide();
        $("#download-book").hide();
        $("#diff-wrapper").hide();
        $("#contributor").hide();
    }else{
            $("#download-book").show();
            $("#contributor").show();
    }
    if($("#chapters").val() == 0){
        $("#examples-wrapper").hide();
        $("#revisions-wrapper").hide();
        $("#diff-wrapper").hide();
        $("#download-chapter").hide();
    }else{
            $("#download-chapter").show();
    }
    if($("#examples").val() == 0){
        $("#revisions-wrapper").hide();
        $("#diff-wrapper").hide();
        $("#download-example").hide();
    }else{
        $("#download-example").show();
    }
    /*******************************************/
    /******  Below removed dajax ***************/
    /*******************************************/
    /*********** Main categories change ********/
    /*******************************************/
    $(document.body).on("change", "#main_categories", function() {
        var maincat_id = $('#main_categories').find(":selected").val();
        if (maincat_id != 0) {
            $("#categories").html("");
            $("#category-wrapper").show();
            $("#books").html("");
            editor.setValue("");
            result.setValue("");
            $("#chapters-wrapper").hide();
            $("#examples-wrapper").hide();
            $("#revisions-wrapper").hide();
            $("#download-book").hide();
            $("#submit-revision").hide();
            $("#review-link").hide();
            $("#contributor").hide();
            $.ajax({
                url: 'get_subcategories/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    maincat_id: maincat_id,
                },
                success: function(data) {
                    $("#categories").html('');
                    $("#categories").html(
                        ' <option value="">Select Subcategory</option>'
                    );
                    for (var i = 0; i < data.length; i++) {
                        $('#categories').append(
                            '<option value="' +
                            data[i].subcategory_id + '">' +
                            data[i].subcategory + '</option>');
                    }
                }
            });
        } else {
            editor.setValue("");
            result.setValue("");
            $("#categories").html("");
            $("#category-wrapper").hide();
            $("#review-link").hide();
            $("#books-wrapper").hide();
            $("#chapters-wrapper").hide();
            $("#examples-wrapper").hide();
            $("#revisions-wrapper").hide();
            $("#download-book").hide();
            $("#diff-wrapper").hide();
        }
    });
    /*******************************************/
    /*******************************************/
    /**************** sub categories change ********/
    /*******************************************/
    $(document.body).on("change", "#categories", function() {
        var maincat_id = $('#main_categories').find(":selected").val();
        var subcat_id = $('#categories').find(":selected").val();
        if (subcat_id != 0) {
            $("#books-wrapper").show();
            $("#books").html("");
            editor.setValue("");
            result.setValue("");
            $("#chapters-wrapper").hide();
            $("#examples-wrapper").hide();
            $("#revisions-wrapper").hide();
            $("#download-book").hide();
            $("#submit-revision").hide();
            $("#review-link").hide();
            $.ajax({
                url: 'get_books/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    maincat_id: maincat_id,
                    cat_id: subcat_id,
                },
                success: function(data) {
                    $("#books").html('');
                    $("#books").html(
                        ' <option value="">Select Book</option>'
                    );
                    for (var i = 0; i < data.length; i++) {
                        $('#books').append(
                            '<option value="' +
                            data[i].id + '">' +
                            data[i].book +
                            ' (by ' + data[i].author +
                            ' )' + '</option>');
                    }
                }
            });
        } else {
            editor.setValue("");
            result.setValue("");
            $("#review-link").hide();
            $("#books-wrapper").hide();
            $("#chapters-wrapper").hide();
            $("#examples-wrapper").hide();
            $("#revisions-wrapper").hide();
            $("#download-book").hide();
            $("#diff-wrapper").hide();
            $("#contributor").hide();
        }
    });
    /*******************************************/
    /*******************************************/
    /**************** book change **************/
    /*******************************************/
    $(document.body).on("change", "#books", function() {
        var book_id = $('#books').find(":selected").val();
        $("#chapters-wrapper").show();
        console.log(book_id);

        if (book_id != 0) {
            $("#download-book").show();
            $("#contributor").show();
            $("#chapters-wrapper").show();
            editor.setValue("");
            result.setValue("");
            $("#examples-wrapper").hide();
            $("#revisions-wrapper").hide();
            $("#download-chapter").hide();
            $("#submit-revision").hide();
            $("#review-link").hide();
            $.ajax({
                url: 'get_chapters/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    book_id: book_id,
                },
                success: function(data) {
                    $("#chapters").html('');
                    $("#chapters").html(
                        ' <option value="">Select Chapter</option>'
                    );
                    for (var i = 0; i < data.length; i++) {
                        $('#chapters').append(
                            '<option value="' +
                            data[i].id + '">' +
                            data[i].number +
                            ' - ' + data[i].chapter +
                            '</option>');
                    }
                }
            });
        } else {
            $("#chapters-wrapper").hide();
            $("#download-book").hide();
            $("#examples-wrapper").hide();
            $("#revisions-wrapper").hide();
            editor.setValue("");
            result.setValue("");
            $("#submit-revision").hide();
            $("#contributor").hide();
            $("#review-link").hide();
            $("#diff-wrapper").hide();
        }
    });
    /*******************************************/
    /*******************************************/
    /************ chapter change ***************/
    /*******************************************/
    $(document.body).on("change", "#chapters", function() {
        var chapter_id = $('#chapters').find(":selected").val();
        $("#examples-wrapper").show();
        console.log(chapter_id);
        if (chapter_id != 0) {
            $("#examples-wrapper").show();
            $("#download-chapter").show();
            editor.setValue("");
            result.setValue("");
            $("#revisions-wrapper").hide();
            $("#download-example").hide();
            $("#review-link").hide();
            $.ajax({
                url: 'get_examples/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    chapter_id: chapter_id,
                },
                success: function(data) {
                    $("#examples").html(
                        ' <option value="">Select Example</option>'
                    );
                    for (var i = 0; i < data.length; i++) {
                        $('#examples').append(
                            '<option value="' +
                            data[i].id + '">' +
                            data[i].number +
                            ' - ' + data[i].caption +
                            '</option>');
                    }
                }
            });
        } else {
            $("#download-chapter").hide();
            $("#examples-wrapper").hide();
            $("#revisions-wrapper").hide();
            editor.setValue("");
            result.setValue("");
            $("#submit-revision").hide();
            $("#review-link").hide();
            $("#diff-wrapper").hide();
        }
    });
    /*******************************************/
    /*******************************************/
    /************ revision change **************/
    /*******************************************/
    $(document.body).on("change", "#examples", function() {
        var example_id = $('#examples').find(":selected").val();
        //$("#revisions-wrapper").html("");
        $("#download-example").show();
        if (example_id != 0) {
            $("#revisions-wrapper").show();
            $("#download-example").show();
            $("#submit-revision").show();
            editor.setValue("");
            result.setValue("");
            ajax_loader('#revisions');
            $.ajax({
                url: 'get_revisions/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    example_id: example_id,
                },
                success: function(data) {
                    $("#revisions").html(
                        ' <option value="">Select a revision</option>'
                    );
                    var i = 1;
                    data.commits.forEach(function(
                        item) {
                        $('#revisions').append(
                            '<option value="' +
                            item.sha +
                            '"> ' + i +
                            ' - ' +
                            item.commit
                            .message +
                            '</option>'
                        );
                        i++;
                    });
                    ajax_loader("clear");
                    $('#revisions option:eq(1)').prop(
                        'selected', true);
                    $.ajax({
                        url: 'get_code/',
                        dataType: 'JSON',
                        type: 'GET',
                        data: {
                            commit_sha: $(
                                '#revisions'
                            ).val(),
                            example_id: example_id,
                        },
                        success: function(
                            data) {
                            editor.setValue(
                                data
                                .code
                            );
                            initial_code
                                =
                                editor.getValue()
                        }
                    });
                }
            });
        } else {
            $("#revisions-wrapper").hide();
            $("#download-example").hide();
            $("#submit-revision").hide();
            editor.setValue("");
            result.setValue("");
            $("#diff-wrapper").hide();
        }
    });
    /********************************************/
    /********************************************/
    /********** revision-diff change ************/
    /********************************************/
    $(document).on("change", "#revisions-diff", function(e) {
        var revName = $("#revisions-diff").find(":selected").text();
        var example_id = $('#examples').find(":selected").val();
        if ($(this).val()) {
            ajax_loader(this);
            $.ajax({
                url: 'get_diff/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    diff_commit_sha: $('#revisions').val(),
                    example_id: example_id,
                },
                success: function(data) {
                    console.log(data);
                    ajax_loader("clear");
                    $("#diff-wrapper").lightbox_me({
                        centered: false
                    });
                    $("#diff-area").html(diffString(
                        editor.getValue(),
                        data.code2));
                    $("#diff-first").html(
                        'editor code')
                    console.log(revName)
                    $("#diff-second").html(revName)
                    editor.setValue(data.code);
                    initial_code = editor.getValue()
                }
            });
        }
    });
    /********************************************/
    /********************************************/
    /******** Execute the code ******************/
    /********************************************/
    $plotbox_wrapper = $("#plotbox-wrapper");
    $plotbox = $("#plotbox");

    $(document).on("click", "#execute", function() {
        $("#execute-inner").html("Executing...");
        var send_data = {
            token: $("[name='csrfmiddlewaretoken']").val(),
            code: editor.getValue(),
            book_id: $("#books").val() || 0,
            chapter_id: $("#chapters").val() || 0,
            example_id: $("#examples").val() || 0
        };
        $.post("/execute-code", send_data,
            function(data) {
                $("#execute-inner").html("Execute");
                result.setValue(data.output);

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
                    var dt = $("#examples option:selected")
                        .text();
                    $("#plot_download").show();
                    $("#plot_download").attr("download", dt +
                        '.png');
                    $("#plot_download").attr("href", data.plot_path);
                }
            });
    });
    /********************************************/
    /********************************************/
    /****** Download book, chapter, example *****/
    /********************************************/
    $(document).on("click", "#download-book", function(e) {
        window.location = "http://scilab.in/download/book/" + $(
            "#books").val();
        e.preventDefault();
    });

    $(document).on("click", "#download-chapter", function(e) {
        window.location = "http://scilab.in/download/chapter/" +
            $("#chapters").val();
        e.preventDefault();
    });

    $(document).on("click", "#download-example", function(e) {
        window.location = "http://scilab.in/download/example/" +
            $("#examples").val();
        e.preventDefault();
    });
    /********************************************/
    /********************************************/
    /****** Get contributor *********************/
    /********************************************/
    $(document).on("click", "#contributor", function(e) {
            $.ajax({
                url: 'get_contributor/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    book_id: $("#books").val()
                },
                success: function(data) {

                $('#full_name').html(data.contributor_name);
                $('#faculty').html(data.proposal_faculty);
                $('#reviewer').html(data.proposal_reviewer);
                $('#university').html(data.proposal_university);
                $("#databox-wrapper").lightbox_me({
                centered: true
            });
                }
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
    /********************************************/
});
