+function ($) { "use strict";
//	$("#editaboutme").uimedit({
//		aftercall: function(elm){_aboutme_nw(elm)},
//		aftercancel: function(elm){_cancel_abtme_edit(elm);},
//		aftersubmit: function(elm){_save_abtme_edit(elm);},
//	});
	$('#popupmaincontent').on('click', '#editaboutme', function(e){
		e.preventDefault();
		_aboutme_nw($(this));
		
	});
	
	$('#popupmaincontent').on('click', '.edit_save', function(e){
		e.preventDefault();
		_save_abtme_edit($(this));
	});
	
	$('#popupmaincontent').on('click', '.edit_cancel', function(e){
		e.preventDefault();
		_cancel_abtme_edit($(this));
	});
	
	function _save_abtme_edit(_elm){
		var _row = UIMIRRORUTILITY.findNthParent(_elm, '1').addClass('hidden');
		UIMIRRORUTILITY.findNthParent(_elm, '2').removeClass('uimeditopen');
		var _prv_elm = _row.find('>div.extrainfo>ul>li>div.dropit-trigger');
		var _abt_me_elm = _row.find('>div.extrarow>#uim_abtme_i_edit');
		
		//console.log(_row.html());
		//Remember to have a check with old data //TODO latter
		var _data = buildSaveData(_prv_elm, _abt_me_elm);
		
		var updatePrivacyDom = function(_res){
			_row.empty();
			//Callable will go here.
			_row.html(_res);
			console.log(_row.find('#editaboutme'));
//			_row.find('#editaboutme').uimedit({
//				aftercall: function(elm){_aboutme_nw(elm)},
//				aftercancel: function(elm){_cancel_abtme_edit(elm);},
//				aftersubmit: function(elm){_save_abtme_edit(elm);},
//			});
			UIMIRRORUTILITY.applyTip(_row.find('.uimtpd'));
			_row.removeAttr('data-edit-field');
			_row.removeClass('hidden');
		}
		var buildTemplate = function(){
	    	  //Call template render with time out
	    	  setTimeout(function() { new UIMTemplateutil(_data, updatePrivacyDom).renderExtTemplate(); }, 50);
	    }
		buildTemplate();
	}
	
	function _cancel_abtme_edit(_elm){
		var _row = UIMIRRORUTILITY.findNthParent(_elm, '1').addClass('hidden');
		UIMIRRORUTILITY.findNthParent(_elm, '2').removeClass('uimeditopen');
		var _prv_elm = _row.find('>div.extrainfo>div#uim_abtme_prv_wr');
		var _abt_me_elm = _row.find('>div.extrarow>p.aboutMe');
		
		//console.log(_row.html());
		var _data = buildCancelData(_prv_elm, _abt_me_elm);
		
		var updatePrivacyDom = function(_res){
			_row.empty();
			//Callable will go here.
			_row.html(_res);
			UIMIRRORUTILITY.applyTip(_row.find('.uimtpd'));
			_row.removeAttr('data-edit-field');
			_row.removeClass('hidden');
		}
		var buildTemplate = function(){
	    	  //Call template render with time out
	    	  setTimeout(function() { new UIMTemplateutil(_data, updatePrivacyDom).renderExtTemplate(); }, 50);
	    }
		buildTemplate();
	}
	
	function _aboutme_nw(elm){
		//console.log(elm.html());
		UIMIRRORUTILITY.hideAndDisableToolTip(elm);
		var _row = UIMIRRORUTILITY.findNthParent(elm, '1').addClass('hidden');
		UIMIRRORUTILITY.findNthParent(elm, '2').addClass('uimeditopen');
		var _prv_elm = _row.find('>div.extrainfo>ul.extrawrap>li.prvactionWrap');
		var _abt_me_elm = _row.find('>div.extrarow>p.aboutMe');
		
		//console.log(_row.html());
		var _data = builCurrentData(_prv_elm, _abt_me_elm);
		
		var updatePrivacyDom = function(_res){
			$(_res[4]).find('#uim_abtme_i_edit').autosize();
			$(_res[0]).find('#uim_abtme_prv_wr').privacy({
				_current: _data.data.current.privacy,
			});
			_row.html(_res);
			//Callable will go here.
			_row.attr('data-edit-field','aboutme');
			_row.removeClass('hidden');
		}
		var buildTemplate = function(){
	    	  //Call template render with time out
	    	  setTimeout(function() { new UIMTemplateutil(_data, updatePrivacyDom).renderExtTemplate(); }, 50);
	    }
		buildTemplate();
		
	};
	
	function buildCancelData($prvElm, $abtMeElm){
		var _data = {};
		_data['data'] = {};
		_data.data['privacy'] = {};
		_data.data.privacy["_id"] = $prvElm.attr('data-old-pr-id');
		_data.data.privacy["_class"] = $prvElm.attr('data-old-pr-class');
		_data.data.privacy["label"] = $prvElm.attr('data-old-pr-label');
		_data.data.privacy["value"] = $prvElm.attr('data-old-pr-value');
		_data.data.privacy["title"] = $prvElm.attr('data-old-pr-title');
		_data.data['aboutme'] = $abtMeElm.text();
		_data["name"] = 'about_me';
		return _data;
	}
	
	function buildSaveData($prvElm, $abtMeElm){
		var _data = {};
		_data['data'] = {};
		_data.data['privacy'] = {};
		_data.data.privacy["_id"] = $prvElm.attr('data-pr-id');
		_data.data.privacy["_class"] = $prvElm.attr('data-pr-class');
		_data.data.privacy["label"] = $prvElm.attr('data-pr-label');
		_data.data.privacy["value"] = $prvElm.attr('data-pr-value');
		_data.data.privacy["title"] = $prvElm.attr('data-pr-title');
		_data.data['aboutme'] = $abtMeElm.val();
		_data["name"] = 'about_me';
		return _data;
	}
	
	function builCurrentData($prvElm, $abtMeElm){
		var _data = {};
		_data['data'] = {};
		_data.data['current'] = {};
		_data.data.current["privacy"] = {};
		_data.data.current.privacy["_id"] = $prvElm.attr('data-pr-id');
		_data.data.current.privacy["_class"] = $prvElm.attr('data-pr-class');
		_data.data.current.privacy["label"] = $prvElm.attr('data-label');
		_data.data.current.privacy["value"] = $prvElm.attr('data-value');
		_data.data.current.privacy["title"] = $prvElm.attr('data-title');
		_data.data.current["aboutme"] = $abtMeElm.text();
		_data["name"] = 'about_me_edit';
		return _data;
		
	}

}(window.jQuery);