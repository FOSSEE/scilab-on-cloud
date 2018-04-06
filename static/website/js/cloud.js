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
    var editor = CodeMirror.fromTextArea(document.getElementById(
        "code"), {
        lineNumbers: true,
        lineWrapping: true,
        theme: "default",
        extraKeys: {
            "F11": function(cm) {
                cm.setOption("fullScreen", !cm.getOption(
                    "fullScreen"));
            },
            "Esc": function(cm) {
                if (cm.getOption("fullScreen")) cm
                    .setOption(
                        "fullScreen", false);
            }
        }
    });

    var result = CodeMirror.fromTextArea(document.getElementById(
        "result"), {
        lineWrapping: true,
        theme: "default",
        readOnly: true,
        extraKeys: {
            "F11": function(cm) {
                cm.setOption("fullScreen", !cm.getOption(
                    "fullScreen"));
            },
            "Esc": function(cm) {
                if (cm.getOption("fullScreen")) cm
                    .setOption(
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
        if (result.getOption("theme") == "defaul") {
            result.setOption("theme", "monokai");
        } else {
            result.setOption("theme", "default");
        }
        e.preventDefault();
    });

    /* 
     * Selectors function
     * Write the queries using .on()
     */
    /* Contributor details */
    // $(document).on("click", "#bug-form #id_notify", function() {
    //     $("#id_email_wrapper").toggle(this.checked);
    // });

    $("#plot_download").hide();
    $("#diff-wrapper").hide();
    $("#databox-wrapper").hide();
    if ($("#main_categories").val() == 0) {
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
    if ($("#categories").val() == 0) {
        $("#books-wrapper").hide();
        $("#chapters-wrapper").hide();
        $("#examples-wrapper").hide();
        $("#revisions-wrapper").hide();
        $("#download-book").hide();
        $("#diff-wrapper").hide();
        $("#contributor").hide();
        $("#databox-wrapper").hide();
    }
    if ($("#books").val() == 0) {
        $("#chapters-wrapper").hide();
        $("#examples-wrapper").hide();
        $("#revisions-wrapper").hide();
        $("#download-book").hide();
        $("#diff-wrapper").hide();
        $("#contributor").hide();
        $("#databox-wrapper").hide();
    } else {
        $("#download-book").show();
        $("#contributor").show();
    }
    if ($("#chapters").val() == 0) {
        $("#examples-wrapper").hide();
        $("#revisions-wrapper").hide();
        $("#diff-wrapper").hide();
        $("#download-chapter").hide();
    } else {
        $("#download-chapter").show();
    }
    if ($("#examples").val() == 0) {
        $("#revisions-wrapper").hide();
        $("#diff-wrapper").hide();
        $("#download-example").hide();
        $("#databox-wrapper").hide();
    } else {
        $("#download-example").show();
    }
    /*******************************************/
    /******  Below removed dajax ***************/
    /*******************************************/
    /*********** Main categories change ********/
    /*******************************************/
    $(document.body).on("change", "#main_categories",
        function() {
            ajax_loader(this);
            var maincat_id = $('#main_categories').find(
                ":selected").val();
            if (maincat_id != 0) {
                $("#categories").html("");
                $("#category-wrapper").show();
                $("#books").html("");
                editor.setValue("");
                result.setValue("");
                $("#example_views_count").text("");
                $("#chapters-wrapper").hide();
                $("#examples-wrapper").hide();
                $("#books-wrapper").hide();
                $("#revisions-wrapper").hide();
                $("#download-book").hide();
                $("#submit-revision").hide();
                $("#review-link").hide();
                $("#contributor").hide();
                $("#databox-wrapper").hide();
                $.ajax({
                    url: 'get_subcategories/',
                    dataType: 'JSON',
                    type: 'GET',
                    data: {
                        maincat_id: maincat_id,
                    },
                    success: function(data) {
                    ajax_loader("clear");
                        $("#categories").html(
                            '');
                        $("#categories").html(
                            ' <option value="">Select Subcategory</option>'
                        );
                        for (var i = 0; i <
                            data.length; i++) {
                            $('#categories').append(
                                '<option value="' +
                                data[i].subcategory_id +
                                '">' +
                                data[i].subcategory +
                                '</option>'
                            );
                        }
                    }
                });
            } else {
                ajax_loader("clear");
                $("#example_views_count").text("");
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
                $("#databox-wrapper").hide();
            }
        });
    /*******************************************/
    /*******************************************/
    /**************** sub categories change ********/
    /*******************************************/
    $(document.body).on("change", "#categories", function() {
        ajax_loader(this);
        var maincat_id = $('#main_categories').find(
            ":selected").val();
        var subcat_id = $('#categories').find(
            ":selected").val();
        if (subcat_id != 0) {
            $("#books-wrapper").show();
            $("#books").html("");
            editor.setValue("");
            result.setValue("");
            $("#example_views_count").text("");
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
                    ajax_loader("clear");
                    $("#books").html('');
                    $("#books").html(
                        ' <option value="">Select Book</option>'
                    );
                    for (var i = 0; i <
                        data.length; i++) {
                        $('#books').append(
                            '<option value="' +
                            data[i].id +
                            '">' +
                            data[i].book +
                            ' (by ' +
                            data[i].author +
                            ' )' +
                            '</option>'
                        );
                    }
                }
            });
        } else {
            ajax_loader("clear");
            $("#example_views_count").text("");
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
        ajax_loader(this);
        $("#chapters-wrapper").show();
        console.log(book_id);

        if (book_id != 0) {
            $("#download-book").show();
            $("#contributor").show();
            $("#chapters-wrapper").show();
            editor.setValue("");
            result.setValue("");
            $("#example_views_count").text("");
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
                ajax_loader("clear");
                    $("#chapters").html(
                        '');
                    $("#chapters").html(
                        ' <option value="">Select Chapter</option>'
                    );
                    for (var i = 0; i <
                        data.length; i++) {
                        $('#chapters').append(
                            '<option value="' +
                            data[i].id +
                            '">' +
                            data[i].number +
                            ' - ' +
                            data[i].chapter +
                            '</option>'
                        );
                    }
                }
            });
        } else {
            ajax_loader("clear");
            $("#example_views_count").text("");
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
        ajax_loader(this);
        var chapter_id = $('#chapters').find(
            ":selected").val();
        $("#examples-wrapper").show();
        console.log(chapter_id);
        if (chapter_id != 0) {
            $("#examples-wrapper").show();
            $("#download-chapter").show();
            editor.setValue("");
            result.setValue("");
            $("#example_views_count").text("");
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
                    ajax_loader("clear");
                    $("#examples").html(
                        ' <option value="">Select Example</option>'
                    );
                    for (var i = 0; i <
                        data.length; i++) {
                        $('#examples').append(
                            '<option value="' +
                            data[i].id +
                            '">' +
                            data[i].number +
                            ' - ' +
                            data[i].caption +
                            '</option>'
                        );
                    }
                }
            });
        } else {
            ajax_loader("clear");
            $("#example_views_count").text("");
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
    /************ Example change **************/
    /*******************************************/
    $(document.body).on("change", "#examples", function() {
        ajax_loader(this);
        var example_id = $('#examples').find(
            ":selected").val();
        //$("#revisions-wrapper").html("");
        $("#download-example").show();
        if (example_id != 0) {
            $("#example_views_count").text("");
            $("#revisions-wrapper").show();
            $("#download-example").show();
            $("#submit-revision").show();
            $("#databox-wrapper").hide();
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
                         var ex_id = example_id;
                         $.ajax({
                            url: 'update_view_count/',
                            dataType: 'JSON',
                            type : 'GET',
                            data: {
                                    ex_id: ex_id,
                            },
                            success: function(data){
                            $("#example_views_count").text(data);
                            }
                         });
                    $("#revisions").html(
                        ' <option value="">Select a revision</option>'
                    );

                    var i = 1;
                    data.commits.forEach(
                        function(
                            item) {
                            $('#revisions').append(
                                '<option value="' + item.sha + '"> ' +
                                i + ' - ' + item.commit.message +
                                '</option>'
                            );
                            i++;
                        });
                    $("#revisions-diff").html(
                        ' <option value="">Select a revision</option>'
                    );
                    var i = 1;
                    data.commits.forEach(
                        function(
                            item) {
                            $('#revisions-diff').append(
                                '<option value="' + item.sha + '"> ' +
                                i + ' - ' + item.commit.message +
                                '</option>'
                            );
                            i++;
                        });
                    $(
                        '#revisions option:eq(1)'
                    ).prop(
                        'selected',
                        true);
                    $.ajax({
                        url: 'get_code/',
                        dataType: 'JSON',
                        type: 'GET',
                        data: {
                            commit_sha: $('#revisions').val(),
                            example_id: example_id,
                        },
                        success: function(data) {
                        if (data.review != 0) {
                            $("#review").show();
                            $("#review").attr("href",data.review_url);
                            $("#review").text(data.review + " " + "Review");
                        } else {
                            $("#review").hide();
                        }
                            $("#example_views_count").text(data.exmple);
                            editor.setValue("clear; // Remove clear, clc from code if you want to access existing stored variable from the memory"
                            + "\n"+"\n" + data.code);
                            initial_code = editor .getValue();
                            ajax_loader("clear");
                        }
                    });
                }
            });
        } else {
            ajax_loader("clear");
            $("#example_count").text("");
            $("#revisions-wrapper").hide();
            $("#download-example").hide();
            $("#submit-revision").hide();
            editor.setValue("");
            result.setValue("");
            $("#diff-wrapper").hide();
            $("#databox-wrapper").hide();
        }
    });
    /********************************************/
    /********************************************/
    /********** revision-change ************/
    /********************************************/
    $(document.body).on("change", "#revisions", function(e) {
        ajax_loader(this);
        $("#revisions-two").hide()
                var example_id = $('#examples').find(
            ":selected").val();
        if ($(this).val()) {

            $.ajax({
                        url: 'get_code/',
                        dataType: 'JSON',
                        type: 'GET',
                        data: {
                            commit_sha: $('#revisions').val(),
                            example_id: example_id,
                        },
                        success: function(data) {
                        ajax_loader("clear");
                            if (data.review != 0) {
                                   $("#review").show();
                        $("#review").attr("href",data.review_url);
                        $("#review").text(data.review + " " + "Review");
                            } else {
                                $("#review").hide();
                            }
                            editor.setValue(data.code);
                            initial_code = editor .getValue();
                        }
                    });



                // show revision submit button when a revision is loaded
                $("#submit-revision").show();
                $("#revisions-two").show();
        }
    });
    /********************************************/
    /********************************************/
    /********** revision-diff change ************/
    /********************************************/
    $(document).on("change", "#revisions-diff", function(e) {
        var revName = $("#revisions-diff").find(
            ":selected").text();
        var example_id = $('#examples').find(
            ":selected").val();
        if ($(this).val()) {
            ajax_loader(this);
            $.ajax({
                url: 'get_diff/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    diff_commit_sha: $(
                        '#revisions').val(),
                    example_id: example_id,
                },
                success: function(data) {
                    console.log(data);
                    ajax_loader("clear");
                    $("#diff-wrapper").lightbox_me({
                        centered: false
                    });
                    $("#diff-area").html(
                        diffString(
                            editor.getValue(),
                            data.code2
                        ));
                    $("#diff-first").html(
                        'editor code'
                    )
                    console.log(revName)
                    $("#diff-second").html(
                        revName)
                    editor.setValue(data.code);
                    initial_code = editor
                        .getValue()
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
            token: $(
                "[name='csrfmiddlewaretoken']"
            ).val(),
            code: editor.getValue(),
            book_id: $("#books").val() || 0,
            chapter_id: $("#chapters").val() || 0,
            example_id: $("#examples").val() || 0
        };
        $.post("/execute-code", send_data,
            function(data) {
                $("#execute-inner").html(
                    "Execute");
                result.setValue(data.output);
                pp = data.plot_path;
                if (data.plot_path) {
                    $.ajax({
                        type: "HEAD",
                        async: true,
                        url: pp,
                    }).done(function(){
                    $plot = $("<img>");
                    $plot.attr({
                        src: data.plot_path,
                        width: '100%'
                    });
                    $plotbox.html($plot);
                   
                   /* $plotbox_wrapper.lightbox_me({
                        centered: true
                    });*/
                     $plotbox_wrapper.modal('show');
                    var dt = $(
                            "#examples option:selected"
                        )
                        .text();
                    $("#plot_download").show();
                    $("#plot_download").attr(
                        "download", dt +
                        '.png');
                    $("#plot_download").attr(
                        "href", data.plot_path
                    );
                     });
                }
            });
    });
    /********************************************/
    /********************************************/
    /****** Download book, chapter, example *****/
    /********************************************/
    $(document).on("click", "#download-book", function(e) {
        window.location =
            "http://scilab.in/download/book/" + $(
                "#books").val();
        e.preventDefault();
    });

    $(document).on("click", "#download-chapter", function(e) {
        window.location =
            "http://scilab.in/download/chapter/" +
            $("#chapters").val();
        e.preventDefault();
    });

    $(document).on("click", "#download-example", function(e) {
        window.location =
            "http://scilab.in/download/example/" +
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

                $('#full_name').html(data
                    .contributor_name
                );
                $('#faculty').html(data.proposal_faculty);
                $('#reviewer').html(data.proposal_reviewer);
                $('#university').html(
                    data.proposal_university
                );
                $("#databox-wrapper").lightbox_me({
                    centered: true
                });
            }
        });
        e.preventDefault();
    });
    /********************************************/
    /********************************************/
    /****** Node popup handling *******************/
    /********************************************/
    $(document).on("click", ".node", function(e) {
        $.ajax({
            url: 'get_node/',
            dataType: 'JSON',
            type: 'GET',
            data: {
                key: $(this).data("key")
            },
            success: function(data) {
                console.log(data);
                $('#node-wrapper').html(
                    data);
                $("#node-wrapper").lightbox_me({
                    centered: true
                });
            }
        });
        e.preventDefault();
    });
    /********************************************/
    /********************************************/
    /****** Bug form handling *******************/
    /********************************************/
    $(document).on("click", "#bug", function(e) {

        $.ajax({
            url: 'get_bug_form/',
            dataType: 'JSON',
            type: 'GET',
            data: {
                bug_form: 'bug_form_pop'
            },
            success: function(data) {
                console.log(data);
                $('#bug-form-wrapper').html(
                    data);
                $("#bug-form-wrapper").lightbox_me({
                    centered: false
                });
            }
        });
        e.preventDefault();
    });
    /********************************************/

    $(document).on("click", "#bug-form-submit", function(e) {
        ajax_loader(this);
        ex_id = $("#examples").val();
        cat_id = $("#categories").val();
        book_id = $("#books").val();
        chapter_id = $("#chapters").val();
        issue_id = $("#id_issue").val();
        id_description_wrapper = $(
            "id_description_wrapper").val().trim();
        id_email = $("id_email").val().trim();
        if (issue_id == 0) {
            $('#id_issue').css({
                "border": '#FF0000 1px solid'
            });
            alert("Please select any issues");
        } else if (id_description_wrapper.length == 0) {
            $('#id_issue').css({
                "border": '#FF0000 1px solid'
            });
            alert("Please insert issue description");
        } else if (id_email.length == 0) {
            $('#id_email').css({
                "border": '#FF0000 1px solid'
            });
            alert("Please insert email id");
        } else {
            if (!ex_id) {
                ex_id = "NULL";
            }
            console.log(ex_id);
            $.ajax({
                url: 'get_bug_form_submit/',
                dataType: 'JSON',
                type: 'GET',
                data: {
                    form: $("#bug-form").serialize(
                        true),
                    cat_id: cat_id,
                    book_id: book_id,
                    chapter_id: chapter_id,
                    ex_id: ex_id,
                },
                success: function(data) {
                    console.log(data);
                    alert(data);
                    ajax_loader("clear");
                    $("#bug-form-wrapper")
                        .trigger("close");
                }
            });

        }

        e.preventDefault();
    });
    /********************************************/
    /********************************************/
    /************ submit revision handling ******/
    /********************************************/
    $(document).on("click", "#submit-revision", function(e) {


        $.ajax({
            url: 'get_submit_revision_form/',
            dataType: 'JSON',
            type: 'GET',
            data: {
                code: editor.getValue(),
                initial_code: initial_code
            },
            success: function(data) {
                $(
                    "#submit-revision-wrapper"
                ).html(data);
                $(
                    "#submit-revision-wrapper"
                ).lightbox_me({
                    centered: false
                });
            }
        });
        e.preventDefault();
    });
    /********************************************/
    /********************************************/
    /********* submit revision form submit ******/
    /********************************************/
    $(document).on("click", "#revision-form-submit", function(
        e) {
        ajax_loader(this);

        $.ajax({
            url: 'get_submit_revision_form_submit/',
            dataType: 'JSON',
            type: 'GET',
            data: {
                form: $('#revision-form').serialize(
                    true),
                code: editor.getValue(),
            },
            success: function(data) {
                initial_code = editor.getValue()
                alert(data);
                $(
                    "#submit-revision-wrapper"
                ).trigger("close");
            }
        });
    });
    /********************************************/
 $(document).on("click", "#search", function() {
        $("#relevant").html('');
        var search_string = jQuery.trim($("#search-input").val());
        if (search_string == ''){
        search_string = 'Null';
        }
         $.ajax({
            url: 'search_book',
            dataType: 'JSON',
            type : 'GET',
            data: {
                    search_string: search_string,
            },
            success: function(data){
                $("#relevant").html('<h2>Relevant</h2><hr>');
                for (var i = 0; i < data.length; i++) {
                $("#relevant").append(
                '<a  href="?book_id='+ data[i].ids +'" class="">' + data[i].book +
                ' (Author: ' + data[i].author + ')</a><hr>');
                }
            }
         }),
         $.ajax({
            url: 'search_book/popular/',
            dataType: 'JSON',
            type : 'GET',
            data: {
                    search_string: search_string,
            },
            success: function(data){

                $("#popular").html('<h2>Popular</h2><hr>');
                for (var i = 0; i < data.length; i++) {
                $("#popular").append(
                '<a  href="?book_id='+ data[i].ids +'" class="">' + data[i].book
                + ' (Author: ' + data[i].author + ')</a><hr>');
                }
            }
         }),
            $.ajax({
                url: 'search_book/recent/',
                dataType: 'JSON',
                type : 'GET',
                data: {
                        search_string: search_string,
                },
            success: function(data){
                $("#recent").html('<h2>Recent</h2><hr>');
                for (var i = 0; i < data.length; i++) {
                $("#recent").append(
                '<a  href="?book_id='+ data[i].ids +'" class="">' + data[i].book +
                ' (Author: ' + data[i].author + ')</a><hr>');
                }
            }
         });


 });

 $(document).on("click", "#search_book", function(e) {
        $("#popular").html('');
        $("#recent").html('');
        var search_string = 'popular';
        if (search_string == ''){
        search_string = 'Null';
        }
         $.ajax({
            url: 'search_book/popular/',
            dataType: 'JSON',
            type : 'GET',
            data: {
                    search_string: search_string,
            },
            success: function(data){
               console.log(data);
                $("#popular").html('<h2>Popular</h2><hr>');
                for (var i = 0; i < data.length; i++) {
                    $("#popular").append(
                '<a  href="?book_id='+ data[i].ids +'" class="">' + data[i].book
                + ' (Author: ' + data[i].author + ')</a><hr>');
                }
            }
         }),
            $.ajax({
                url: 'search_book/recent/',
                dataType: 'JSON',
                type : 'GET',
                data: {
                        search_string: search_string,
                },
            success: function(data){
               console.log(data);
                $("#recent").html('<h2>Recent</h2><hr>');
                for (var i = 0; i < data.length; i++) {
                $("#recent").append(
                '<a  href="?book_id='+ data[i].ids +'" class="">' + data[i].book +
                ' (Author: ' + data[i].author + ')</a><hr>');
                }
            }
         });
e.preventDefault();

 });
 
}); //document.readOnly()
