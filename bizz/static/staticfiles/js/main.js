(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
	var isVisible = $( "#main-logo" ).is( ":visible" );
    if (isVisible){
    $('#main-logo').hide();
          $('#small-logo').show();

    }
    else{
         $('#small-logo').hide();
        $('#main-logo').show();
    }
      $('#sidebar').toggleClass('active');


  });

})(jQuery);


