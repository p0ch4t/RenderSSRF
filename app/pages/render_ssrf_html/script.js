$(document).ready(function(e){
	      $('.search-panel .dropdown-menu').find('a').click(function(e) {
				e.preventDefault();
				var param = $(this).attr("href").replace("#","");
				var concept = $(this).text();
				$('.search-panel span#search_concept').text(concept);
				$('.input-group #search_param').val(param);
		   	});
	      });
var a = document.getElementByTagName('a').item(0);
$(a).on('keyup', function(evt){
  console.log(evt);
  if(evt.keycode === 13){
    
    alert('search?');
  } 
});