+function ($) { "use strict";
	var pMeteroptions = {
        	onKeyUp: function (evt) {
    			$(evt.target).uimpwstrength("outputErrorList");
    		}
		};
	//First Set the focus to the first visible input
	UIM.focusWithTimeOut($('#uimResetForm').find('input[type=password],input[type=text],').filter(':visible:first'));
	//$('#newPassword:password').uimpwstrength(pMeteroptions);
	$('#newPassword:password').focusin(function() {
		var _self = $(this)
		_self.uimpwstrength(pMeteroptions);
		if(_self.hasClass('activated') && _self.val().length > 0){
			_self.uimpwstrength('forceUpdate');
		}else{
			_self.addClass('activated');
		}
	});
	$('#newPassword:password').focusout(function() {
		var _self = $(this);
		_self.uimpwstrength('destroy');
		if(_self.val().length === 0){
			_self.removeClass('activated');
		}
	});
	$('#resendEmailToResetPwdForm').on('click', '#resendMailLink:not(".inprogress")', function(e){
		e.preventDefault();
		UIM.resendTokenMail($(this));
	});
	
	$('#uimResetForm').submit(function(){
	    if(!UIM.validatChangePasswordForm()){
	    	return false;
	    }else{
	    	$('#uimResetActn:submit', this).click(function(e) {
		    	return false;
		    });
	    	return true;
	    }
	});
	
}(window.jQuery);

var UIM = (function(CHANGE_PWD) {
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
	function buildStregthMeterOptions(){
		
	}
	function buildResendMailOptions(){
		var options={},
			_data = {},
			_form = $('#resendEmailToResetPwdForm'),
			_load_ico = $('.sendMailRefresh');
		_data.csrfmiddlewaretoken = _form.find('input[name="csrfmiddlewaretoken"]').val();
		options.url = _form.attr('action')
		options.type = "post";
		options.data = _data;
		options.cache = 'false';
		options.dataType = 'json';
		options.async = 'true';
		options.beforeSend = CHANGE_PWD.removeHiddenCLass.apply(this,[_load_ico]);
		options.loadIcon = _load_ico; 
		return options;
	}
	function stopLoadingIcon(_elm){
		CHANGE_PWD.addHiddenCLass.apply(this,[_elm]);
	}
	function updateResendTokenSuccessResponse(_rs){
		if(_rs.RESCD === '200'){
			$('#uimReSendMailSug').addClass('hasSug').find('span:first').text('We have sent the new token, please check your mail.');
		}else{
			$('#uimReSendMailErr').addClass('hasError').find('span:first').text(_rs.MSG);
		    $('#resendEmailToResetPwdForm').addClass('hidden');
		}
	}
	function updateResendTokenFaildResponse(){
		$('#uimReSendMailErr').addClass('hasError').find('span:first').text('Something Went Wrong we are working on it.');
		$('#resendEmailToResetPwdForm').addClass('hidden');
	}
	function isValidChangePassWordForm(){
		var newPassword = $('#newPassword').removeClass('uimFieldErr'),
			confirmPassword = $('#confirmPassword').removeClass('uimFieldErr'),
			token = $('#token').removeClass('uimFieldErr'),
			_new_pwd_val = newPassword.val(),
			_cnf_pwd_val = confirmPassword.val(),
			_tkn_val = token.val(), 
			msg = '',
			_valid_flag = true;
		if(!_new_pwd_val || !_cnf_pwd_val || !(_new_pwd_val === _cnf_pwd_val)){
			msg = 'Key In the Correct Password and confirm it.<br>';
			newPassword.addClass('uimFieldErr');
			confirmPassword.addClass('uimFieldErr');
			_valid_flag = false;
		}
		if(!_tkn_val){
			var _source = $('#changePwdSource').val();
			if(_source === 'form'){
				msg += 'Key In the Token You Received in your mail box.';
				token.addClass('uimFieldErr');
			}else{
				$('#uimReSendMailErr').addClass('hasError').find('span:first').text('Reqtest Can\'t be processed now, ');
			    $('#resendEmailToResetPwdForm').addClass('hidden');
			}
			_valid_flag = false;
		}
		if(!_valid_flag){
			$('#uimChangePwdErr').html(msg).addClass('hasError')
		}
		return _valid_flag;
	}
	CHANGE_PWD.addHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(applyHidden);
	};
	CHANGE_PWD.removeHiddenCLass = function() {
		var argsArray = Array.prototype.slice.call(arguments);
		argsArray.forEach(removeHidden);
	};
	CHANGE_PWD.focusWithTimeOut = function(obj){
		setTimeout(function() { obj.focus(); }, 50);
	};
	CHANGE_PWD.resendTokenMail = function(_self){
		addClass.call(this, _self, _inprogress)
		var _options = buildResendMailOptions.call();
		var _promise = $.ajax(buildResendMailOptions.call());
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
	CHANGE_PWD.validatChangePasswordForm = function(obj){
		return isValidChangePassWordForm.call();
	};
	return CHANGE_PWD;
}(UIM || {})); 