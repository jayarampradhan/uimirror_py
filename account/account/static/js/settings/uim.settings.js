$("#uimLeftMenuTogl").click(function(e) {
        e.preventDefault();
        var togel_ico = $('#uimLeftMenuToglIco');
        if(togel_ico.hasClass('glyphicon-indent-left')){
        	togel_ico.removeClass('glyphicon-indent-left').addClass('glyphicon-indent-right');
        }else{
        	togel_ico.removeClass('glyphicon-indent-right').addClass('glyphicon-indent-left');
        }
        $("#wrapper").toggleClass("active");
});