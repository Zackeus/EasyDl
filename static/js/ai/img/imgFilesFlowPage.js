layui.extend({
	fileflow: '{/}' + ctxStatic + 'layui/lay/custom/fileflow'
});

layui.use(['form', 'layer', 'fileflow'], function() {
    var form = layui.form,
        layer = layui.layer,
        fileflow = layui.fileflow,
        $ = layui.jquery;

    //流加载图片
    fileflow.img({
        url: ctx + 'ai/img/img_files/flow_page',
        headers: {'X-CSRFToken': $("meta[name=csrf-token]").attr("content")},
        method: 'GET',
        data: {
            imgDataId: $("meta[name=img_data_id]").attr("content")
        },
        contentType: 'application/json',
        elem: '#Images',                //流加载容器
        isAuto: true,
        imgNums: 10
    });
});