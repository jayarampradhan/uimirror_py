/*
 * <p>This is the main function for all the functionality of First Time register steps 
 * API
 * 
 */
;$.fn.welcome_fst_time = function(options){
	 "use strict";

	var welcome_fst_timeOpts = $.extend({}, $.fn.welcome_fst_time.defaults, options);

	// define global vars for the function
	var flags = {
		wrap: "",
		hidden_class: 'hidden',
		FALSE: false,
		MOUSE: 'mouse',
		TRUE: true,
		err_class: 'form-cn-cl-r',
		HASH:'#',
		ID: 'id',
		EMPTY: '',
		DATA_FROM_REF:'data-from-ref',
		DATA_FROM_NEXT_REF:'data-from-next-ref',
		DATA_TAB_REF:'data-tab-ref',
		DATA_TAB_NEXT_REF:'data-tab-next-ref',
		DATA_FROM_PRV_REF:'data-from-prv-ref',
		DATA_TAB_PRV_REF:'data-tab-prv-ref',
		PROGTRCKR_ONGOING:'progtrckr-ongoing',
		PROGTRCKR_COMPLETE:'progtrckr-done',
		PROGTRCKR_TODO:'progtrckr-todo',
		PROGTRCKR_SKIP:'progtrckr-skip',
		CHECKED:'checked',
		INVALID_CLASS: 'invalid',
		lastClick: false,
		
	};

	// each First Profile Complete will execute this
	this.each(function(){
		flags.wrap = $(this);
		
		//Find Location inputs and apply the token input plugin to them
		var $placesElm = $('#_ui_places_1_cur');
		if($placesElm){
			
			UIMIRRORUTILITY.apply_current_city_token(buildChooseCityProperty($placesElm), $placesElm);
		}
		var $curCityelm = flags.wrap.find('#_ui_places_1_org');
		if($curCityelm){
			UIMIRRORUTILITY.apply_current_city_token(buildChooseCityProperty($curCityelm), $curCityelm);
		}
		UIMIRRORUTILITY.applyTip('.uimtpd');
	});
	
	function buildChooseCityProperty($elm){
		//TODO Fix This Property for more rfeine way
		var property = {
				propertyToSearch: "location",
				resultsFormatter: function(item){ return "<li>" + "<div style='display: inline-block; padding-left: 10px;'><div class='location'>" + item.location  + "</div></div></li>" },
				tokenFormatter: function(item) { return "<li><p>" + item.location + "</p></li>" },
				theme: "facebook",
				allowFreeTagging:false,
				tokenLimit:1,
				placeholder:$elm.attr("placeholder"),
				hintText: 'Type Locality city state...'
		}
		return property;
	}
	
	//On-click of Skip. move to next Step
	$('#comnon-actions').on('click', '#_ui_stp_skp', function(e){
		e.preventDefault();
		var $this = $(this);
		UIMIRRORUTILITY.hideToolTip($this);
		var $back = $('#_ui_stp_back');
		var $form_elm_to_hide = $this.attr(flags.DATA_FROM_REF);
		var $form_elm_to_shw = $this.attr(flags.DATA_FROM_NEXT_REF);
		var $tab_elm_to_skp = $this.attr(flags.DATA_TAB_REF);
		var $tab_elm_to_shw = $this.attr(flags.DATA_TAB_NEXT_REF);
		
		//TODO check if next Value is empty then do a form submit for next page
		if(!$form_elm_to_shw || $form_elm_to_shw.length == 0){
			console.log('DO a form submit');
			return;
		}
		
		//Set Back Attributes
		$back.attr(flags.DATA_FROM_REF, $form_elm_to_shw);
		$back.attr(flags.DATA_FROM_PRV_REF, $form_elm_to_hide);
		$back.attr(flags.DATA_TAB_REF, $tab_elm_to_shw);
		$back.attr(flags.DATA_TAB_PRV_REF, $tab_elm_to_skp);
		
		//Swap ID
		$this.attr(flags.DATA_FROM_REF, $form_elm_to_shw);
		$this.attr(flags.DATA_TAB_REF, $tab_elm_to_shw);
		
		//Make Them proper selector
		$tab_elm_to_skp = $(flags.HASH+$tab_elm_to_skp);
		$tab_elm_to_shw = $(flags.HASH+$tab_elm_to_shw);
		$form_elm_to_hide = $(flags.HASH+$form_elm_to_hide);
		$form_elm_to_shw = $(flags.HASH+$form_elm_to_shw);
		var next_id = determine_next_form_tab_id($form_elm_to_shw, $tab_elm_to_shw);
		if(next_id){
			$this.attr(flags.DATA_FROM_NEXT_REF, next_id.nextformid);
			$this.attr(flags.DATA_TAB_NEXT_REF, next_id.nexttabid);
		}else{
			$this.attr(flags.DATA_FROM_NEXT_REF, flags.EMPTY);
			$this.attr(flags.DATA_TAB_NEXT_REF, flags.EMPTY);
		}
		//Set Next set Attributes
		//mark progress bar and Form hide and show
		$back.removeClass(flags.hidden_class);
		$form_elm_to_hide.addClass(flags.hidden_class);
		
		var tab_classes = $tab_elm_to_skp.attr("class");
		var tab_class_list = tab_classes.split(/\s+/);
		var tab_to_shw_classes = $tab_elm_to_shw.attr("class");
		var tab_to_shw_class_list = tab_to_shw_classes.split(/\s+/);
		if(-1 == $.inArray(flags.PROGTRCKR_COMPLETE, tab_to_shw_class_list)){
			$tab_elm_to_skp.removeClass(flags.PROGTRCKR_ONGOING);
			$tab_elm_to_skp.addClass(flags.PROGTRCKR_SKIP);
		}
		
		if(-1 == $.inArray(flags.PROGTRCKR_COMPLETE, tab_to_shw_class_list)){
			$tab_elm_to_shw.removeClass(flags.PROGTRCKR_TODO);
			$tab_elm_to_shw.addClass(flags.PROGTRCKR_ONGOING);
		}
		
		$form_elm_to_shw.removeClass(flags.hidden_class);
		
	});
	//This will help to choose next form for skip navigation
	function determine_next_form_tab_id($currform, $currtab){
		var $nextform = $currform.next();
		var $nexttab = $currtab.next();
		var $nextformid = $nextform.attr(flags.ID);
		if($nextformid){
			if($nextform.hasClass( flags.INVALID_CLASS )){
				determine_next_form_tab_id($nextform, $nexttab);
			}else{
				var form_id = {
						nextformid:$nextformid,
						nexttabid:$nexttab.attr(flags.ID),
				}
				return form_id 
			}
		}else{
			return;
		}
	}
	//On-Click of Going back
	$('#comnon-actions').on('click', '#_ui_stp_back', function(e){
		e.preventDefault();
		var $this = $(this);
		UIMIRRORUTILITY.hideToolTip($this);
		var $skip = $('#_ui_stp_skp');
		var $form_elm_to_hide = $this.attr(flags.DATA_FROM_REF);
		var $form_elm_to_shw = $this.attr(flags.DATA_FROM_PRV_REF);
		var $tab_elm_to_hide = $this.attr(flags.DATA_TAB_REF);
		var $tab_elm_to_shw = $this.attr(flags.DATA_TAB_PRV_REF);
		//Set Back Attributes
		$skip.attr(flags.DATA_FROM_REF, $form_elm_to_shw);
		$skip.attr(flags.DATA_FROM_NEXT_REF, $form_elm_to_hide);
		$skip.attr(flags.DATA_TAB_REF, $tab_elm_to_shw);
		$skip.attr(flags.DATA_TAB_NEXT_REF, $tab_elm_to_hide);
		
		//Swap ID
		$this.attr(flags.DATA_FROM_REF, $form_elm_to_shw);
		$this.attr(flags.DATA_TAB_REF, $tab_elm_to_shw);
		
		//Make Them proper selector
		$tab_elm_to_hide = $(flags.HASH+$tab_elm_to_hide);
		$tab_elm_to_shw = $(flags.HASH+$tab_elm_to_shw);
		$form_elm_to_hide = $(flags.HASH+$form_elm_to_hide);
		$form_elm_to_shw = $(flags.HASH+$form_elm_to_shw);
		var $formprevid =  determine_prev_form_tab_id($form_elm_to_shw, $tab_elm_to_shw);
		if($formprevid){
			$this.attr(flags.DATA_FROM_PRV_REF, $formprevid.prevformid);
			$this.attr(flags.DATA_TAB_PRV_REF, $formprevid.prevtabid);
		}else{
			$this.addClass(flags.hidden_class);
			$this.attr(flags.DATA_FROM_PRV_REF, flags.EMPTY);
			$this.attr(flags.DATA_TAB_PRV_REF, flags.EMPTY);
		}
		//Set Next set Attributes
		//mark progress bar and Form hide and show
		$form_elm_to_hide.addClass(flags.hidden_class);
		
		var tab_classes = $tab_elm_to_hide.attr("class");
		var tab_class_list = tab_classes.split(/\s+/);
		var tab_to_shw_classes = $tab_elm_to_shw.attr("class");
		var tab_to_shw_class_list = tab_to_shw_classes.split(/\s+/);
		
		if(-1 == $.inArray(flags.PROGTRCKR_COMPLETE, tab_class_list)){
			$tab_elm_to_hide.removeClass(flags.PROGTRCKR_ONGOING);
			$tab_elm_to_hide.removeClass(flags.PROGTRCKR_TODO);
			$tab_elm_to_hide.addClass(flags.PROGTRCKR_SKIP);
		}
		
		if(-1 == $.inArray(flags.PROGTRCKR_COMPLETE, tab_to_shw_class_list)){
			$tab_elm_to_shw.removeClass(flags.PROGTRCKR_TODO);
			$tab_elm_to_shw.removeClass(flags.PROGTRCKR_SKIP);
			$tab_elm_to_shw.addClass(flags.PROGTRCKR_ONGOING);
		}
		
		$form_elm_to_shw.removeClass(flags.hidden_class);
	});
	
	//This will help to choose prev form for back navigation
	function determine_prev_form_tab_id($currform, $currtab){
		var $prevform = $currform.prev();
		var $prevtab = $currtab.prev();
		var $prevformid = $prevform.attr(flags.ID);
		if($prevformid){
			if($prevform.hasClass( flags.INVALID_CLASS )){
				determine_prev_form_tab_id($prevform, $prevtab);
			}else{
				var form_id = {
						prevformid:$prevformid,
						prevtabid:$prevtab.attr(flags.ID),
				}
				return form_id; 
			}
		}else{
			return;
		}
	}
	
	//On click of contact import check boxes
	$('#_step_complete_card').on('change', '._ui_cntct_chc', function(e){
		var $this = $(this);
		var $par_elm = $(flags.HASH+$this.attr('data-form-ref'));
		var $span = $('.prvbdwrap');
		var $chk_box = $('._ui_cntct_chc');
		$span.addClass(flags.hidden_class);
		$chk_box.prop(flags.CHECKED, false);
		$this.prop(flags.CHECKED, true);
		$par_elm.find('.prvbdwrap').removeClass(flags.hidden_class);
		
	});
	
	//ON click of Close/ hide button from pop up
	$('#popup').on('click', '#popup_close', function(e){
		var parelm = $('#popup');
		var fade = $('#fade');
		var popupcontent = $('#popupmaincontent');
		parelm.hide();
		fade.hide();
		popupcontent.remove();
		
	});
	
	//Onclick of invite/Ignore
    $('#popupmaincontent').on('click', '#_contact_ex_ac' , function(e){
    	var $this = $(this);
    	var _ref = $this.attr('data-ref');
    	if(_ref == 'lft'){
    		$('#contact_token_list').find('.active').appendTo($('#invite_token_list'));
    		$('#_ui_send_invitation').removeClass(flags.hidden_class);
    		changeToIgnoreContact();
    	}else{
    		$('#invite_token_list').find('.active').appendTo($('#contact_token_list'));
    		if($('#invite_token_list li').length == 0){
    			$('#_ui_send_invitation').addClass(flags.hidden_class);
    		}
    		changeToInviteContact();
    	}
		
	});
    
    //Onclick of inviteAll/ Ignore All
    $('#popupmaincontent').on('click', '#_contact_ex_ac_all' , function(e){
    	var $this = $(this);
    	var _ref = $this.attr('data-ref');
    	if(_ref == 'lft'){
    		$('#contact_token_list').find('li').appendTo($('#invite_token_list'));
    		$('#_ui_send_invitation').removeClass(flags.hidden_class);
    		changeToIgnoreContact();
    	}else{
    		$('#invite_token_list').find('li').appendTo($('#contact_token_list'));
    		$('#_ui_send_invitation').addClass(flags.hidden_class);
    		changeToInviteContact();
    	}
	});
	
	//On Click of the LI element of contact or event
	$('.contacttokenlist li').on('mousedown mouseup' , function(e){
		
		var clickDelay = 600;
		
		if (e.type == "mousedown") {
			flags.lastClick = e.timeStamp; // get mousedown time
        } else {
            var diffClick = e.timeStamp - flags.lastClick;
            if (diffClick < clickDelay) {
                // add selected class to group draggable objects
                $(this).toggleClass('active');
                //console.log(e.shiftKey);
            }
            
            if($(this).parent().attr('id') == 'contact_token_list'){
            	changeToInviteContact();
            	
            }else{
            	changeToIgnoreContact();
            }
            
        }
	}).draggable({
        revertDuration: 10,
        // grouped items animate separately, so leave this number low
        containment: '#popupmaincontent',
        start: function(e, ui) {
            ui.helper.addClass('active');
            $("#contacttowrapper").css({
                overflow: 'visible',
            });
            $("#contactfromwrapper").css({
                overflow: 'visible',
            });
            
        },
        stop: function(e, ui) {
            // reset group positions
            $('.active').css({
                top: 0,
                left: 0
            });
            $("#contacttowrapper").removeAttr("style");
            $("#contactfromwrapper").removeAttr("style");
        },
        drag: function(e, ui) {
            // set selected group position to main dragged object
            // this works because the position is relative to the starting position
            $('.active').css({
                top: ui.position.top,
                left: ui.position.left
            });
            
        }
    });
	
    $("#contact_token_list, #invite_token_list").sortable().droppable({
        drop: function(e, ui) {
            $('.active').appendTo($(this)).add(ui.draggable) // ui.draggable is appended by the script, so add it after
            .removeClass('active').css({
                top: 0,
                left: 0
            });
            if($(this).attr('id') == 'invite_token_list'){
            	$('#_ui_send_invitation').removeClass(flags.hidden_class);
            	changeToIgnoreContact();
            }else{
            	if($('#invite_token_list li').length == 0){
            		$('#_ui_send_invitation').addClass(flags.hidden_class);
            	}
            	changeToInviteContact();
            }
        }
    });
    
    function changeToInviteContact(){
    	$('#_contact_ex_ac')
			.text('Invite >')
			.attr('data-ref', 'lft');
    	$('#_contact_ex_ac_all')
			.text('Invite All >')
			.attr('data-ref', 'lft');
    }
    
    function changeToIgnoreContact(){
    	$('#_contact_ex_ac')
			.text('< Ignore')
			.attr('data-ref', 'right');
    	$('#_contact_ex_ac_all')
			.text('< Ignore All')
			.attr('data-ref', 'right');
    }
    
    //Ajax Call Helper for showing loading
	function showLoading(formData, jqForm, options) {
		var $elm_to_show = $('#_ui_img_load_wt'),
			_pop_up = $('#popup').html($elm_to_show.removeClass(flags.hidden_class)).removeClass(flags.hidden_class),
			_fade = $('#fade').removeClass(flags.hidden_class);
	}

	//Preview of the image just uploaded //TODO final Touch required
	function showPreview(response) {
		setTimeout(function() { hideLoading(); }, 50);
		var $em = '<img src="/static/images/123/123_prf_snap.png" alt="Profile Pic" class="_ui_tmp_prf_pic_upl" id="_ui_tmp_prf_pic_upl" onload="new UIMCroputil().applyCropingAndPreview();"/>';
		var $save_button = $('#_ui_first_time_prf_up_snap');
		$save_button.removeClass(flags.hidden_class);
		$('#_uim_upl_snap_prv').html($em).removeClass(flags.hidden_class);
		$('#_uim_upl_snap_prv_hldr').removeClass(flags.hidden_class);
	}
	//Hide the loading icon just displayed
	function hideLoading(){
		var $elm_to_show = $('#_ui_img_load_wt').addClass(flags.hidden_class),
			_pop_up = $('#popup').addClass(flags.hidden_class);
			_fade = $('#fade').addClass(flags.hidden_class);
		$elm_to_show.insertAfter(_fade);
	}
	
	function updateError(res){
		setTimeout(function() { hideLoading(); }, 50);
		console.log(res);
		//TODO update the error document.
	};
	
	//on click of File Select	
	$('#snapupload').on('change','#prf_snap',function(e){
		var $form = $('#snapupload'), 
			options= {
			  dataType: 'json',
			  url: $form.attr("data-snap-upload-url"),
			  beforeSubmit: showLoading,
			  success: showPreview,
			  error: updateError,
			};
		$form.ajaxSubmit(options);
		e.preventDefault();
	});
	//On Click of image save//TODO complete this once done
	flags.wrap.find('#snapupload').on('click', '#_ui_first_time_prf_up_snap', function(e){
		var dataURL = document.getElementById('canvasThumbResult').toDataURL("image/png");
		flags.wrap.find('#_ui_prf_crop_fn').val(dataURL);
		var options= {
				  dataType: 'json',
				  url: '/appl/test/',
				  beforeSubmit: showRequest
				};
		var $form = $('#snapupload');
		$form.ajaxSubmit(options);
		return;
	});

};

//define the parameters with the default values of the function
$.fn.welcome_fst_time.defaults = {
};