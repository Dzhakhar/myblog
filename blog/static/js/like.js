$(document).ready(function(){
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    var likeload = function(){
      if($(this).attr('src') == '/media/heart.png'){
        $(this).attr('src', '/media/heart-red.png');
        // $(this).parent().siblings().text(bbb+1);
      }else if($(this).attr('src') == '/media/heart-red.png') {
        $(this).attr('src', '/media/heart.png');
        // if(bbb != 0){
        //   $(this).parent().siblings().text(bbb-1);
        // }
      }else {
      };
      var aThis = this;
      $.ajax({
        type: 'POST',
        url: '/post/like/',
        data: {
          'i':$(this).attr('psi'),
          'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        success: function(data, textStatus, jqXHR){
          $(aThis).parent().siblings().text(data)
        },
        dataType: 'text'
      })
    }
    $('.like_img').click(function(){
      if($(this).attr('src') == '/media/heart.png'){
        $(this).attr('src', '/media/heart-red.png');
        // $(this).parent().siblings().text(bbb+1);
      }else if($(this).attr('src') == '/media/heart-red.png') {
        $(this).attr('src', '/media/heart.png');
        // if(bbb != 0){
        //   $(this).parent().siblings().text(bbb-1);
        // }
      };

      var aThis = this;
      $.ajax({
        type: 'POST',
        url: '/post/like/',
        data: {
          'i':$(this).attr('psi'),
          'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        success: function(data, textStatus, jqXHR){
          $(aThis).parent().siblings().text(data)
        },
        dataType: 'text'
      });
    })

})

var likeload = function(){
  if($(this).attr('src') == '/media/heart.png'){
    $(this).attr('src', '/media/heart-red.png');
    // $(this).parent().siblings().text(bbb+1);
  }else if($(this).attr('src') == '/media/heart-red.png') {
    $(this).attr('src', '/media/heart.png');
    // if(bbb != 0){
    //   $(this).parent().siblings().text(bbb-1);
    // }
  }else {
  };
  var aThis = this;
  $.ajax({
    type: 'POST',
    url: '/post/like/',
    data: {
      'i':$(this).attr('psi'),
      'csrfmiddlewaretoken': getCookie('csrftoken')
    },
    success: function(data, textStatus, jqXHR){
      $(aThis).parent().siblings().text(data)
    },
    dataType: 'text'
  })
}
$('.like_img').click(function(){
  if($(this).attr('src') == '/media/heart.png'){
    $(this).attr('src', '/media/heart-red.png');
    // $(this).parent().siblings().text(bbb+1);
  }else if($(this).attr('src') == '/media/heart-red.png') {
    $(this).attr('src', '/media/heart.png');
  }
    // if(bbb != 0){
    //   $(this).parent().siblings().text(bbb-1);
    // }
  });
