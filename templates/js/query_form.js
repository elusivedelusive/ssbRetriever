"use strict";

ckan.module('query_form', function($, _) {
  return {
    initialize: function(){

	this.el.popover({title: "url", content: this.options.url , placement: 'left'});
    }
  };
});
