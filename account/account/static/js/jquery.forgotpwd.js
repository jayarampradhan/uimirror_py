/*
 * <p>This is the main function for all the functionality of forgot password 
 * API
 * 
 */
;$.fn.forgotpwd = function(options){
	 "use strict";

	var forgotpwdOpts = $.extend({}, $.fn.forgotpwd.defaults, options);

	// define global vars for the function
	var flags = {
		wrap: "",
		hidden_class: 'hidden',
		elm_to_fade_out: '',
		elm_to_fade_in: '',
		FALSE: false,
		MOUSE: 'mouse',
		TRUE: true,
		err_class: 'form-cn-cl-r',
	};

	// each login will execute this function
	this.each(function(){
		flags.wrap = $(this);
		
	});
	
	//on click I don't know my password	
	flags.wrap.find('#_ui_reset_pwd_frm').on('change',':radio',function(e){
		var $this = $(this);
		var $val = $this.val();
		if(!$val){
			return;
		}
		var $elm_to_show = $('#hideable-box'+$val);
		var $elm_to_hide = $('#hideable-box'+($val==1 ? 2:1));
		UIMIRRORUTILITY.doFadeUpSwap($elm_to_show, $elm_to_hide
				, forgotpwdOpts.dfltFadoutTime, flags.FALSE);
	});
	
	//On click of reset password
	flags.wrap.find('#_ui_reset_pwd_frm').on('click', '#_ui_frgt_pwd_sbmt', function(e){
		e.preventDefault();
		var $this = $(this);
		var $form = $('#_ui_reset_pwd_frm');
		var $radio_elm = $form.find(':radio:checked');
		var $val = $radio_elm.val();
		var $recent_pwd = flags.FALSE;
		var $email_elm = $('#Email'+$val);
		var $errWrap = $('#_ui_reset_faild_msg_wr');
		var $errText = $('#_ui_reset_faild_msg');
		if($val == 2){
			$recent_pwd = $('#recentpassword2');
		}
		
		if(!$email_elm.val() || !UIMIRRORUTILITY.IsEmail($email_elm.val())){
			$errText.text('Enter a Valid Email');
			$errWrap.removeClass( flags.hidden_class );
			$email_elm.addClass( flags.err_class );
			return;
		}
		
		if($recent_pwd && (!$recent_pwd.val() || $recent_pwd.val().length < 4)){
			$errText.text('Enter a Valid most recent password');
			$errWrap.removeClass( flags.hidden_class );
			$recent_pwd.addClass( flags.err_class );
			return;
		}
		$form.submit();
		
	});

};

//define the parameters with the default values of the function
$.fn.forgotpwd.defaults = {
	dfltFadoutTime: 100,
	dfltFadinTime: 100,
};

