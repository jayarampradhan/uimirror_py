var UIM = (function($, REGISTER) {
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
	function buildDefaultTitleTipProp(_self){
		var _prop = {},
			_content_obj = {},
			_hide_obj = {},
			_position_obj = {},
			_pos_adjust_obj = {};
		_content_obj.text = _self.attr('title') || _self.attr('data-title')|| _self.attr('data-tip');
		_pos_adjust_obj.mouse = false;
		_position_obj.my = 'bottom right';
		_position_obj.at = 'bottom right';
		_position_obj.target = 'mouse';
		_position_obj.adjust = _pos_adjust_obj;
		_hide_obj.fixed = false;
		_hide_obj.delay = 300;
		_hide_obj.leave = true;
		_prop.content = _content_obj;
		_prop.hide = _hide_obj;
		_prop.position = _position_obj;
		return _prop;
	}
	function buildBirthDayTipProperty(){
		var _prop = {},
			_content_obj = {},
			_hide_obj = {},
			_position_obj = {},
			_pos_adjust_obj = {},
			_style_obj = {};
		_content_obj.text = $('#_whybd_hlp').html() || '';
		_pos_adjust_obj.mouse = false;
		_position_obj.target = 'mouse';
		_position_obj.adjust = _pos_adjust_obj;
		_hide_obj.fixed = true;
		_hide_obj.delay = 300;
		_hide_obj.leave = false;
		_style_obj.classes = '_uim_context_boot _ui_context_shadow';
		
		_prop.id = 'bd_hlp_tip';
		_prop.content = _content_obj;
		_prop.hide = _hide_obj;
		_prop.position = _position_obj;
		_prop.style = _style_obj;
		return _prop; 
	}
	function inactieveLink(_elm){
		_elm.on('click',function(e){
			   e.preventDefault();
		 }).removeAttr('href');
		 return _elm;
	}
	function isValidRegisterForm(){
		var fName = $('#fname').removeClass('uimFieldErr'),
			lName = $('#lname').removeClass('uimFieldErr'),
			email = $('#email').removeClass('uimFieldErr'),
			password = $('#password').removeClass('uimFieldErr'),
			confirmPassword = $('#confirmPassword').removeClass('uimFieldErr'),
			birth_date = $('#birth_date').removeClass('uimFieldErr'),
			birth_month = $('#birth_month').removeClass('uimFieldErr'),
			birth_year = $('#birth_year').removeClass('uimFieldErr'),
			_date = birth_date.val(),
			_month = birth_month.val(),
			_year = birth_year.val(),
			DIGIT_REGX = '/^\d+$/',
			msg = '',
			_valid_flag = true;
		if(!fName.val()){
			msg += gettext('Key In your Name<br>');
			fName.addClass('uimFieldErr');
			lName.addClass('uimFieldErr');
			_valid_flag = false;
		}else if(!email.val()){
			msg += gettext('Key In your Email ID<br>');
			email.addClass('uimFieldErr');
			_valid_flag = false;
		}else if(!password.val() || !(password.val() === confirmPassword.val())){
			msg += gettext('Key In your Desired Password<br>');
			password.addClass('uimFieldErr');
			confirmPassword.addClass('uimFieldErr');
			_valid_flag = false;
		}else if(!DIGIT_REGX.test(_date) || !DIGIT_REGX.test(_month) || !DIGIT_REGX.test(_year)){
			msg += gettext('Key In your Birth Date<br>');
			birth_date.addClass('uimFieldErr');
			birth_month.addClass('uimFieldErr');
			birth_year.addClass('uimFieldErr');
			_valid_flag = false;
		}
		console.log(_valid_flag);
		if(!_valid_flag){
			console.log('coming',msg);
			$('#uimRegInfoErrWrap').addClass('hasErrorOrSug').find('#uimRegisterErr').html(msg).addClass('hasError')
		}
		return _valid_flag;
	}
	REGISTER.addHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(applyHidden);
	};
	REGISTER.removeHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(removeHidden);
	};
	REGISTER.focusWithTimeOut = function(obj){
		setTimeout(function() { obj.focus(); }, 50);
	};
	REGISTER.applyWhyBirthDayTip = function(_self){
		if(_self.exists()){
			_self.uimtip(buildBirthDayTipProperty.call())
		}
		return inactieveLink.call(this, _self);
	};
	REGISTER.applyDefaultTip = function(){
		setTimeout(function() {
				$('.uimTip').each(function(_ind, _elm){
				var $_elm = $(_elm);
				$_elm.uimtip(buildDefaultTitleTipProp.call(this, $_elm));
			});
		}, 50);
	};
	REGISTER.hideWhyBirthDayTip = function(targetElement, e){
		e.preventDefault();
		var element ='#uitip-'+ targetElement;
		$(element).uimtip("api").hide();
	};
	REGISTER.openGenderSelect = function(_self, e){
		e.preventDefault();
		var element ='#uitip-'+ targetElement;
		$(element).uimtip("api").hide();
	};
	REGISTER.validateRegisterForm = function(){
		return isValidRegisterForm.call();
	};
	REGISTER.initRegister = function(){
		var _body = $('body');
		if(_body.attr('data-js_uim_register') === 'applied'){
			console.log('Already Applied');
			return false;
		}
		setTimeout(function() { 
			UIM.focusWithTimeOut($('#uimRegisterForm').find('input[type=text],input[type=email],input[type=password]').filter(':visible:first'));
			UIM.applyWhyBirthDayTip($('#uimWhyBdTip'));
			var pMeteroptions = {
				onKeyUp: function (evt) {
					$(evt.target).uimpwstrength("outputErrorList");
				}
			};
			$('#password:password').focusin(function() {
				var _self = $(this)
				_self.uimpwstrength(pMeteroptions);
				if(_self.hasClass('activated') && _self.val().length > 0){
					_self.uimpwstrength('forceUpdate');
				}else{
					_self.addClass('activated');
				}
			});
			$('#password:password').focusout(function() {
				var _self = $(this);
				_self.uimpwstrength('destroy');
				if(_self.val().length === 0){
					_self.removeClass('activated');
				}
			});

			$('#uimRegisterForm').submit(function(){
				  if(!UIM.validateRegisterForm()){
					  return false;
				  }else{
					  $('#uimRegisterActn:submit', this).click(function() {
						  return false;
					  });
					  return true;
				  }
			});
			$('#timeZone').val(jstz.determine().name());
			UIM.applyDefaultTip();
		}, 50);
		_body.attr('data-js_uim_register', 'applied');
	};
	return REGISTER;
}(jQuery.noConflict(), UIM || {})); 

/* Define dummy gettext if Django's javascrip_catalog is not being used */
if (typeof gettext != 'function') {
    window.gettext = function(text) {
        return text;
    };
}

+function ($) { "use strict";
	UIM.initRegister();
}(window.jQuery);

$.fn.exists = function () {
    return this.length !== 0;
}