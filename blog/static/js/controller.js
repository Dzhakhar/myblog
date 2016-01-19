var post_price = $('.post_price');
var inp = $('.amount');
var price = inp.attr('pr');
var product_id = inp.attr('pi');
var form_action = $('.add');
inp.on('input keyup', function(){
  var count = $(this).val();
  post_price.html(count*price);
  form_action.attr('action', '/add_to_cart/' + product_id + '/' + count);
});
var cart_input = $('.table_item_item_3 input');
$('.table_item_item_4').click(function(){
  $(this).html($(this).siblings().children().val() + $(this).siblings().children().attr('pp'));
});

$(document).ready(function(){
  $('.table_item_item_4').click();
});

cart_input.on('input keyup', function(){
  var counter = $(this).val();
  $(this).parent().siblings('.table_item_item_4').html($(this).val() * $(this).attr('pp'));
});
