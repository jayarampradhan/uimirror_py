var UIMTemplateutil = function(_data, res_call_back, _ext, _url){
	this.init(_data, res_call_back, _ext, _url);
};

$.extend(UIMTemplateutil.prototype,{
	//"use strict";
	// object variables
		res_call_back: '',
		_url:'../static/js/template/_',
		_ext: '.tmpl.html',
		_data: '',
		
	init: function(_data, call_back, _ext, _url) {
	     // do initialization here
		if(_data)
			this._data = _data;
		if(call_back)
			this.res_call_back = call_back;
		if(_url)
			this._url = _url;
		if(_ext)
			this._ext = _ext;
	},
	getPath: function(name){
		return this._url + name + this._ext;
	},
	renderExtTemplate: function(){
		var file = this.getPath( this._data.name );
		var _this = this;
		$.when($.get(file)).done(function(tmplData) {
	         $.templates({ tmpl: tmplData });
	         var _res = $.render.tmpl(_this._data.data);
	         if(_this._data.selector)
	        	 $(_this._data.selector).html(_res);
	         if($.isFunction(_this.res_call_back))
	        	 _this.res_call_back.call(this,$(_res));
	     });
	}
	
}); 