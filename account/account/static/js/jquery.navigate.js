/*
 * jQuery Plugin: Navigate standard DOM element
 * Version 0.0.1
 *
 * Copyright (c) 2014 UIMirror
 *
 */
;(function ($) {

	//Keys
	var KEY = {
			  BACKSPACE: 8,
			  TAB: 9,
			  ENTER: 13,
			  ESCAPE: 27,
			  SPACE: 32,
			  PAGE_UP: 33,
			  PAGE_DOWN: 34,
			  END: 35,
			  HOME: 36,
			  LEFT: 37,
			  UP: 38,
			  RIGHT: 39,
			  DOWN: 40,
			  NUMPAD_ENTER: 108,
			  COMMA: 188
			};
  // Default settings
  var DEFAULT_SETTINGS = {
		  _child_to_Navigate: 'li',
		  _skip_attr: 'class',
		  _skip_value: 'optionseprator',
		  _mouse_ignore_attr: 'class',
		  _mouse_ignore_value: 'optionseprator',
		  _ignore_attr: 'class',
		  _ignore_value: 'hidden',
		  _ignore_selector: '',
		  _skip_selector: '',
		  _mouse_ignore_selector: '',
		  _select_class: 'selected',
		  _stop_right_nav: true,
		  _stop_left_nav: true,
		  _listn_click:true,
		  _listn_enter:true,
		  _listen_escape:true,
		  beforeUp:false,
		  afterUp:false,
		  beforeDown:false,
		  afterDown:false,
		  beforeLeft:false,
		  afterLeft:false,
		  beforeRight:false,
		  afterRight:false,
		  beforeEnter:false,
		  afterEnter:false,
		  beforeClick:false,
		  afterClick:false,
		  beforeMouseEnter:false,
		  afterMouseEnter:false,
		  beforeMouseLeave:false,
		  afterMouseLeave:false,
		  beforeFoucs:false,
		  afterFocus:false,
		  beforeEscape:false,
		  afterEscape:false
  };

  // Default name Spaces
  var DEFAULT_NAME_SPACE = {
		  NAVIGATABLE : 'uiNavigable',
		  NAVIGATE : 'uiNavigate',
		  TABINDEX: 'tabindex'
  };

  // Additional public (exposed) methods
  var methods = {
      init: function(options) {
          var settings = $.extend({}, DEFAULT_SETTINGS, options || {});

          return this.each(function () {
              $(this).data("settings", settings);
              $(this).data("navigableObject", new $.Navigable(this, settings));
          });
      },
      destroy: function () {
        if (this.data("navigableObject")) {
        	var _elm = $(this.data("navigableObject"));
        	_elm.removeClass($(this).data("settings").namespace.NAVIGATABLE);
        	_elm.find('>.'+$(this).data("settings").namespace.NAVIGATE).removeClass($(this).data("settings").namespace.NAVIGATE).off('keydown mouseenter mouseleave click');
        	this.data("navigableObject" , '');
        	this.data("settings" , '');
        	return this;
        }
      }
  };

  // Expose the uimNavigable function to jQuery as a plugin
  $.fn.uimNavigable = function (method) {
      // Method calling and initialization logic
      if(methods[method]) {
          return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
      } else {
          return methods.init.apply(this, arguments);
      }
  };

  // Navigatable For each element
  $.Navigable = function (_elm, settings) {
      //
      // Initialization
      //
      // Build Common NameSpaces
      if($(_elm).data("settings").namespace) {
          // Use custom NameSpaces
    	  $(_elm).data("settings").namespace = $.extend({}, DEFAULT_NAME_SPACE, $(_elm).data("settings").namespace);
      } else {
    	  $(_elm).data("settings").namespace = DEFAULT_NAME_SPACE;
      }
      
      $(_elm).addClass($(_elm).data("settings").namespace.NAVIGATABLE);
      var _child = $(_elm).find($(_elm).data("settings")._child_to_Navigate);
      
      if(!_child.exists()){
    	  return;
      }
      _child.addClass($(_elm).data("settings").namespace.NAVIGATE);
      var _tab_attr = _child.attr('tabindex');
      if (!_tab_attr || typeof _tab_attr === 'undefined' || _tab_attr === false) {
    	  _child.each(function(index) {
    		  $(this).attr($(_elm).data("settings").namespace.TABINDEX, index);
    	  });
      }
      //Update the ignore selector
      if($(_elm).data("settings")._ignore_attr){
    	  $(_elm).data("settings")._ignore_selector = ($(_elm).data("settings")._ignore_attr === 'class') ? 
    			  ('.'+$(_elm).data("settings")._ignore_value) : ('['+$(_elm).data("settings")._ignore_attr+'="'+$(_elm).data("settings")._ignore_value+'"]');
	  }
      
      //Update the Mouse ignore selector
      if($(_elm).data("settings")._mouse_ignore_attr){
    	  $(_elm).data("settings")._mouse_ignore_selector = ($(_elm).data("settings")._mouse_ignore_attr === 'class') ? 
    			  ('.'+$(_elm).data("settings")._mouse_ignore_value) : ('['+$(_elm).data("settings")._mouse_ignore_attr+'="'+$(_elm).data("settings")._mouse_ignore_value+'"]');
	  }
      
      //Update the Skip selector
      if($(_elm).data("settings")._skip_attr){
    	  $(_elm).data("settings")._skip_selector = ($(_elm).data("settings")._skip_attr === 'class') ? 
    			  ('.'+$(_elm).data("settings")._skip_value) : ('['+$(_elm).data("settings")._skip_attr+'="'+$(_elm).data("settings")._skip_value+'"]');
	  }
      //Now cache the element as all data has been set
      var $_elm = $(_elm);
      
      $_elm.find('>.'+$_elm.data("settings").namespace.NAVIGATE).keydown(function (e) {
    	  var $this = $(this);
    	  var _key = e.which || e.keyCode;
    	  switch(_key) {
          	case KEY.LEFT:
          		if ($.isFunction($_elm.data("settings").beforeLeft)) {
          			$_elm.data("settings").beforeLeft.call(this,$this);
          		}
          		if(!$_elm.data("settings")._stop_left_nav){
          			handelLeft($this);
          			return false;
          		}
          		if ($.isFunction($_elm.data("settings").afterLeft)) {
          			$_elm.data("settings").afterLeft.call(this,$this);
          		}
          		break;
          	case KEY.RIGHT:
          		if ($.isFunction($_elm.data("settings").beforeRight)) {
          			$_elm.data("settings").beforeRight.call(this,$this);
          		}
          		if(!$_elm.data("settings")._stop_right_nav){
          			handelRight($this);
          			return false;
          		}
          		if ($.isFunction($_elm.data("settings").afterRight)) {
          			$_elm.data("settings").afterRight.call(this,$this);
          		}
          		break;
          	case KEY.UP:
          		if ($.isFunction($_elm.data("settings").beforeUp)) {
                    $_elm.data("settings").beforeUp.call(this,$this);
                }
          		var _prv = getPrevElement($this);
          		if(!_prv) return false;
          		markAsSelected(_prv);
          		if ($.isFunction($_elm.data("settings").afterUp)) {
                    $_elm.data("settings").beforeUp.call(this,_prv);
                }
          		return false;
          	case KEY.DOWN:
          		if ($.isFunction($_elm.data("settings").beforeDown)) {
                    $_elm.data("settings").beforeDown.call(this,$this);
                }
          		var _next = getNextElement($this);
          		if(!_next) return false;
          		markAsSelected(_next);
          		if ($.isFunction($_elm.data("settings").afterDown)) {
                    $_elm.data("settings").afterDown.call(this,_next);
                }
          		return false;
          	case KEY.ENTER:
          		if($_elm.data("settings")._listn_enter){
          			if ($.isFunction($_elm.data("settings").beforeEnter)) {
                        $_elm.data("settings").beforeEnter.call(this,$this);
                    }
          			//No Custom Implementation user has has to give
          			if ($.isFunction($_elm.data("settings").afterEnter)) {
                        $_elm.data("settings").afterEnter.call(this,$this);
                    }
          		}
          		break;
          	case KEY.ESCAPE:
          		if ($.isFunction($_elm.data("settings").beforeEscape)) {
          			$_elm.data("settings").beforeEscape.call(this,$this);
          		}
          		if($_elm.data("settings")._listen_escape){
          			unFocus($this);
          		}
          		if ($.isFunction($_elm.data("settings").afterEscape)) {
          			$_elm.data("settings").afterEscape.call(this,$this);
          		}
          		break;
    	  }
      })
      .on({
          mouseenter: function (e) {
        	  if ($.isFunction($_elm.data("settings").beforeMouseEnter)) {
                  $_elm.data("settings").beforeMouseEnter.call();
              }
        	  var _this = $(this),
        	  	  _mouse_ignore = ''+$_elm.data("settings")._mouse_ignore_selector;
        	  if(!_this.is(_mouse_ignore)){
        		  markAsSelected($(this));
        	  }
        	  if ($.isFunction($_elm.data("settings").afterMouseEnter)) {
                  $_elm.data("settings").afterMouseEnter.call();
              }
        	  return false;
          },
          mouseleave: function (e) {
        	  if ($.isFunction($_elm.data("settings").beforeMouseLeave)) {
                  $_elm.data("settings").beforeMouseLeave.call();
              }
          	  $(this).removeClass($_elm.data("settings")._select_class);
          	  if ($.isFunction($_elm.data("settings").afterMouseLeave)) {
          		  $_elm.data("settings").afterMouseLeave.call();
          	  }
          },
          click: function(e){
        	  if ($.isFunction($_elm.data("settings").beforeClick)) {
                  $_elm.data("settings").beforeClick.call(this,$(this));
              }
        	  if($_elm.data("settings")._listn_click){
        		  //No Implementation yet.
        	  }
        	  if ($.isFunction($_elm.data("settings").afterClick)) {
                  $_elm.data("settings").afterClick.call(this,$(this));
              }
          }
      });
      
      //Get the next element, first get all next till skip then filter with ignore
      function getNextElement(_curr){
    	  var _next_all = _curr.nextAll(),
    	  	  _elm_found = false,
    	  	  _this;
    	  if(!_next_all.exists()) return _elm_found;
    	  var _skip_selector = ''+$_elm.data("settings")._skip_selector;
		  var _ignore_selector = ''+$_elm.data("settings")._ignore_selector;
    	  _next_all.each(function(index) {
    		  _this = $(this);
    		  if(_skip_selector && _this.is(_skip_selector)){
    			  return true;
        	  }else if(_ignore_selector && _this.is(_ignore_selector)){
        		  return false;
        	  }
    		  _elm_found = _this;
    		  return false;
    	  });
    	  return _elm_found; 
      }
      
      //Get the Prev element, first get all Previous till skip then filter with ignore
      function getPrevElement(_curr){
    	  var _prev_all = _curr.prevAll(),
    	  	  _elm_found = false,
    	  	  _this;
    	  if(!_prev_all.exists()) return _elm_found;
    	  var _skip_selector = ''+$_elm.data("settings")._skip_selector;
		  var _ignore_selector = ''+$_elm.data("settings")._ignore_selector;
    	  _prev_all.each(function(index) {
    		  _this = $(this);
    		  if(_skip_selector && _this.is(_skip_selector)){
    			  return true;
        	  }else if(_ignore_selector && _this.is(_ignore_selector)){
        		  return false;
        	  }
    		  _elm_found = _this;
    		  return false;
    	  });
    	  return _elm_found; 
      }
      //Mark as selected
      function markAsSelected(_curr){
    	  var _parent = _curr.parent(),
    	  		_selected_class = ''+$_elm.data("settings")._select_class; 
          _parent.find('>.'+_selected_class).removeClass(_selected_class);
          _curr.addClass(_selected_class);
          if ($.isFunction($_elm.data("settings").beforeFoucs)) {
              $_elm.data("settings").beforeFoucs.call();
          }
          focus_with_timeout(_curr);
          if ($.isFunction($_elm.data("settings").afterFocus)) {
              $_elm.data("settings").afterFocus.call();
          }
      }
      
      function unFocus(_curr){
    	  var _parent = _curr.parent(),
	  		_selected_class = ''+$_elm.data("settings")._select_class;
    	  _parent.find('>.'+_selected_class).removeClass(_selected_class);
    	  blur_with_timeout(_curr.parent());
      }
      //This will take care Right Navigation
      function handelRight(_curr){
    	  var _next = getNextElement(_curr);
    	  if(!_next) return false;
    	  markAsSelected(_next);  
      }
      
      //This will take care Left Navigation
      function handelLeft(_curr){
    	  var _prv = getPrevElement(_curr);
    	  if(!_prv) return false;
    	  markAsSelected(_prv);  
      }
      
      function focus_with_timeout(obj){
		setTimeout(function() { obj.focus(); }, 50);
      };
      function blur_with_timeout(obj){
		setTimeout(function() { obj.blur(); }, 50);
      };
      return _elm; 
  };
  $.fn.exists = function () {
	    return this.length !== 0;
  }
}(jQuery));

