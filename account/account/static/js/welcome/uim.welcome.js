var UIM = (function($, WELCOME) {
	var navListItems,
		allWells,
		allNav,
		allNavLink,
		profile_pic_jcrop_api = false,
		lastClick= false,
		clickDelay = 600,
		_inprogress= 'inprogress';
	
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
	}
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
	}
	function applyContactDragable(){
		//On Click of the LI element of contact or event
		$('.contacttokenlist li').on('mousedown mouseup' , function(e){
			if (e.type == "mousedown") {
				lastClick = e.timeStamp; // get mousedown time
		    } else {
		        var diffClick = e.timeStamp - lastClick;
		        if (diffClick < clickDelay) {
		            $(this).toggleClass('uimcontacttodrag');
		        }
		    }
		}).draggable({
		    revertDuration: 10,
		    // grouped items animate separately, so leave this number low
		    containment: '#invitationContacts',
		    start: function(e, ui) {
		        ui.helper.addClass('uimcontacttodrag');
		        
		    },
		    stop: function(e, ui) {
		        // reset group positions
		        $('.uimcontacttodrag').css({
		            top: 0,
		            left: 0
		        });
		    },
		    drag: function(e, ui) {
		        // set selected group position to main dragged object
		        // this works because the position is relative to the starting position
		        $('.uimcontacttodrag').css({
		            top: ui.position.top,
		            left: ui.position.left
		        });
		        
		    }
		}).on({
			mouseenter: function (e) {
				if($(this).parent().attr('id') == 'contact_token_list'){
		        	changeToInviteContact.call();
		        }else{
		        	changeToDontInviteContact.call();
		        }
	          }
		});

		$("#contact_token_list, #invite_token_list").sortable().droppable({
		    drop: function(e, ui) {
		        $('.uimcontacttodrag').appendTo($(this)).add(ui.draggable) // ui.draggable is appended by the script, so add it after
		        	.removeClass('uimcontacttodrag').css({
		        		top: 0,
		        		left: 0
		        	});
		        UIM.addHiddenCLass.apply(this,[$('#uimContactInviteActn')]);
		        if($('#invite_token_list li').length > 0){
		        	UIM.removeHiddenCLass.apply(this,[$('#uimContactInviteActn')]);
            	}
		    }
		});
		//Invite Selected
		$('#invitationContactWrap').on('click', '#inviteSelected', function(e){
			e.preventDefault();
			$('#contact_token_list').find('>li.uimcontacttodrag').appendTo($('#invite_token_list'));
			UIM.removeHiddenCLass.apply(this,[$('#uimContactInviteActn')]);
		});
		//Invite All
		$('#invitationContactWrap').on('click', '#inviteAll', function(e){
			e.preventDefault();
			$('#contact_token_list').find('>li').appendTo($('#invite_token_list'));
			UIM.removeHiddenCLass.apply(this,[$('#uimContactInviteActn')]);
		})
		//UnInvite Selected
		$('#invitationContactWrap').on('click', '#removeinviteSelected', function(e){
			e.preventDefault();
			$('#invite_token_list').find('>li.uimcontacttodrag').appendTo($('#contact_token_list'));
			UIM.addHiddenCLass.apply(this,[$('#uimContactInviteActn')]);
	        if($('#invite_token_list li').length > 0){
	        	UIM.removeHiddenCLass.apply(this,[$('#uimContactInviteActn')]);
        	}
		});
		$('#contact_token_list').uimNavigable();
		changeToInviteContact.call();
	};
	function changeToInviteContact(){
		//make Sure No other has been selected
		$('#invite_token_list').find('>li.uimcontacttodrag').removeClass('uimcontacttodrag');
		UIM.addHiddenCLass.apply(this,[$('.inviteShortAct')]);
		UIM.removeHiddenCLass.apply(this,[$('#inviteSelected'), $('#inviteAll')]);
	};
	function changeToDontInviteContact(){
		//make Sure No other has been selected
		$('#contact_token_list').find('>li.uimcontacttodrag').removeClass('uimcontacttodrag');
		UIM.addHiddenCLass.apply(this,[$('.inviteShortAct')]);
		UIM.removeHiddenCLass.apply(this,[$('#removeinviteSelected')]);
	};
	function handelStepNavigationManualy(_self){
		var $target = $(_self.attr('href')), 
			$item = _self.closest('li');
		if (!$item.hasClass('disabled')) {
			allNav.hide();
			navListItems.closest('li').removeClass('active');
			$item.addClass('active');
			if(_self.attr('data-back-step')){
				$('#backNavigation').show();
			}
			if(_self.attr('data-next-step')){
				$('#forwardNavigation').show();
			}
			if(_self.attr('data-back-step') && !_self.attr('data-next-step')){
				$('#homeNavigation').show();
			}
			allWells.hide();
			$target.show();
		}
	};
	function handelStepNavigationByPager(_self){
		var $item = _self.closest('li');
		if (!$item.hasClass('home')) {
			if($item.hasClass('next')){
				$('ul.setup-panel li.active').next(':not(".disabled")').find('>a').trigger('click');
			}else{
				$('ul.setup-panel li.active').prev(':not(".disabled")').find('>a').trigger('click');
			}
			
		}
	};
	function handelProfileSnapPreview(input){
		if (input.files && input.files[0]) {
			var _load_icon = $('#profilePicPreviewUploadLoader');
			showLoadingIcon.call(this, _load_icon);
			var oFile = input.files[0];
			// check for file size
		    if (oFile.size > 250 * 1024) {
		    	 //TODO : Update the error field
		        $('.error').html('You have selected too big file, please select a one smaller image file').show();
		        return;
		    }
	    	var reader = new FileReader();
	        reader.onload = function (e) {
	        	setTimeout(function(){
	        		$('#actorProfileSnapForm').addClass('unsaved');
	        		if (profile_pic_jcrop_api) {
	        			profile_pic_jcrop_api.destroy();
	        			profile_pic_jcrop_api = null;
	        			console.log('destroying');
	        		}
	        		$('#snapPreviewCenter').removeClass('hidden');
	        		$('#actorSnapRecentUpload').attr('src', e.target.result);
	        		$('#actorSnapRecentUpload').load(function(e){
	        			$(this).Jcrop({
	        				onSelect: new UIMCroputil().showCoords('canvasThumbResult', 'actorSnapRecentUpload', '2d'),
	        				bgFade: true,
	        				bgOpacity: .2,
	        				setSelect: [ 0, 0, 120, 120 ],
	        				aspectRatio: 1
	        			},function(){
	        				profile_pic_jcrop_api = this;
	        			});
	        			stopLoadingIcon.call(this, _load_icon);
	        		});
	        		UIM.removeHiddenCLass.apply(this,[$('#actorProfileSnapSaveAct')])
	        	},0);
	        }
	        reader.readAsDataURL(oFile);
	    }
	};
	function handelProfilePicSave(_self){
		//TODO not yet implemented
		console.log('Give implementation');
	}
	function applyCurrentCityToken(_self){
		_self.uimTokenInput('destroy');
		_self.uimTokenInput(_self.attr('data-uri_loc'), buildLocTokenProperty.call(this,'Current City.'));
	};
	function applyHomeCityToken(_self){
		_self.uimTokenInput('destroy');
		_self.uimTokenInput(_self.attr('data-uri_loc'), buildLocTokenProperty.call(this,'Home Location.'));
	};
	function updateLocationClick(_self){
		//TODO implement this latter
		console.log('implement latter');
	};
	function importContact(_self){
		//TODO save the other forms if unsaved
		if(_self.attr('data-contact') === _self.attr('data-provider')){
			$('#invitationContactWrap').modal('show');
		}else{
			_self.parent().submit();
		}
	}
	WELCOME.addHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(applyHidden);
	};
	WELCOME.removeHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(removeHidden);
	};
	WELCOME.focusWithTimeOut = function(obj){
		setTimeout(function() { obj.focus(); }, 50);
	};
	WELCOME.initWelcomeUserStep = function(){
		var _body = $('body');
		if(_body.attr('data-js_uim_welcome_step') === 'applied'){
			return false;
		}
		setTimeout(function() {
			navListItems = $('ul.setup-panel li a');
			allWells = $('.setup-content').hide();
			allNav = $('.uimStepNav').hide();
			allNavLink = $('.uimStepNav>a');
			navListItems.click(function(e) {
				e.preventDefault();
				handelStepNavigationManualy.call(this, $(this));
			});
			allNavLink.click(function(e){
				e.preventDefault();
				handelStepNavigationByPager.call(this, $(this));
			});
			//On Click Of change Image
			$('#actorProfileSnapForm').on('change', '#prfSnap',function(e){
				e.preventDefault();
				handelProfileSnapPreview(this, this);
			});
			//On Click Of Save Image
			$('#actorProfileSnapForm').on('click', '#actorProfileSnapSaveAct',function(e){
				e.preventDefault();
				handelProfilePicSave.call(this, this)
			});
			
			//Apply Token Input
			setTimeout(function() {
				applyCurrentCityToken.call(this,$('#actorCurrentPlace'));
				applyHomeCityToken.call(this,$('#actorHomeTown'));
			},50);
			//On Click of Save Location
			$('#actorLocForm').on('click', '#actorLocationSaveAct', function(e){
				updateLocationClick.call(this, $(this));
			});
			$('#actorInviteContactStep').on('click', '#importFromGoogle,#importFromYahoo', function(e){
				importContact.call(this,$(this));
			})
			
			//Apply Contact Releated Stuff
			var _contacts = $('#invitationContactWrap');
			if(_contacts.hasClass('hasContact')){
				//Apply Sortable Dragable
				setTimeout(function(){
					applyContactDragable.call();
					_contacts.modal('show');
				});
			}
			//Activate the first active Tab
			$('ul.setup-panel li.active a').trigger('click');

		}, 50);
		_body.attr('data-js_uim_welcome_step', 'applied');
	};
	return WELCOME;
}(jQuery.noConflict(), UIM || {})); 

/* Define dummy gettext if Django's javascrip_catalog is not being used */
if (typeof gettext != 'function') {
    window.gettext = function(text) {
        return text;
    };
}

+function ($) { "use strict";
	UIM.initWelcomeUserStep();
}(window.jQuery);
/*Test*/
var $ = jQuery.noConflict();           
$(document).ready(function() {
//	$('#importFromGoogle').on('click', function(e){
//		$('#invitationContactWrap').modal('show')
//	});
});
