var UIM = (function($, LOGIN) {
	function applyHidden(_elm) {
		_elm.addClass('hidden');
	}
	function removeHidden(_elm) {
		_elm.removeClass('hidden');
	}
	function updateLoginErrMsg(msg){
		$('#uimLgnErr').txt(msg).addClass('hasError');
	}
	function updateForgotPwdErrMsg(msg){
		$('#uimForgotPwdErr').txt(msg).addClass('hasError');
	}
	function isValidateLoginForm(){
		var _uid_elm = $('#user_id').removeClass('uimFieldErr'),
			_pwd_elm = $('#password').removeClass('uimFieldErr'),
			_valid_flag = true,
			_uid = _uid_elm.val(),
			_pwd = _pwd_elm.val();
		if(!_uid && !_pwd){
			_valid_flag = false;
			updateLoginErrMsg(gettext('Key In User Id And Password.'));
			_uid_elm.addClass('uimFieldErr');
			_pwd_elm.addClass('uimFieldErr');
		}else if(!_pwd){
			_valid_flag = false;
			updateLoginErrMsg(gettext('Key In Password.'));
			_pwd_elm.addClass('uimFieldErr');
		}else if(!_uid){
			_valid_flag = false;
			updateLoginErrMsg(gettext('Key In User Id.'));
			_uid_elm.addClass('uimFieldErr');
		}
		return _valid_flag;
	}
	function isValidForgotPassWordForm(){
		var _option_val = $('input[name=preoption]:checked', '#uimForgotPasswordForm').val(),
			_valid_flag = true;
		if(_option_val === '1'){
			var _uimEmail_elm = $('#uimSignedUpEmail').removeClass('uimFieldErr');
			if(!_uimEmail_elm.val()){
				_valid_flag = false;
				updateForgotPwdErrMsg(gettext('Key In User Id And Password.'));
				_uimEmail_elm.addClass('uimFieldErr');
			}
		}else if(_option_val === '2'){
			var _uimEmail_elm = $('#uimEmail').removeClass('uimFieldErr'),
				_uimrRecent_pwd_elm = $('#uimRecentPwd').removeClass('uimFieldErr'),
				_uimrAlternative_em_elm = $('#uimResetEmailAccessTo').removeClass('uimFieldErr'),
				_uimEmail_val = _uimEmail_elm.val(),
				_uimrRecent_pwd_val = _uimrRecent_pwd_elm.val(),
				_uimrAlternative_em_val = _uimrAlternative_em_elm.val(),
				_valid_flag = true;
				
			if(!_uimEmail_val && !_uimrRecent_pwd_val && !_uimrAlternative_em_val){
				updateForgotPwdErrMsg(gettext('Key In All the fields.'));
				_uimEmail_elm.addClass('uimFieldErr');
				_uimrRecent_pwd_elm.addClass('uimFieldErr');
				_uimrAlternative_em_elm.addClass('uimFieldErr');
				_valid_flag = false;
			}else if(!_uimEmail_val && !_uimrRecent_pwd_val){
				updateForgotPwdErrMsg(gettext('Key In Registered Email and Recent Password.'));
				_uimEmail_elm.addClass('uimFieldErr');
				_uimrRecent_pwd_elm.addClass('uimFieldErr');
				_valid_flag = false;
			}else if(!_uimrRecent_pwd_val && !_uimrAlternative_em_val){
				updateForgotPwdErrMsg(gettext('Key In Recent Password and Alternative Email Id.'));
				_uimrRecent_pwd_elm.addClass('uimFieldErr');
				_uimrAlternative_em_elm.addClass('uimFieldErr');
				_valid_flag = false;
			}else if(!_uimEmail_val && !_uimrAlternative_em_val){
				updateForgotPwdErrMsg(gettext('Key In Regsitered Email and Alternative Email Id.'));
				_uimEmail_elm.addClass('uimFieldErr');
				_uimrAlternative_em_elm.addClass('uimFieldErr');
				_valid_flag = false;
			}else if(!_uimEmail_val){
				updateForgotPwdErrMsg(gettext('Key In Registered Email.'));
				_uimEmail_elm.addClass('uimFieldErr');
				_valid_flag = false;
			}else if(!_uimrRecent_pwd_val){
				updateForgotPwdErrMsg(gettext('Key In Most Recent Password.'));
				_uimrRecent_pwd_elm.addClass('uimFieldErr');
				_valid_flag = false;
			}else if(!_uimrAlternative_em_val){
				updateForgotPwdErrMsg(gettext('Key In Alternative Email Id.'));
				_uimrAlternative_em_elm.addClass('uimFieldErr');
				_valid_flag = false;
			}
		}
		return _valid_flag;
	}
	LOGIN.addHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(applyHidden);
	};
	LOGIN.removeHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(removeHidden);
	};
	LOGIN.focusWithTimeOut = function(obj){
		setTimeout(function() { obj.focus(); }, 50);
	};
	LOGIN.validateLoginForm = function(){
		return isValidateLoginForm.call();
	};
	LOGIN.validateForgotPasswordForm = function(){
		return isValidForgotPassWordForm.call();
	};
	LOGIN.initLogin = function(){
		var _body = $('body');
		if(_body.attr('data-js_uim_login') === 'applied'){
			console.log('Already Applied');
			return false;
		}
		setTimeout(function() { 
			$('.forgot-pass').on('click', function(e) {
				  e.preventDefault();
				  UIM.removeHiddenCLass.apply(this,[$('#fade'), $('#popup')]);
				  UIM.focusWithTimeOut($('.pass-reset').find('input[type=email],input[type=password]').filter(':visible:first'));
			});

			$('#popup_close').on('click', function(e){
				  e.preventDefault();
				  UIM.addHiddenCLass.apply(this,[$('#fade'), $('#popup')]);
				  UIM.focusWithTimeOut($('#user_id'));
			})

			$('.pass-reset').on('change',':radio',function(e){
					var $this = $(this);
					var $val = $this.val();
					if(!$val){
						return;
					}
					var $elm_to_show = $('#hideable-box'+$val);
					var $elm_to_hide = $('#hideable-box'+($val==='1' ? '2':'1'));
					$elm_to_hide.fadeOut("slow", function() {
						UIM.removeHiddenCLass.apply(this,[$elm_to_show]);
						$elm_to_show.fadeIn('slow',function(){
							UIM.focusWithTimeOut($elm_to_show.find(':input').filter(':visible:first'));
						});
					 });
				});

			$('#uimLoginForm').submit(function(e){
				    if(!UIM.validateLoginForm()){
				    	return false;
				    }else{
				    	$('#uimLgnActn:submit', this).click(function() {
					        return false;
					    });
				    	return true;
				    }
				});
			$('#uimForgotPasswordForm').submit(function(){
				  if(!UIM.validateForgotPasswordForm()){
					  return false;
				  }else{
					  $('#uimForgotPwdReqAction:submit', this).click(function() {
						  return false;
					  });
					  return true;
				  }
				});
		}, 50);
		_body.attr('data-js_uim_login', 'applied');
	};
	return LOGIN;
}(jQuery.noConflict(), UIM || {})); 

/* Define dummy gettext if Django's javascrip_catalog is not being used */
if (typeof gettext != 'function') {
    window.gettext = function(text) {
        return text;
    };
}

+function ($) { "use strict";
	UIM.initLogin();
}(window.jQuery);