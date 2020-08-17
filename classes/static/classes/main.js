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

function toggleFavorite(courseId, $element) {
    console.log('toggleFavorite() called.');

    var options = {
            method : 'GET',
            fail : function(error) {
                console.log(error);
            }
        };

    if ($element.attr('data-favorite') == 'true') {
        console.log("user has already favorited this course, so call un-favorite and reset div");
        options.url = "/classes/" + courseId + "/unfavorite";
        options.success = function() {
            console.log('Success!');
            $element.attr({
                'title' : "Favorite",
                'data-favorite' : "false",
            })
            .find('span').css('color','gray');
        };
    } else {
        //user has not favorited this course, so call favorite and reset div
        options.url = "/classes/" + courseId + "/favorite";
        options.success = function() {
            console.log('Success!');
            $element.attr({
                'title' : "Un-favorite",
                'data-favorite' : "true",
            })
            .find('span').css('color','red');
        };
    }

    return $.ajax(options);
}

/*
$('.container.main').on('click', '.favorite', function(e){
    //e.preventDefault();
    var courseId = $(this).closest('.card').attr('id');
    console.log('toggling favorite for course id ' + courseId);
    toggleFavorite(courseId, $(this));
    return false;
});
*/
function rateCourse(courseId){
    console.log('about to rate class via ajax.');
    $.ajax({
        url: '/classes/' + courseId + '/rate',
        method: 'POST',
        data: $('.ratings-form').serialize(),
    })
    .done(function(data){
        console.log('Successfully rated class.');
        $('div.user-rating').html(data);
    })
    .fail(function(error){
        console.log("Error submitting rating.");
        console.log(error);
    });
}

$('.course-details').on('click','.ratings-form input[type="submit"]', function(e){
    e.preventDefault();
    var courseId = $('.course-details').attr('data-id');
    rateCourse(courseId);
});

$('.course-details .ratings-form [data-id="comments"]').find('label').after('<span class="characters-remaining float-right" style="color:red;"></span>');

$('.course-details').on('keyup','.ratings-form [name="comments"]', function(e){
    var $span = $(this).siblings('.characters-remaining');
    var chars_remaining = 255 - $(this).val().length
    $span.html(chars_remaining + ' characters left.');
});

$('.search-form').submit(function(e){
    e.preventDefault();
    console.log('AJAX SEARCH:')
    console.log($('.search-form').serialize());

    var data = $('.search-form').serialize();
    data.csrfmiddlewaretoken = getCookie('csrftoken');

    $.ajax({
        url: '/classes/search',
        method: 'GET',
        data: data,
    })
    .done(function(data){
        console.log(data);
        $('div.content').html(data);
    })
    .fail(function(error){
        console.log("Error submitting rating.");
        console.log(error);
    });
})