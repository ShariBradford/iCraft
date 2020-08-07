$('form.registration input').keyup(function(e){
    var $element = $(this),
        data = {
            fieldname: e.target.name, //$(this).attr('name'),
            value: e.target.value, //$(this).val(),
            csrfmiddlewaretoken: getCookie('csrftoken'),
        };

    //the password confirmation validator needs both the password and the password_confirm fields
    //add the password field  to the data payload
    if ($element.attr('name') == 'password_confirm') {
        data['password'] = $('input[name="password"]').val()
    }

    $.ajax({
        url: 'validate',
        method: 'POST',
        data: data,
    })
    .done(function(data){
        console.log(data);
        $element.prev('div.message').html(data);
    })
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}