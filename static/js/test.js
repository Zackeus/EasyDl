layui.use(['form','layer','jquery'],function() {
	var form = layui.form,
		$ = layui.$;
    	layer = parent.layer === undefined ? layui.layer : top.layer;


    // 监听语义标签复选框
    form.on('checkbox(lexer)',function(data) {
        if (data.elem.checked) {
            // 选中
            $("font." + data.value).addClass("lexer_font_show").removeClass("lexer_font__hide");
        } else {
            // 关闭
            $("font." + data.value).addClass("lexer_font__hide").removeClass("lexer_font_show");
        }
    });
});
