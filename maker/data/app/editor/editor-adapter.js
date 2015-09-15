var Maker = {
	
	save : function(image, comments) {
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

addon.port.on('screenshot', Maker.__fireScreenshot.bind(Maker));