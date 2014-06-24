$("#uimLeftMenuTogl").click(function(e) {
        e.preventDefault();
        var togel_ico = $('#uimLeftMenuToglIco');
        if(togel_ico.hasClass('fa-caret-square-o-left')){
        	togel_ico.removeClass('fa-caret-square-o-left').addClass('fa-caret-square-o-right');
        }else{
        	togel_ico.removeClass('fa-caret-square-o-right').addClass('fa-caret-square-o-left');
        }
        $("#wrapper").toggleClass("active");
});
