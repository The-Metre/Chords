window.Songlists = {};

window.Songlists.initialize = function () {
    $("input[name='text']").keypress(function(){
        $("li").hide();
    });
}


