/*
 * Library for the drop down menu.
 * Customization of .dropit plug-in from https://github.com/gilbitron/Dropit
 * Copyright 2014, UiMirror
 */
;
(function($) {
	// Default settings
	var DEFAULT_SETTINGS = {
		action : 'click', // The open action for the trigger
		submenuEl : 'ul', // The submenu element
		triggerEl : 'button', // The trigger element
		triggerParentEl : 'div', // The trigger parent element
		optionsEl : 'li', // The option element inside submenu
		afterLoad : null, // Triggers when plugin has loaded
		beforeShow : null, // Triggers before submenu is shown
		afterShow : null, // Triggers after submenu is shown
		beforeHide : null, // Triggers before submenu is hidden
		afterHide : null, // Triggers before submenu is hidden
		showselectedmark : true, //Show Selected mark on the item already selected
		onSelect : null,//Triggers when element selected
		insideNavClass : 'seeall',
		backNavClass : 'goback',
		//Modification for short started
		primary_option_class : 'primaryOption',
		secondary_option_class : 'secondaryOption',
		select_class : 'selected',
		checked_class : 'checked',
		data_serach_attr : 'data-label',
		nav_serach_attr : 'data-label',
		toggler_btn_selector : '>a.uiButton',
	};

	// Default name Spaces
	var DEFAULT_NAME_SPACE = {
		SUBMENU : 'dropit-submenu',
		DROP : 'dropit',
		DROP_OPEN : 'dropit-open',
		TRIGGER : 'dropit-trigger',
		MENU_ITEM_RADIO : 'uiMenuItemRadio',
		MENU_ITEM : 'menuItem',
		OPEN_TOGGLER : 'openToggler',
		TOGGLE : 'uiToggle',
		SEPRATOR : 'optionseprator',
	};

	var methods = {
		init : function(options) {
			var settings = $.extend({}, DEFAULT_SETTINGS, options || {});
			return this.each(function() {
				$(this).data("settings", settings);
				$(this).data("dropDownObject", new $.DropDown(this, settings));
			});

		},
		destroy : function() {
			if (this.data("dropDownObject")) {
				var _elm = $(this.data("dropDownObject"));
				_elm.removeClass($(this).data("settings").namespace.NAVIGATABLE);
				_elm.find('>.' + $(this).data("settings").namespace.NAVIGATE)
						.removeClass(
								$(this).data("settings").namespace.NAVIGATE)
						.off('keydown mouseenter mouseleave click');
				this.data("dropDownObject", '');
				this.data("settings", '');
				return this;
			}
		}

	};
	$.fn.uimdrop = function(method) {
		// Method calling and initialization logic
		if (methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method "' + method+ '" does not exist in uimdrop plugin!');
		}
	};
	// Drop Down For each element
	$.DropDown = function(_elm, settings) {

		//
		// Initialization
		//
		// Build Common NameSpaces
		var SETTINGS = "settings";
		if ($(_elm).data(SETTINGS).namespace) {
			// Use custom NameSpaces
			$(_elm).data(SETTINGS).namespace = $.extend({}, DEFAULT_NAME_SPACE, $(_elm).data(SETTINGS).namespace);
		} else {
			$(_elm).data(SETTINGS).namespace = DEFAULT_NAME_SPACE;
		}
		
		var _submenu = $(_elm).addClass('dropit')
						.parent('.dropdown').addClass('dropitWrap dropItClose')
						.find('>ul.dropdown-menu').addClass('dropitToggelWrap');
		var $_elm = $(_elm);
		var _items = _submenu.find('>li[role=drop-item]');
				
		//If No Element for drop down
		if (!_items.exists())
			return false;

//		_items.addClass($_elm.data(SETTINGS).namespace.MENU_ITEM_RADIO+' '+$_elm.data(SETTINGS).namespace.MENU_ITEM);
//		_submenu.find($_elm.data(SETTINGS).optionsEl + ':empty')
//				.removeClass($_elm.data(SETTINGS).namespace.MENU_ITEM_RADIO)
//				.addClass($_elm.data(SETTINGS).namespace.SEPRATOR);
		console.log(_items.filter( "[data-role-pri='second']" ));
		_items.filter( "[data-role-pri='second']" ).addClass('hidden');
		//If Primary and seconadry mark marked
//		if ($_elm.data(SETTINGS).primary_option_class && $_elm.data(SETTINGS).secondary_option_class) {
//			var _seprator = _submenu.find($_elm.data(SETTINGS).optionsEl + '.' + $_elm.data(SETTINGS).insideNavClass);
//			
//			if (_seprator.exists()) {
//				_seprator.addClass($_elm.data(SETTINGS).primary_option_class);
//				var _sep_index = _items.index(_seprator);
//				_submenu.find($_elm.data(SETTINGS).optionsEl + ':gt('+ _sep_index + ')')
//						.addClass($_elm.data(SETTINGS).secondary_option_class + ' hidden');
//				_submenu.find($_elm.data(SETTINGS).optionsEl + ':lt('+ _sep_index + ')')
//						.addClass($_elm.data(SETTINGS).primary_option_class);
//			}
//		}
		
		//Hide all the open drop down
		var hideAllDrop = function(){
			if($_elm.exists()
					&& $_elm.data(SETTINGS) 
					&& $_elm.data(SETTINGS).select_class 
					&& $_elm.data(SETTINGS).namespace 
					&& $_elm.data(SETTINGS).namespace.DROP_OPEN){
				var _elm_to_hide = $('.'+$_elm.data(SETTINGS).namespace.DROP_OPEN);
				$('.'+$_elm.data(SETTINGS).namespace.DROP_OPEN)
					.removeClass($_elm.data(SETTINGS).namespace.DROP_OPEN)
					.find('>.'+$_elm.data(SETTINGS).namespace.OPEN_TOGGLER)
					.removeClass($_elm.data(SETTINGS).namespace.OPEN_TOGGLER)
					.find('>.'+$_elm.data(SETTINGS).select_class)
					.removeClass($_elm.data(SETTINGS).select_class)
					.find('>.'+$_elm.data(SETTINGS).namespace.SUBMENU).hide();
				if ($.isFunction($_elm.data(SETTINGS).afterHide) && _elm_to_hide.exists()) {
					$_elm.data(SETTINGS).afterHide.call(this, _elm_to_hide);
		        }
			}
			
		}
		
		var handelLeft = function(_curr){
			var _nav_to = getBackOrForward(_curr);
			if(!_nav_to)return false;
			if(_nav_to === $_elm.data(SETTINGS).backNavClass){
				doOptionSwap(_curr, _nav_to);
			}
			
		};
		
		var handelRight = function(_curr){
			var _nav_to = getBackOrForward(_curr);
			if(!_nav_to)return false;
			if(_nav_to === $_elm.data(SETTINGS).insideNavClass){
				doOptionSwap(_curr, _nav_to);
			}
		};
		
		function handelSelect(_this){
			var _nav_to = getBackOrForward(_this);
			if(_nav_to){
				doOptionSwap(_this, _nav_to);
			}else{
				if ($.isFunction($_elm.data(SETTINGS).onSelect)) {
		            $_elm.data(SETTINGS).onSelect.call(this, _this);
		        }
				hideAllDrop();
			}
		}
		function getBackOrForward(_curr){
			var _label = _curr.attr($_elm.data(SETTINGS).data_serach_attr);
			if(typeof _label === 'undefined' || _label === false){
				_label = _curr.attr($_elm.data(SETTINGS).nav_serach_attr);
				if($_elm.data(SETTINGS).backNavClass.toLowerCase() === UIMIRRORUTILITY.replaceAllSpace(_label).toLowerCase()){
					return $_elm.data(SETTINGS).backNavClass;
				}else if($_elm.data(SETTINGS).insideNavClass.toLowerCase() === UIMIRRORUTILITY.replaceAllSpace(_label).toLowerCase()){
					return $_elm.data(SETTINGS).insideNavClass;
				}
			}else{
				return false;
			}
		}
		
		//It will swap the show the primary options / secondary option
		function doOptionSwap(_this, _nav_to) {
			var _parent = _this.parent(), 
				optn_elm = $_elm.data(SETTINGS).optionsEl, 
				_prm_label = $_elm.data(SETTINGS).primary_option_class, 
				_secondary_label = $_elm.data(SETTINGS).secondary_option_class, 
				_slct_class = $_elm.data(SETTINGS).select_class, 
				_prm_elm = _parent.find(optn_elm + '.'+_prm_label), 
				_second_elm = _parent.find(optn_elm + '.'+ _secondary_label);
			if(_nav_to === $_elm.data(SETTINGS).insideNavClass){
				_prm_elm.addClass('hidden');
				_second_elm.removeClass('hidden');
				UIMIRRORUTILITY.focus_with_timeout(_second_elm.eq(0));
			}else if(_nav_to === $_elm.data(SETTINGS).backNavClass){
				_prm_elm.removeClass('hidden');
				_second_elm.addClass('hidden');
				UIMIRRORUTILITY.focus_with_timeout(_prm_elm.eq(0));
			}
		}
		
		// Open on click
		$_elm.on($_elm.data(SETTINGS).action, function(e) {
			var $this = $(this).addClass('active'), 
				_parent_trg_elm = $this.parent('.dropitWrap').removeClass('close');
			
			if (_parent_trg_elm.hasClass('open'))
				return false;
			
			_parent_trg_elm.addClass('open');
			if ($.isFunction($_elm.data(SETTINGS).beforeShow)) {
	            $_elm.data(SETTINGS).beforeShow.call(this,$_elm);
	        }
			var _drop_wrap = _parent_trg_elm.find('>ul.dropdown-menu');
			
			//Mark the toggller as selected
//			$this.addClass($_elm.data(SETTINGS).namespace.OPEN_TOGGLER)
//				.find($_elm.data(SETTINGS).toggler_btn_selector)
//				.addClass($_elm.data(SETTINGS).select_class);
			
			//Selected mark needs to show, so have to iterate over the elements to show
			var _cur_val = $this.attr('data-val');
			console.log(_cur_val);
			showMenuAndMarkSelected(_drop_wrap, _cur_val);
			
			_parent_trg_elm.addClass($_elm.data(SETTINGS).namespace.DROP_OPEN);
			_drop_wrap.show();
			if ($.isFunction($_elm.data(SETTINGS).afterShow)) {
	            $_elm.data(SETTINGS).afterShow.call();
	        }
			return false;
		});
		
		//On Select drop down, return
		$_elm.on('click', '.'+$(_elm).data(SETTINGS).namespace.SUBMENU, function(e) {
			return false;
		});
		// Close if outside click
		$(document).on('click', function(e) {
			hideAllDrop();
		});

		//This will be called when option of show selected marked
		function showMenuAndMarkSelected(_options, curr_val) {
			_options.addClass('noSelectMark');
			_options.each(function() {
				var current = $(this);
				var _data_label = current.find('>a').attr('data-val');
				if (typeof _data_label != "undefined"
						&& _data_label.length > 0
						&& _data_label.toLowerCase() === curr_val.toLowerCase()) {
					current.removeClass('noSelectMark');
					return false;
				}
			});
//			var optn_elm = $_elm.data(SETTINGS).optionsEl, 
//				_chkd_class = $_elm.data(SETTINGS).checked_class, 
//				_slct_class = $_elm.data(SETTINGS).select_class, 
//				_search_attr = $_elm.data(SETTINGS).data_serach_attr, 
//				_options = _drop_wrap.find(optn_elm+'.'+$_elm.data(SETTINGS).namespace.MENU_ITEM);
//			if ($_elm.data(SETTINGS).showselectedmark && curr_val.length > 0) {
//				//Remove the already selected element
//				_drop_wrap.find(optn_elm + '.' + _chkd_class)
//						   .removeClass(_chkd_class);
//				
//				_options.each(function() {
//					var current = $(this);
//					var _data_label = current.attr(_search_attr);
//					if (typeof _data_label != "undefined"
//							&& _data_label.length > 0
//							&& _data_label.toLowerCase() === curr_val.toLowerCase()) {
//						current.addClass(_chkd_class);
//						return false;
//					}
//				});
//			}
			UIMIRRORUTILITY.focus_with_timeout(_options.eq(0));
		};
		
		var navigable_property = {
				_select_class : $_elm.data(SETTINGS).select_class,
				afterLeft: handelLeft,
				afterRight: handelRight,
				afterEnter: handelSelect,
				afterClick: handelSelect,
				afterEscape: hideAllDrop,
		};
		//Navigate 
		_submenu.uimNavigable(navigable_property);

		if ($.isFunction($_elm.data(SETTINGS).afterLoad)) {
            $_elm.data(SETTINGS).afterLoad.call(this, $_elm);
        }

	};

})(jQuery);