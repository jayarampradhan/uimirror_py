// Keys "enum"
//Element Enum
var ELM = {
	SPAN : 'span',
	UL   : 'ul',
	LI   : 'li',
	OL   : 'ol',
	DIV  : 'div',
	I    : 'i',
	A    : 'a',
	P    : 'p'
}

var ELM_ATTR = {
	TITLE : 'title',
	ID    : 'id'
}

var HTML_ESCAPE_CHARS = /[&<>"'\/]/g;
var HTML_ESCAPES = {
		  '&': '&amp;',
		  '<': '&lt;',
		  '>': '&gt;',
		  '"': '&quot;',
		  "'": '&#x27;',
		  '/': '&#x2F;'
		};

var LOCATION_URL = {
		URL: '/location/'
}



;UIMIRRORUTILITY = {
		/**
		 * <p>This will slide up the second element and slide down the first element.
		 * <p>Take the init step of hiding if any
		 */
		doFadeUpSwap: function($element1, $element2, interval, $elm_to_hide) {
			var HIDE = 'hidden';
			$element2.fadeOut( 'slow', function() {
				$element2.addClass( HIDE );
				$element1.fadeIn('slow', function(){
					if($elm_to_hide){
						$elm_to_hide.addClass( HIDE );
					}
					$element1.removeClass( HIDE );
				});
			});
		},
	   inactiveLink: function($elm){
		   $elm.on('click',function(e){
			   e.preventDefault();
		   });
	   },
	   markChecked: function($elm){
		   $elm.prop('checked', true);
	   },
	   cahngeTitle: function(text){
		   $(document).attr('title', text);
	   },
	   IsEmail: function(email) {
		   var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
		   return regex.test(email);
		 },
	   //Generate 32 char random uuid in case length is not defined
	   getUUID: function($len){
		   if(!$len){
			   $len = 32;
		   }
		   var uuid = ""
		   for (var i=0; i < $len; i++) {
			    uuid += Math.floor(Math.random() * 16).toString(16); 
		   }
		return uuid
	   },
	   coerceToString: function(val) {
		    return String((val === null || val === undefined) ? '' : val);
		},
		//Used for escape html
		_escapeHTML: function (text) {
		    return UIMIRRORUTILITY.coerceToString(text).replace(HTML_ESCAPE_CHARS, function(match) {
		      return HTML_ESCAPES[match];
		    });
		},
		//Used For applying Token Input
		apply_current_city_token: function(property, $element){
			$element.uimTokenInput(LOCATION_URL.URL, property);
		},
		focus_with_timeout: function(obj){
			setTimeout(function() { obj.focus(); }, 50);
		},
		blur_with_timeout: function(obj){
			setTimeout(function() { obj.blur(); }, 50);
		},
		//This will create a blank Element with class title id
		_blankelm: function(elm, _class, _title, _id){
			var _elm = $("<"+elm+"/>");
			if(typeof _class != "undefined" || _class != null){
				_elm.addClass(_class);
			}	
			if(typeof _title != "undefined" || _title != null){
				_elm.attr("title", _title);
			}
			
			if(typeof _id != "undefined" || _id != null){
				_elm.attr("id", _id);
			}
			return _elm;
		},
		//This will apply default tool tip
		//TODO work on this for a stalyish div
		applyTip: function(targetElement, _options){
			if(typeof _options === "undefined" || _options == null || !_options){
				_options = {
						hide: {
					        fixed: false,
					        delay: 300
					    },position: {
							target: 'mouse', // Use the mouse position as the position origin
							adjust: {
								// Don't adjust continuously the mouse, just use initial position
								mouse: false
							},
							my: 'bottom right',
							at: 'bottom right',
						},
						style: {
							classes: '_uim_context_boot _ui_context_shadow'
						}
					}
			}
			$(targetElement).uimtip(_options);
		},
		hideToolTip: function(elm){
			if(typeof elm === "undefined" || elm === null || elm === '')return false;
			var tip_plugin = elm.uimtip("api");
			if(typeof tip_plugin != "undefined"){
				tip_plugin.hide();
			}
		},
		hideAndDisableToolTip: function(elm){
			if(typeof elm === "undefined" || elm === null || elm === '')return false;
			var tip_plugin = elm.uimtip("api");
			if(typeof tip_plugin != "undefined"){
				tip_plugin.hide();
				tip_plugin.disable(true);
			}
		},
		enableToolTip: function(elm){
			if(typeof elm === "undefined" || elm === null || elm === '')return false;
			var tip_plugin = elm.uimtip("api");
			if(typeof tip_plugin != "undefined"){
				tip_plugin.hide();
				tip_plugin.disable(false);
			}
		},
		updateToolTip: function(elm, option){
			if(typeof elm === "undefined" || elm === null || elm === '')return false;
			var tip_plugin = elm.uimtip("api");
			if(typeof tip_plugin != "undefined" && option){
				tip_plugin.set(option);
			}
		},
		findNthParent: function($elm, nthpos){
			if($elm.length > 0 && nthpos >= 0){
				return $elm.parent().parents().eq(nthpos);
			}
		},
		replaceAllSpace: function(str){
			return str.replace(/\s+/g, '');
		},
		capitaliseFirstLetter: function(str){
			return str.charAt(0).toUpperCase() + str.slice(1);
		}
		
	}


//convert bytes into friendly format
function bytesToSize(bytes) {
    var sizes = ['Bytes', 'KB', 'MB'];
    if (bytes == 0) return 'n/a';
    var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
};
