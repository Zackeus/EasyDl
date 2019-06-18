layui.extend({
	imgflow: '{/}' + ctxStatic + 'layui/lay/custom/imgflow'
});

layui.use(['form', 'layer', 'imgflow'], function() {
    var form = layui.form,
        layer = layui.layer,
        imgflow = layui.imgflow,
        $ = layui.jquery;

    //流加载图片
    imgflow.load({
        url: ctx + 'ai/img/img_datas',
        elem: '#Images',                //流加载容器
        imgNums: 10
    });
});