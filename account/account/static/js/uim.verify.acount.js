var UIM = (function($, VERIFY_ACCOUNT) {
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
	function buildChangeMailOptions(){
		var options={},
			_data = {},
			_form = $('#changeEmailForm');
		_data.csrfmiddlewaretoken = _form.find('input[name="csrfmiddlewaretoken"]').val();
		_data.oldEmail = $('#oldEmail').val();
		_data.newEmail = $('#newEmail').val();
		options.url = _form.attr('action')
		options.type = "post";
		options.data = _data;
		options.cache = 'false';
		options.dataType = 'json';
		options.async = 'true';
		return options;
	}
	function buildResendMailOptions(){
		var options={},
			_data = {},
			_form = $('#resendEmailToVerifyAccountForm'),
			_load_ico = _form.find('.ajxLoad');
		_data.csrfmiddlewaretoken = _form.find('input[name="csrfmiddlewaretoken"]').val();
		options.url = _form.attr('action')
		options.type = "post";
		options.data = _data;
		options.cache = 'false';
		options.dataType = 'json';
		options.async = 'true';
		options.beforeSend = UIM.removeHiddenCLass.apply(this,[_load_ico]);
		options.loadIcon = _load_ico; 
		return options;
	}
	function stopLoadingIcon(_elm){
		UIM.addHiddenCLass.apply(this,[_elm]);
	}
	function showLoadingIcon(_elm){
		UIM.removeHiddenCLass.apply(this,[_elm]);
	}
	function updateResendTokenSuccessResponse(_rs){
		if(_rs.RESCD === '200'){
			$('#uimVerifyCommonSug').addClass('hasSug').html(gettext('We have sent the new token to: <b>')+_rs.EMAIL+gettext('</b>, please check your mail.'));
			UIM.focusWithTimeOut($('#uimVerifyAccountForm').find('input[type=text]').filter(':visible:first'));
		}else{
			$('#uimVerifyCommonErr').addClass('hasError').text(_rs.MSG);
		}
		if(_rs.RESCD !== '200' || _rs.RESCD !== '500'){
			$('#resendEmailToVerifyAccountForm').addClass('hidden');
		}
	}
	function updateResendTokenFaildResponse(){
		$('#uimVerifyCommonErr').addClass('hasError').text(gettext('Something Went Wrong we are working on it. Try Again after sometime.'));
	}
	function updateChangeEmailSuccessResponse(_rs){
		if(_rs.RESCD === '200'){
			$('#uimVerifyCommonSug').addClass('hasSug').html(gettext('We have Changed Your Email to <b>')+_rs.EMAIL+gettext('</b>, Check your Mail for the instruction(s).'));
			UIM.focusWithTimeOut($('#uimVerifyAccountForm').find('input[type=text]').filter(':visible:first'));
		}else{
			$('#uimVerifyCommonErr').addClass('hasError').text(_rs.MSG);
		}
		if(_rs.RESCD !== '500' && _rs.RESCD === '200'){
			$('#changeEmailWrap').addClass('hidden');
			$('#changeEmailLink').removeClass(_inprogress);
		}
	}
	function updateChangeEmailFaildResponse(){
		$('#uimVerifyCommonErr').addClass('hasError').text(gettext('Something Went Wrong we are working on it. Try Again after sometime.'));
	}
	function isValidChangeEmailForm(){
		var newEmail = $('#newEmail').removeClass('uimFieldErr'),
			email = $('#oldEmail').val(),
			_new_ema_val = newEmail.val(),
			msg = '',
			_valid_flag = true;
		if(!_new_ema_val){
			msg = gettext('Key In the Email You want to update.<br>');
			newEmail.addClass('uimFieldErr');
			_valid_flag = false;
		}else if(_new_ema_val === email){
			msg = gettext('This was your old Email, for update you need to key in new valid one.<br>');
			newEmail.addClass('uimFieldErr');
			_valid_flag = false;
		}
		if(!_valid_flag){
			$('#uimVerifyCommonErr').html(msg).addClass('hasError')
		}
		return _valid_flag;
	}
	function isValidVerifyForm(){
		var token = $('#token').removeClass('uimFieldErr'),
			token_val = token.val(),
			msg = '',
			_valid_flag = true;
		if(!token_val){
			msg = gettext('Key In Token You got in your Mail Box.<br>');
			token.addClass('uimFieldErr');
			_valid_flag = false;
		}
		if(!_valid_flag){
			$('#uimVerifyAccountErr').html(msg).addClass('hasError')
		}
		return _valid_flag;
	}
	function resetChangeEmailButton(_self){
		_self.html('Update');
	}
	VERIFY_ACCOUNT.addHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(applyHidden);
	};
	VERIFY_ACCOUNT.removeHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(removeHidden);
	};
	VERIFY_ACCOUNT.focusWithTimeOut = function(obj){
		setTimeout(function() { obj.focus(); }, 50);
	};
	VERIFY_ACCOUNT.resendTokenMail = function(_self){
		addClass.call(this, _self, _inprogress)
		var _options = buildResendMailOptions.call();
		var _promise = $.ajax(_options);
		_promise.done(function(rs){
			stopLoadingIcon.call(this, _options.loadIcon);
			removeClass.call(this, _self, _inprogress);
			updateResendTokenSuccessResponse.call(this, rs);
		});
		_promise.fail(function(rs){
			stopLoadingIcon.call(this, _options.loadIcon);
			removeClass.call(this, _self, _inprogress);
			updateResendTokenFaildResponse.call(this, rs);
		});
	};
	VERIFY_ACCOUNT.handelChangeEmailLink = function(_self){
		addClass.call(this, _self, _inprogress);
		var _load_ico = _self.next('i');
		showLoadingIcon.call(this,_load_ico);
		UIM.removeHiddenCLass.apply(this,[$('#changeEmailWrap')]);
		stopLoadingIcon.call(this,_load_ico);
		UIM.focusWithTimeOut($('#changeEmailForm').find('input[type=email]').filter(':visible:first'));
	}
	VERIFY_ACCOUNT.changeEmail = function(_self){
		addClass.call(this, _self, _inprogress);
		_self.html('<i class="ajxLoad verifyRefresh"></i> '+gettext('Updating'));
		if(isValidChangeEmailForm.call()){
			var _options = buildChangeMailOptions.call();
			var _promise = $.ajax(_options);
			_promise.done(function(rs){
				resetChangeEmailButton.call(this, _self);
				removeClass.call(this, _self, _inprogress);
				updateChangeEmailSuccessResponse.call(this, rs);
			});
			_promise.fail(function(rs){
				resetChangeEmailButton.call(this, _self);
				removeClass.call(this, _self, _inprogress);
				updateChangeEmailFaildResponse.call(this, rs);
			});
		}else{
			_self.html(gettext('Update'));
		}
	};
	VERIFY_ACCOUNT.verifyAccount = function(_self){
		addClass.call(this, _self, _inprogress);
		if(isValidVerifyForm.call()){
			$('#uimVerifyAccountForm').submit();
		}else{
			removeClass.call(this, _self, _inprogress);
		}
	};
	VERIFY_ACCOUNT.initVerifyAccount = function(){
		var _body = $('body');
		if(_body.attr('data-js_uim_verify_acc') === 'applied'){
			console.log('Already Applied');
			return false;
		}
		setTimeout(function() { 
			UIM.focusWithTimeOut($('#uimVerifyAccountForm').find('input[type=text]').filter(':visible:first'));
			$('#resendEmailToVerifyAccountForm').on('click', '#resendMailLink:not(".inprogress")', function(e){
				e.preventDefault();
				UIM.resendTokenMail($(this));
			});
			
			$('#changeEmailForm').on('click', '#changeEmailLink:not(".inprogress")', function(e){
				e.preventDefault();
				UIM.handelChangeEmailLink($(this));
			});
			$('#changeEmailForm').on('click dblclick', '#uimAccountChangeEmailAct:not(".inprogress")', function(e){
				e.preventDefault();
				UIM.changeEmail($(this));
			});
			$('#uimVerifyAccountForm').on('click dblclick', '#uimAccountVerifyActn:not(".inprogress")', function(e){
				e.preventDefault();
				UIM.verifyAccount($(this));
			});
			$('#verifyContainer').on('click dblclick', '.inprogress', function(e){
				e.preventDefault();
				UIM.focusWithTimeOut($('#verifyContainer').find('input[type=text],input[type=email]').filter(':visible:first'));
			})

		}, 50);
		_body.attr('data-js_uim_verify_acc', 'applied');
	};
	
	return VERIFY_ACCOUNT;
}(jQuery.noConflict(), UIM || {})); 

/* Define dummy gettext if Django's javascrip_catalog is not being used */
if (typeof gettext != 'function') {
    window.gettext = function(text) {
        return text;
    };
}

+function ($) { "use strict";
	UIM.initVerifyAccount();
}(window.jQuery);