let initialize = function () {
    $(document).ready(function(){
        $("input[name='text']").keypress(function(){
            $("li").hide();
        });
    });
}
