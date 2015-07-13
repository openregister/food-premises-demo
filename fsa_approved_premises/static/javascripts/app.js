var fetchRecords = function(input) {
    var searchTerm = input.value;
    if(searchTerm.length >= 3) {
        doSearch(searchTerm)
    } else {
        reload();
    }
}

var doSearch = function(searchTerm) {
    $.ajax({
      type: 'GET',
      url: "/search?query="+searchTerm,
      success: function(data) {
        $('#premises-list').empty();
        $('#count').text(data.entries.length);
        $.each(data.entries, function(index, item){
            var item = $('<li><a href="#">'+ item.entry.name +'</a></li>');
            $('#premises-list').append(item);
        });
      },
      error: function(){
        console.log("error");
      }
    });
};

var reload = function() {
    $.ajax({
      type: 'GET',
      url: "search",
      success: function(data) {
        $('#premises-list').empty();
        $('#count').text(data.meta.total_entries);
        $.each(data.entries, function(index, item) {
            var item = $('<li><a href="#">'+ item.entry.name +'</a></li>');
            $('#premises-list').append(item);
        });
      },
      error: function(){
        console.log("error");
      }
    });
};

var pager = function(event) {
  event.preventDefault();
  var searchTerm = $('#search')[0].value,
    page = $('#page-number').text();
  $.ajax({
    type: 'GET',
    url: "/search?query="+searchTerm+"&page="+page,
    success: function(data) {
      $('#premises-list').empty();
      $('#count').text(data.meta.total_entries);
      $('#page-number').text(data.meta.page+1);
      $.each(data.entries, function(index, item) {
          var item = $('<li><a href="#">'+ item.entry.name +'</a></li>');
          $('#premises-list').append(item);
      });
    },
    error: function(){
      console.log("error");
    }
  });
};


$(document).ready(function() {
    $('#search').on('keyup', function(event) {
      fetchRecords(event.currentTarget);
    });
    $('#pager').on('click', pager);
});
