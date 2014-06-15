/*
 * jQuery Plugin: Privacy Builder
 * Version 0.0.1
 *
 * Copyright (c) 2014 UIMirror
 *
 */
;(function ($) {

  // Default settings
  var DEFAULT_SETTINGS = {
		  _data: {},
		  toggle_tip: true,
		  data_from_url: false,
		  default_data: [
				         {"_class":"friends","title":"Friends", "value":"Friends", "_id":"1"},
				         {"_class":"friends","title":"Public", "value":"Friends", "_id":"2"},
				         {"_class":"friends","title":"Friends Of Friend", "value":"Friends", "_id":"3"},
				         {"_class":"friends","title":"Only Me", "value":"Friends", "_id":"4"},
				         {},
				         {"label":"seeall", "value":"See All"},
				         {"_class":"friends","title":"friends", "value":"Friends", "_id":"5"},
				         {"_class":"friends","title":"friends", "value":"Friends", "_id":"6"},
				         {"_class":"friends","title":"friends", "value":"Friends", "_id":"7"},
				         {"_class":"friends","title":"friends", "value":"Friends", "_id":"8"},
				         {},
				         {"label":"goback", "value":"Go Back"},
				       ],
		  tmpl_info: {
			  "name": "privacy_drop",
		  },
		  _id_prefix: 'uim_prv_',
		  _current: '',
		  _is_drop_down: true,
  };

  // Default name Spaces
  var DEFAULT_NAME_SPACE = {
    TOOL_TIP_CLASS  : 'uimtpd',
    WRAP: 'prvbuilder',
    _DATA_ATR_ID_REF: 'data-prv-ref',
  };

  // Additional public (exposed) methods
  var methods = {
      init: function(_data, options) {
          var settings = $.extend({}, DEFAULT_SETTINGS,_data, options || {});
          return this.each(function () {
              $(this).data("settings", settings);
              $(this).data("privacyObject", new $.Privacy(this, settings));
          });
      },
      destroy: function () {
        if (this.data("privacyObject")) {
        	var _elm = $(this.data("privacyObject"));
        	var _privacy_elm = $(this).next();
			if(_privacy_elm.exists() && _privacy_elm.hasClass($(this).data("settings").namespace.WRAP))
				_privacy_elm.remove();
			this.data("privacyObject", '');
			return this;
        }
      }
  };

  // Expose the .privacy builder function to jQuery as a plugin
  $.fn.privacy = function (method) {
      // Method calling and initialization logic
      if(methods[method]) {
          return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
      } else {
          return methods.init.apply(this, arguments);
      }
  };

  // Privacy For each element
  $.Privacy = function (_elm, settings) {
	  $(_elm).hide();
	  //
      // Initialization
	  var _id =  $(_elm).data("settings")._id_prefix+_elm.id;
      //
	  // Build Common NameSpaces
      if($(_elm).data("settings").namespace) {
          // Use custom NameSpaces
          $(_elm).data("settings").namespace = $.extend({}, DEFAULT_NAME_SPACE, $(_elm).data("settings").namespace);
      } else {
          $(_elm).data("settings").namespace = DEFAULT_NAME_SPACE;
      }
      $(_elm).attr($(_elm).data("settings")._DATA_ATR_ID_REF, _id);
      $(_elm).data("settings")._DATA_ATR_ID_REF = _id;
      
      //Now Cache the elem as its all data settings done
      var $_elm = $(_elm);
      //If there is no current selection then destroy this plugin
      if($_elm.data("settings")._current === "undefined" || $_elm.data("settings")._current === null || $_elm.data("settings")._current.length === 0){
    	  $_elm.privacy('destroy');
    	  return false;
      }
      //CallBack to update the result into DOM
      var applyToolTip = function(_elm){
    	  if(!$_elm.data("settings").toggle_tip){
    		  return false;
    	  }
    	  if(_elm.hasClass($_elm.data("settings").namespace.TOOL_TIP_CLASS)){
    		  UIMIRRORUTILITY.applyTip(_elm);
    	  }
    	  UIMIRRORUTILITY.applyTip(_elm.find('.'+$_elm.data("settings").namespace.TOOL_TIP_CLASS));
    	  return false;
      };
      var disableToolTip = function(_elm){
    	  if(!$_elm.data("settings").toggle_tip){
    		  return false;
    	  }
    	  if(_elm.hasClass($_elm.data("settings").namespace.TOOL_TIP_CLASS)){
    		  UIMIRRORUTILITY.hideAndDisableToolTip(_elm);
    	  }
    	  UIMIRRORUTILITY.hideAndDisableToolTip(_elm.find('.'+$_elm.data("settings").namespace.TOOL_TIP_CLASS));
    	  //$_elm.privacy('destroy');//Destroy testing for this plugin
    	  return false;
      };
      var enableToolTip = function(_elm){
    	  if(!$_elm.data("settings").toggle_tip){
    		  return false;
    	  }
    	  if(_elm.hasClass($_elm.data("settings").namespace.TOOL_TIP_CLASS)){
    		  UIMIRRORUTILITY.enableToolTip(_elm);
    	  }
    	  UIMIRRORUTILITY.enableToolTip(_elm.find('.'+$_elm.data("settings").namespace.TOOL_TIP_CLASS));
    	  return false;
      };
      var selectFromDropDown = function(_elm){
    	  var _parent = _elm.parents('.dropit-trigger');
    	  var _curr_id = _parent.attr('data-pr-id');
    	  var _selected_id = _elm.attr('data-pr-id');
    	  if(typeof _selected_id !== 'undefined' && _selected_id !== false && _selected_id !== _curr_id){
    		  var _curr_class = _parent.attr('data-pr-class');
    		  var _class = _elm.attr('data-pr-class');
    		  var _title = _elm.attr('data-title');
    		  var _value = _elm.attr('data-value');
    		  _parent.find('>a>i')
    		  			.removeClass('im_v_'+_curr_class)
    		  			.addClass('im_v_'+_class);
    		  _parent.attr('data-pr-id', _selected_id);
    		  _parent.attr('title', _title);
    		  _parent.attr('data-pr-class', _class);
    		  _parent.attr('data-pr-title', _title);
    		  _parent.attr('data-pr-value', _value);
    	  }
      }
      var updatePrivacyDom = function(_privacy){
    	  if($_elm.data("settings")._is_drop_down){
    		  _privacy.uimdrop({
    			  afterLoad : applyToolTip,
    			  beforeShow: disableToolTip,
    			  afterHide:  enableToolTip, 
    			  onSelect: selectFromDropDown,
    			  data_serach_attr: 'data-pr-id',
    		  });
    	  }
    	  _privacy.addClass($_elm.data("settings").namespace.WRAP);
    	  _privacy.insertAfter($_elm);
      };
      
      //This will build the template rendering
      var buildTemplate = function(){
    	  //Call template render with time out
    	  setTimeout(function() { new UIMTemplateutil($(_elm).data("settings")._data, updatePrivacyDom).renderExtTemplate(); }, 50);
      }
      
      // Configure the data source
	  var _buid_data = function(_data){
		  _data = _data || $_elm.data("settings").default_data;
		  _tmpl_data = $_elm.data("settings")._data || {};
		  _tmpl_data["name"] = $_elm.data("settings").tmpl_info.name;
		  _tmpl_data["data"] = {};
		  _tmpl_data.data["_id"] = $_elm.data("settings")._DATA_ATR_ID_REF;
		  _tmpl_data.data["current"] = $_elm.data("settings")._current;
		  _tmpl_data.data["options"] = _data;
		  $(_elm).data("settings")._data = _tmpl_data;
		  $_elm = $(_elm);
		  //Now Build Template
		  buildTemplate();
	  }
      
      //Configure the data source and build the available object
	  if($(_elm).data("settings").data_from_url){
		  //TODO get the data from the ajax call using $.getJSON()
		  //with timeout and call _buid_data with the response got from url
	  }else{
		  _buid_data(false);
	  }
      
  };

}(jQuery));
