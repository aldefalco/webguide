"use strict";

var Maker = {
	screenshot : function() {
		addon.port.emit('screenshot');
		//self.postMessage({ command: 'screenshot'}, "*");
	},
    
    save : function(pages) {
		addon.port.emit('save', pages);
	},
    
    complete : function() {
		addon.port.emit('complete');
		//self.postMessage({ command: 'screenshot'}, "*");
	},
    
    __fireAppendPage: function(data){
		this.__appendPage(data);
	},
	
	onAppendPage: function(handler){
		this.__appendPage = handler;
	},
    
     __fireOpenSave: function(data){
		this.__openSave(data);
	},
	
	onOpenSave: function(handler){
		this.__openSave = handler;
	},
    
    savePage : function(image, comments) {
        image.data = null;
        image.highlighted = null;
		addon.port.emit('save', { image: image, comments: comments} );
	},
	
	__fireScreenshot: function(data){
		this.__screenshot(data);
	},
	
	onScreenshot: function(handler){
		this.__screenshot = handler;
	}
};

addon.port.on('appendPage', Maker.__fireAppendPage.bind(Maker));
addon.port.on('openSave', Maker.__fireOpenSave.bind(Maker));
addon.port.on('screenshot', Maker.__fireScreenshot.bind(Maker));