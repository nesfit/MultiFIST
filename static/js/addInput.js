var limit = 5;

function addInput(divName) {
    var counter = $("#" + divName + " > div").length;

    if (counter == limit) {
        alert("You have reached the limit of adding " + counter + " inputs");
    }
    else {
        var newdiv = document.createElement('div');
        newdiv.className = 'form-groups';
        newdiv.id = 'url_input_' + counter;

        var input_name = 'form-' + counter + '-url';
        var id = 'id_' + input_name;

        newdiv.innerHTML =
            "<label for='" + id + "'>Url:</label>" +
            "<div class='input-group control-group'>" +
            "<input name='" + input_name + "' maxlength='200' class='form-control' id='" + id + "'type='url'>" +
            "<div class='input-group-btn'>" +
            '<button class="btn btn-danger remove" type="button" onclick="removeInput(\'' + newdiv.id + '\')">Remove</button>' +
            "</div>" +
            "</div>";
        document.getElementById(divName).appendChild(newdiv);
        document.getElementById("id_form-TOTAL_FORMS").value = $("#" + divName + " > div").length;
    }
}

function removeInput(divID) {
    document.getElementById(divID).remove();
    document.getElementById("id_form-TOTAL_FORMS").value -= 1;
}

function renderInput(divName) {
    $("#" + divName + " > div").each(function (index, element) {
        if (index == 0) {
            // pass
        }
        else {
            element.id = 'url_input_' + index;
            var newdiv = document.createElement('div');
            newdiv.className = "input-group control-group";
            newdiv.innerHTML =
                "<div class='input-group-btn'>" +
                '<button class="btn btn-danger remove" type="button" onclick="removeInput(\'' +  element.id + '\')">Remove</button>' +
                "</div>";
            element.appendChild(newdiv);
            newdiv.prepend($(this).children("input").get(0));

            if($(this).children("div").length >1) {
                newdiv.appendChild($(this).children("div").get(0));
            }
        }
    });
}