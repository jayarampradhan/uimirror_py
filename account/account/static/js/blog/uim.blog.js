var UIM = (function($, BLOG) {
	var _inprogress= 'inprogress';
	
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
	function stopLoadingIcon(_elm){
		UIM.addHiddenCLass.apply(this,[_elm]);
	}
	function showLoadingIcon(_elm){
		UIM.removeHiddenCLass.apply(this,[_elm]);
	};
	function buildLocTokenProperty(_placeholder){
		var _prop = {};
		_prop.propertyToSearch = gettext('location');
		_prop.resultsFormatter =  function(item){ return "<li>" + "<div class='row no_margin'><div class='location'>" + gettext(item.location)  + "</div></div></li>" };
		_prop.tokenFormatter = function(item) { return "<li>" +
				"<p data-id='"+item.id+"' data-lat='"+item.lat+"' dta-long='"+item.long+"'>" + gettext(item.name) + "</p>" +
				"</li>" };
		_prop.theme = 'uim';
		_prop.allowFreeTagging = false;
		_prop.tokenLimit = 1;
		_prop.placeholder = _placeholder;
		_prop.hintText = gettext('Type Locality city state...');
		_prop.searchingText = '<i class="ajxLoad loadRefresh"></i>';
		_prop.searchingIco = true; 
		return _prop; 
	};
	function applyTokenInput(_self){
		_self.uimTokenInput('destroy');
		_self.uimTokenInput(_self.attr('data-uri_loc'), buildLocTokenProperty.call(this,'Tags To Filter.'));
	};
	BLOG.addHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(applyHidden);
	};
	BLOG.removeHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(removeHidden);
	};
	BLOG.focusWithTimeOut = function(obj){
		setTimeout(function() { obj.focus(); }, 50);
	};
	BLOG.initBlog = function(){
		var _body = $('body');
		if(_body.attr('data-js_uim_blog_step') === 'applied'){
			return false;
		}
		setTimeout(function() {
			//Apply Token
			applyTokenInput.call(this,$('#tagsToFilter'));

		}, 50);
		_body.attr('data-js_uim_blog_step', 'applied');
	};
	return BLOG;
}(jQuery.noConflict(), UIM || {})); 

/* Define dummy gettext if Django's javascrip_catalog is not being used */
if (typeof gettext != 'function') {
    window.gettext = function(text) {
        return text;
    };
}

+function ($) { "use strict";
	UIM.initBlog();
}(window.jQuery);
/*Test*/
var $ = jQuery.noConflict();           
$(document).ready(function() {
//	$('#importFromGoogle').on('click', function(e){
//		$('#invitationContactWrap').modal('show')
//	});
});
