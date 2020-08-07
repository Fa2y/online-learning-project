$(function() { //////source:https://bootsnipp.com/snippets/ykXa
    console.log("I am not a front-end dev I just copy and paste what I find cool and try to add the source too");
    // $(document).on('click', '.btn-add', function(e) {
    //     e.preventDefault();
    //     var controlForm = $('.Question div:first'),
    //         currentEntry = $(this).parents('.entry:first'),
    //         newEntry = $(currentEntry.clone()).appendTo(controlForm);

    //     newEntry.find('input').val('');
    //     controlForm.find('.entry:not(:last) .btn-add')
    //         .removeClass('btn-add').addClass('btn-remove')
    //         .removeClass('btn-success').addClass('btn-danger')
    //         .html('<i class="fas fa-lg fa-minus-circle"></i>');
    // }).on('click', '.btn-remove', function(e) {
    //     $(this).parents('.entry:first').remove();

    //     e.preventDefault();
    //     return false;
    // }); 
          var newStyle = document.createElement("link");
      newStyle.rel = "stylesheet";
      newStyle.href = "https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/css/bootstrap-select.min.css";
      document.getElementsByTagName("head")[0].appendChild(newStyle);
      $('[data-toggle="tooltip"]').tooltip()
      $('.btn-add').tooltip('show');
    /////source:https://bootsnipp.com/snippets/kMp2V
    $('body').on("click", "#add_row", function() {
        // Dynamic Rows Code
        // Get max row id and set new id
        var newid = 0;
        $.each($("#tab_logic tr"), function() {
            if (parseInt($(this).data("id")) > newid) {
                newid = parseInt($(this).data("id"));
            }
        });
        newid++;

        var tr = $("<tr></tr>", {
            id: "addr" + newid,
            "data-id": newid
        });
        i = 0;
        // loop through each td and create new elements with name of newid
        $.each($("#tab_logic tbody tr:nth(0) td"), function() {
            $('button[name ="del0"]').prop('disabled', false);
            var td;
            var cur_td = $(this);

            var children = cur_td.children();

            // add new td and element if it has a nane
            if ($(this).data("name") !== undefined) {
                td = $("<td></td>", {
                    "data-name": $(cur_td).data("name")
                });

                var c = $(cur_td).find($(children[0]).prop('tagName')).clone().val("");
                //A quick fix for the switch input bcuz it was assiging the name to the lable instead of the input
                if (i == 1) {
                    var c1 = $(c.children()[0])
                    c1.attr("name", $(cur_td).data("name") + newid);

                } else {
                    c.attr("name", $(cur_td).data("name") + newid);
                }
                c.appendTo($(td));
                td.appendTo($(tr));
            } else {
                td = $("<td></td>", {
                    'text': $('#tab_logic tr').length
                }).appendTo($(tr));
            }
            i += 1;
            $('button[name ="del0"]').prop('disabled', true);
        });

        // add delete button and td
        /*
        $("<td></td>").append(
            $("<button class='btn btn-danger glyphicon glyphicon-remove row-remove'></button>")
                .click(function() {
                    $(this).closest("tr").remove();
                })
        ).appendTo($(tr));
        */

        // add the new row
        $(tr).appendTo($('#tab_logic'));


        $("body").on("click", 'button.row-remove', function() {
            $(this).closest("tr").remove();
        });
    });




    // Sortable Code
    var fixHelperModified = function(e, tr) {
        var $originals = tr.children();
        var $helper = tr.clone();

        $helper.children().each(function(index) {
            $(this).width($originals.eq(index).width())
        });

        return $helper;
    };

    $(".table-sortable tbody").sortable({
        helper: fixHelperModified
    }).disableSelection();

    $(".table-sortable thead").disableSelection();



    $("#add_row").trigger("click");

});