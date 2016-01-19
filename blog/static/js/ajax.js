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

    $('#search').keyup(function(){
        if($('#search').val() != ''){
            $.ajax({
                type: 'POST',
                url: "http://localhost:8000/search/",
                data: {
                    'search_text': $('#search').val(),
                    'csrfmiddlewaretoken': getCookie('csrftoken')
                },
                success: searchSuccess,
                dataType: 'html'
            });
        } else {
            $('.triangle').css('display', 'none');
            $('.search-results').hide();
        }
    });
});

function searchSuccess(data, textStatus, jqXHR)
    {
        $('.triangle').css('display', 'inline-block');
        $('.search-results').show();
        $('#search-results').html(data);
    }

var page = 2;

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

  $('.more_posts').click(function(){
    $.ajax({
      type: 'POST',
      url: '/loadmore/',
      data: {
        'p':page,
        'csrfmiddlewaretoken': getCookie('csrftoken')
      },
      success: moreLoadSuccess,
      dataType: 'html'
    })
  })
})

function moreLoadSuccess(data, textStatus, jqXHR){
  $('.ul-catalog').append(data)
  page = page + 1
}
