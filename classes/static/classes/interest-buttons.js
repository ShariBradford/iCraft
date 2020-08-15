$(document).ready(function(){
    var $select = $('select#id_areas_of_interest');
    var $selectErrors = $select.siblings('p.alert');
    var $selectExtras = $($select.prevAll().get().reverse()); //get the errors (if any), label, and required indicator (if any) 

    var htmlString = '<div class="areas-of-interest">';
    //htmlString += '<p>Areas of Interest: <small class="text-muted">(Click to select)</small></p>';
    htmlString += '<div class="button-bar d-flex flex-wrap" style="width:100%;">';

    $select.find('option').each(function(){
        var imgSource = static_prefix + 'classes/images/interests' + $(this).val() + ($(this).is(':selected') ? '-selected' : '') + '.png';

        htmlString += '<div data-id="' + $(this).val() + '" data-selected="' + $(this).is(':selected') + '" class="button d-flex flex-column align-items-center justify-content-between" style="width:100px;height:100px;border:1pt solid #009EC3;margin:5px;padding:5px;border-radius:5px;">';
        htmlString += '<img src="' + imgSource + '" alt="' + $(this).text() + '" style="width:80%;">';
        htmlString += '<span style="font-size:8pt;">' + $(this).text() + '</span>';
        htmlString += '</div>';
    });

    htmlString += '</div><!-- end .button-bar -->';
    htmlString += '</div><!-- end .areas-of-interest -->';

    $('.right-column').append(htmlString); //$select.after(htmlString);
    $select.closest('div.fieldWrapper').hide();
    $('div.areas-of-interest').prepend($selectExtras);
    //$selectErrors.prependTo('div.areas-of-interest');

    $('.button-bar div.button').click(function(e){
        var isSelected = $(this).attr('data-selected') == "true";
        //get related option in hidden select
        var selectOption = $('select#id_areas_of_interest option[value="' + $(this).attr('data-id') + '"]');
        var imgSource = '';

        if (isSelected) {
            selectOption.prop('selected', false); //deselect option in hidden select
            $(this).attr('data-selected','false'); //toggle data-selected value for button
        } else {
            selectOption.prop('selected', true); //select option in hidden select
            $(this).attr('data-selected','true'); //toggle data-selected value for button
        }

        isSelected = !isSelected; //toggle isSelected
        imgSource = static_prefix + 'classes/images/interests' + $(this).attr('data-id') + (isSelected ? '-selected' : '') + '.png';
        $(this).find('img').attr('src', imgSource) ;
    });
})
