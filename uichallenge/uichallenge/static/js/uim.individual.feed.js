var UIM = (function($, CHALLENGEINDFEED) {
	var challengeFeedPageLet,
		challengeFeed;
	
	function applyHidden(_elm) {
		return _elm.addClass('hidden');
	}
	function removeHidden(_elm) {
		return _elm.removeClass('hidden');
	}
	function addClass(_elm, _class){
		return _elm.addClass(_class);
	}
	function removeClass(_elm, _class){
		_elm.removeClass(_class)
	}
	function toggelIndividualFeedView(_self){
		challengeFeed.find('.challenge').removeClass(_self.data('remove-class')).addClass(_self.data('apply-class'));
		$(_self.addClass('hidden').data('show-next')).removeClass('hidden')
	};
	function applyClamp(){
		$('.clampIt').each(function() {
			var options = {},
				_self = $(this);
			options.clamp = _self.data('clmap');
			if(options.clamp != undefined && options.clamp != ""){
				$clamp(_self[0], options);
			}
		 });
	}
	CHALLENGEINDFEED.addHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(applyHidden);
	};
	CHALLENGEINDFEED.removeHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(removeHidden);
	};
	CHALLENGEINDFEED.focusWithTimeOut = function(obj){
		setTimeout(function() { obj.focus(); }, 50);
	};
	CHALLENGEINDFEED.initChallengeIndividualFeedStep = function(){
		var _body = $('body');
		if(_body.attr('data-js_uim_challenge_feed_step') === 'applied'){
			return false;
		}
		setTimeout(function() {
			challengeFeedPageLet = $('#challengeIndividualFeedPageLet');
			challengeFeed = $('#challengeIndividualFeedPageLet').find('#challenges');
			$('#listOrGridViewToggler').on('click', '.listOrGridView', function(e){
				e.preventDefault();
				toggelIndividualFeedView.call(this, $(this));
			});
			//Apply CLamp on element
			applyClamp.call();
		}, 50);
		_body.attr('data-js_uim_challenge_feed_step', 'applied');
	};
	return CHALLENGEINDFEED;
}(jQuery.noConflict(), UIM || {})); 

/* Define dummy gettext if Django's javascrip_catalog is not being used */
if (typeof gettext != 'function') {
    window.gettext = function(text) {
        return text;
    };
}

+function ($) { "use strict";
	UIM.initChallengeIndividualFeedStep();
}(window.jQuery);
/*Test*/
var $ = jQuery.noConflict();           
$(document).ready(function() {
//	$('#importFromGoogle').on('click', function(e){
//		$('#invitationContactWrap').modal('show')
//	});
});
