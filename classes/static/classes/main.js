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

