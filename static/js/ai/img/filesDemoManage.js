layui.extend({
	fileflow: '{/}' + ctxStatic + 'layui/lay/custom/fileflow'
});

layui.use(['form', 'layer', 'fileflow', 'element'], function() {
    var form = layui.form,
        layer = layui.layer,
        fileflow = layui.fileflow,
        $ = layui.jquery,
        element = layui.element,
        flowIerval;

    var doFlowIerval = function() {
        $('.layui-flow-more').children('a').trigger('click');
    };

    var done = function () {
        if (flowIerval == null || flowIerval === undefined || flowIerval === '') {
            flowIerval = setInterval(doFlowIerval, 1500);
        }
        $('html, body').scrollTop($('#Images li').eq($('#Images li').length - 1).offset().top);

        $('#fileListView').children('tr').each(function (ii, ee) {
            let id = $(ee).attr("id");
            let img_page = $('#Images .' + id).length;
            let totalImgPage = $(ee).children('td.img_page').text();
            element.progress('file' + id, Math.floor((img_page / totalImgPage) * 100) + '%');
        });
    };

    //流加载图片
    fileflow.img({
        url: ctx + 'ai/img/files_demo/page',
        headers: {'X-CSRFToken': $("meta[name=csrf-token]").attr("content")},
        method: 'GET',
        data: {
            imgDataId: $("meta[name=img_data_id]").attr("content")
        },
        contentType: 'application/json',
        elem: '#Images',                //流加载容器
        isAuto: false,
        imgNums: 1,
        success: function (res, page, next) {
            if (res.code === "0") {
                let imgList = [];

                layui.each(res.data, function(index, item) {
                    imgList.push('<li class="'+ item.pid +'">' +
                        '<img layer-src="'+ item.src +'" src="'+ item.thumb +'" ' +
                        'alt="'+ item.alt+'" data-sort="' + (Number(res.page - 1) * Number(res.pageSize) + Number(index)) + '">' +
                        '<div class="operate"><div class="check">' +
                        '<input type="checkbox" name="belle" lay-filter="choose" lay-skin="primary" ' +
                        'title="'+ item.alt + '">' +
                        '</div><i class="layui-icon img_del">&#xe640;</i></div></li>');
                });
                next(imgList.join(''), page < res.totalPage);
                form.render();
                $("#Images li img").height($("#Images li img").width() * 1.3);
            } else {
                next('', false);
                layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
            }
        },
        done: function () {
            done();
        }
    });
});