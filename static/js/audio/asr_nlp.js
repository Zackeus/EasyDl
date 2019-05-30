layui.use(['form','layer','jquery'],function() {
	var form = layui.form,
        layer = layui.layer,
		$ = layui.$;

	// 初始化 layui
	layer.tips('', '#asrDatas', {tips: [1, '#000'], time: 1});

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

    // 监听鼠标悬停
    $(".layim-chat-text font").mouseover(function() {
        layer.tips(
            $(this).data("ne-title"),
            this,
            {tips: [1, '#000'], time: 0},
        );
    }).mouseout(function() {
        layer.closeAll('tips');
    });
});
