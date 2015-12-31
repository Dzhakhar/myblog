$('.submenu').mouseover(function(){
    $(this).siblings().addClass('active');
    $(this).siblings().css('background', '#F38181');
    $(this).parent().siblings().children('.category').css('background', 'none');
    $(this).mouseout(function(){
        $(this).parent().css('background', 'none');
    })
});

$('.category').mouseover(function(){
    $(this).siblings('.category').css('background', 'none');
})

$('.category').mouseout(function(){
    $(this).css('background', 'none');
})