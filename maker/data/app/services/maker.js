var Maker = {
	screenshot : function() {
		
		addon.port.emit('screenshot');
		//self.postMessage({ command: 'screenshot'}, "*");
	},
    
    __fireAppendPage: function(data){
		this.__appendPage(data);
	},
	
	onAppendPage: function(handler){
		this.__appendPage = handler;
	}

};

addon.port.on('appendPage', Maker.__fireAppendPage.bind(Maker));