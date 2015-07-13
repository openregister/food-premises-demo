var fetchRecords = function(input) {
    var searchTerm = input.value;
    if(searchTerm.length >= 3) {
        console.log('do a search');
        doSearch(searchTerm)
    } else {
        reload();
    }
}

var doSearch = function(searchTerm) {
    $.ajax({
      type: 'GET',
      url: "http://premises.openregister.org/search?_representation=json&_query="+searchTerm,
      success: function(data) {
        $('#premises-list').empty();
        $('#count').text(data.entries.length);
        $.each(data.entries, function(index, item){
            console.log(item.entry);
            var item = $('<li>'+ item.entry.name +'</li>');
            $('#premises-list').append(item);
        });
      },
      error: function(){
        console.log("error");
      }
    });
};

var reload = function() {
    console.log('reload all');
    $.ajax({
      type: 'GET',
      url: "http://premises.openregister.org/search?_representation=json",
      success: function(data) {
        $('#premises-list').empty();
        $('#count').text(data.meta.total_entries);
        $.each(data.entries, function(index, item){
            console.log(item.entry);
            var item = $('<li>'+ item.entry.name +'</li>');
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
});
