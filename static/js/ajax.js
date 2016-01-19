$(function(){
    $('#search').keyup(function(){
        if($('#search').val() != ''){
            $.ajax({
                type: 'POST',
                url: "/search/",
                data: {
                    'search_text': $('#search').val(),
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
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
  $('.more_posts').click(function(){
    $.ajax({
      type: 'POST',
      url: '/loadmore/',
      data: {
        'p':page,
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
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
