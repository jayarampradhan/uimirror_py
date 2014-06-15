var UIMCroputil = function(_c_id, _img, _context){
	this.init(_c_id, _img, _context);
};

$.extend(UIMCroputil.prototype,{
	//"use strict";
	// object variables
	_canvas_id: '',
	_img: '',
	_context: '',
	
	init: function(_c_id, _img, _context, _elm) {
	     // do initialization here
		if(_elm)
			this._elm = _elm;
		if(_c_id)
			this._canvas_id = _c_id;
		if(_img)
			this._img = _img;
		this._context = _context || '2d';
	},
	showCoords: function(_c_id, _img, _context){// show all coords
		return function (c){
			new UIMCroputil(_c_id, _img, _context).drawimage(c.x, c.y, c.w, c.h);
		}
		
	},
	drawimage: function(x_cord, y_cord, w_cord, h_cord){
		var canvas = document.getElementById(this._canvas_id),
	    	context = canvas.getContext(this._context),
	    	img = document.getElementById(this._img),
	        $img = $(img),
	        imgW = img.width,
	        imgH = img.height;
	    
	    var ratioY = imgH / $img.height(),
	        ratioX = imgW / $img.width();
	    
	    var getX = x_cord * ratioX,
	        getY = y_cord * ratioY,
	        getWidth = w_cord * ratioX,
	        getHeight = h_cord * ratioY;
	    
	    context.drawImage(img,getX,getY,getWidth,getHeight,0,0,160,160);
	}
}); 