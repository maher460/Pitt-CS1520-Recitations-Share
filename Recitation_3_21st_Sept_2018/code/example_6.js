window.addEventListener('load', function() {
    
    console.log('All assets are loaded')

    API = (function() {
        "use strict";

        var export_list = {};

        var private_function = function(){
            // private is not available from outside
        }

        export_list.public_function = function(){
            // public is available from outside
        }

        return export_list;
    }());
})