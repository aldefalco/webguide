var capture = require("./capture.js"),
    pager = require("sdk/ui/sidebar").Sidebar({
        id: 'record-bar',
        title: 'Web Guide Maker',
        url: "./app/pager/pager.html",
        onReady: function (worker) {

            pager.worker = worker;


            worker.port.on("screenshot", function () {
                console.log("Take a screenshot");
                editor.show();
                editor.port.emit('screenshot', capture.tab());
            });
            
            worker.port.on("save", function (pages) {
                console.log("Save");
                save.show();
                save.port.emit('openSave', pages);
            });

            /*
             worker.port.on("ping", function() {
             console.log("add-on script got the message");
             worker.port.emit("pong");
             });*/
        }
    }),

    editor = require("sdk/panel").Panel({
        width: 800,
        height: 600,
        contentURL: "./app/editor/editor.html"
    }),
    
    save = require("sdk/panel").Panel({
        width: 500,
        height: 300,
        contentURL: "./app/save/save.html"
    }),

    button = require("sdk/ui/button/toggle").ToggleButton({
        id: "run-btn",
        label: "Run maker",
        icon: "./open.png",
        onChange: function changed(state) {
            if (state.checked) {
                pager.show();

            } else {

                pager.hide();
            }
        }
    });

editor.port.on("save", function (page) {
    editor.hide();
    //console.log("=== save");
    //console.log(page);
    pager.worker.port.emit('appendPage', page);
});

save.port.on("complete", function () {
    save.hide();
});