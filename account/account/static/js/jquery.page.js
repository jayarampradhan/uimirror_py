/*
 * <p>This is the main function for all the functionality of Page 
 * API
 * 
 */
;
$.fn.uipage = function(options) {
	"use strict";

	var uipageOpts = $.extend({}, $.fn.uipage.defaults, options);

	// define global vars for the function
	var flags = {
		wrap : "",
		hidden_class : 'hidden',
		elm_to_fade_out : '',
		elm_to_fade_in : '',
		df_easing : 'linear'
	};

	// each Page will execute this function
	this.each(function() {

		flags.wrap = $(this);

		// Update day inetrval
		// nextInterval();

	});

	// on click of inside page
	flags.wrap.find('#pagecontainer').on('click', '.thumbnail-box', function(e) {
		e.preventDefault();
		var $this = $(this);
		var $elm_to_up = $this.next();
		var $par = $this.parent().parent();
		var $elm_to_hide = $par.find('.open');
		var $elm_to_down = $this;
		$elm_to_up.animate({
			top : '0px'
		}, 200, function() {
			$elm_to_down.animate({
				top : '-275px'
			}, 200, function() {
				$elm_to_down.addClass('open');
			});
		});
		if ($elm_to_hide.is('div')) {
			$elm_to_hide.animate({
				top : '0px'
			}, 200, function() {
				$elm_to_hide.removeClass('open');
			});
			$elm_to_hide.next().animate({
				top : '275px'
			}, 200, function() {
			});
		}

	});
};

// define the parameters with the default values of the function
$.fn.uipage.defaults = {
	dfltFadoutTime : 200,
	dfltFadinTime : 200,
};
