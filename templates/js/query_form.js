ckan.module('query_form', function($, _) {
    return {
        initialize: function() {
	    	var showingQuery = false;
        	$('#form-toggle').on('click', function() {
			if(showingQuery){
				document.getElementById('field-query-url').value = "";
				document.getElementById('field-query-text').value = "";
				document.getElementById('field-image-url').value = " ";
				$('#query-inputs').hide();
				$('.image-upload').show();
				showingQuery = false;
			} else {
				$('#field_image_url').val("query");
				document.getElementById('field-image-url').value = " ";
				$('#query-inputs').show();
				$('.image-upload').hide();
				showingQuery = true;
			}
        	});
    	}
    };
});
