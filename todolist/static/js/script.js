var todo_list = [];

$(document).ready(function() {
    $('#input-text').keyup(function(e) {
        if (e.keyCode === 13) {
            submit();
        }
     });
    todo_list = fetchList();
});

function submit() {
    var text = $('#input-text').val();
    text = text.trim();

    if (text != "") {
        if (todo_list.includes(text)) {
            alert(text + " is already in your todo list.");
        } else {
            $.ajax({
              type: "POST",
              url: "/todo/create",
              contentType: 'application/json',
              async: false,
              //json object to sent to the authentication url
              data: JSON.stringify({ "content": text}),
              success: function () {
                var $elem = $(
                    "<li class='list-group-item clearfix'>" +
                        "<span style='display: inline-block; vertical-align: middle;'>" + text + "</span>" +
                        "<div class='float-right btn-group'>" +
                            "<input type=button class='btn btn-info' value='EDIT' onclick='update(this)'>" +
                            "<input type=button class='btn btn-danger' value='DELETE' onclick='remove(this)'>" +
                        "</div>" +
                    "</li>"
                );
                todo_list.push(text);
                $elem.hide().appendTo($('#todo-list')).slideDown();
                $('#input-text').val("");
                console.log("Added " + text);
                }
            });
    }
}
}

function remove(e) {
    e = e.parentElement.parentElement;
    console.log(e);
    var text = $(e).children('span').text();
    console.log(text);
    if (confirm('Would you like to remove "'+ text +'" from your todo list?')) {
        $.ajax({
            type: "DELETE",
            contentType: 'application/json',
            url: "/todo/delete",
            data: JSON.stringify({"item": text}),
            dataType: "json",
            success: function (data) {
                if (data["result"] == "success") {
                    console.log("Removing " + text);
                    $(e).slideUp(300, function() {
                        $(e).remove();
                    });
                    todo_list.pop(todo_list.indexOf(text));
                } else {
                    console.log("Failed to remove " + text);
                }
            }
        });
    }
}

function update(e) {
    e = e.parentElement.parentElement;
    console.log(e);
    var text = $(e).children('span').text();
    console.log(text);

    $(e).children('span').text('');
    $newtext = $("<input type='text' class='form-control' placeholder='New todo...' value='" + text + "'>");
    $newtext.appendTo($(e).children('span'));
    $newtext.focus();
    $newtext.focusout(function() {
        setText(text);
    });
    $newtext.keyup(function(e2) {
        if (e2.keyCode === 13) {
            var text2 = $newtext.val();
            text2 = text2.trim();
            console.log("attempting change...");
            if (!(todo_list.includes(text2))) {
                $.ajax({
                    type: "PUT",
                    contentType: "application/json",
                    async: false,
                    url: "/todo/update",
                    data: JSON.stringify({"item": text, "new": text2}),
                    dataType: "json",
                    success: function (data) {
                        if (data["result"] == "success") {
                            console.log("Updating " + text + " to " + text2);
                            setText(text2);
                            todo_list[todo_list.indexOf(text)] = text2;
                        } else {
                            console.log("Failed to update " + text);
                        }
                    }
                });
            } else {
                alert(text2 + " is already in your todo list");
            }
        }
    });

    function setText(t) {
        $newtext.remove();
        $(e).children('span').append(t);
    }

}

function fetchList() {
    var list = [];
    $.ajax({
        type: "GET",
        url: "/todo/read",
        contentType: 'application/json',
        async: false,
        success: function (data) {
            list = data;
        }
    });
    return list;
}
