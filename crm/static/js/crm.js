/* for bootstrap select */ 
$('.selectpicker').selectpicker();


function searchOpen(thiss,url) {
    var search = $('#'+thiss.id).val()
    var data = {search: search};
    

    $.ajax({
        url: url+'list/',
        data: data,
        dataType: 'jsonp',
        jsonp: 'callback',
        jsonpCallback: 'searchResult'
    });
}


function searchResult(data) {
    $( "#txtSearch").autocomplete({
        source: data,
        select: function(event,ui){
            $("#txtSearch").val(ui.item.value);
            $("#srchform").submit()
        }
        
    });
}
/*$('table').footable({
  breakpoints: {
  }
});
$(document).ready(function(){
$("#my_act").append("<span> - 2nd!</span>"); 
});*/


