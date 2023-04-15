$(document).ready(function(){
    $('.types-check').click(function() {
        $('.types-check').not(this).prop('checked', false);
    });
});

$(document).ready(function(){
    $('.regions-check').click(function() {
        $('.regions-check').not(this).prop('checked', false);
    });
});

$(document).ready(function(){
    $('.natures-check').click(function() {
        $('.natures-check').not(this).prop('checked', false);
    });
});
