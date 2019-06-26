layui.extend({
	fileflow: '{/}' + ctxStatic + 'layui/lay/custom/fileflow'
});

layui.use(['form', 'layer', 'fileflow'], function() {
    var form = layui.form,
        layer = layui.layer,
        fileflow = layui.fileflow,
        $ = layui.jquery;

    //流加载图片
    fileflow.file({
        url: ctx + 'ai/img/img_source_files/' + $("meta[name=img_data_id]").attr("content"),
        headers: {'X-CSRFToken': $("meta[name=csrf-token]").attr("content")},
        method: 'GET',
        contentType: 'application/json',
        elem: '#files',
        imgNums: 10,
        done: function() {
            $("#files img").EZView();
        }
    });

});