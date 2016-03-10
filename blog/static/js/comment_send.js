$(function(){
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

  // alert(getCookie('csrftoken'));

    $('.comment_send').click(function(){
          $.ajax({
              type: 'POST',
              url: "/comment/",
              data: {
                  'comment_text': $('#comment').val(),
                  'post': parseInt($(this).attr('psi')),
                  'csrfmiddlewaretoken': getCookie('csrftoken')
              },
              success: function(data, textStatus, jqXHR){
                $('.all_comments').append(data);
              },
              dataType: 'html'
          });
    });
});
