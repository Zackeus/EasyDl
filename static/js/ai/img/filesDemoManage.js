layui.extend({
	fileflow: '{/}' + ctxStatic + 'layui/lay/custom/fileflow'
});

layui.use(['form', 'layer', 'fileflow', 'flow', 'element'], function() {
    var form = layui.form,
        layer = layui.layer,
        fileflow = layui.fileflow,
        $ = layui.jquery,
        flow = layui.flow,
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

    var imgData,
        imgNums = 1;
    $('#Images').addClass('flow-img');
    flow.load({
        elem: '#Images',                                           //流加载容器
        isAuto: false,
        done: function(page, next) {
            $.ajax({
                method: 'GET',
                url : ctx + 'ai/img/files_demo/' + $("meta[name=img_data_id]").attr("content"),
                headers: {'X-CSRFToken': $("meta[name=csrf-token]").attr("content")},
                contentType : 'application/json',
                dataType : 'json',
                beforeSend: function() {
                },
                success : function(res) {
                    if (res.code === "0") {
                        var imgList = [];
                            imgData = res.data;
                        var maxPage = imgNums*page < imgData.length ? imgNums*page : imgData.length;
                        setTimeout(function() {
                            for(var i= imgNums*(page-1); i< maxPage; i++){
                                imgList.push('<li class="'+ imgData[i].pid +'">' +
                                    '<img layer-src="'+ imgData[i].src +'" src="'+ imgData[i].thumb +'" ' +
                                    'alt="'+ imgData[i].alt+'" data-sort="' + i + '">' +
                                    '<div class="operate"><div class="check">' +
                                    '<input type="checkbox" name="belle" lay-filter="choose" lay-skin="primary" ' +
                                    'title="'+imgData[i].alt+'">' +
                                    '</div><i class="layui-icon img_del">&#xe640;</i></div></li>');
                            }
                            next(imgList.join(''), page < (imgData.length/imgNums));
                            form.render();
                            $("#Images li img").height($("#Images li img").width() * 1.3);

                            done();

                        }, 500);
                    } else {
                        next('', false);
                        layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
                    }
                },
                error : function(event) {
                    layer.msg('响应失败', {icon: 5,time: 2000,shift: 6}, function(){});
                }
            });
        }
    });

    //弹出层
    $("body").on("click", "#Images img", function() {
        var photos = {
            "title": "图片管理",
            "id": '#Images',
            "start": $(this).data('sort'),
        };
        photos.data = imgData;
        layer.photos({
            photos: photos,
            anim: 5
        });
    });

    //设置图片的高度
    $(window).resize(function() {
        $("#Images li img").height($("#Images li img").width() * 1.3);
    });

    //流加载图片
    // fileflow.img({
    //     url: ctx + 'ai/img/files_demo/' + $("meta[name=img_data_id]").attr("content"),
    //     headers: {'X-CSRFToken': $("meta[name=csrf-token]").attr("content")},
    //     method: 'GET',
    //     contentType: 'application/json',
    //     elem: '#Images',                //流加载容器
    //     isAuto: false,
    //     imgNums: 1,
    //     done: function () {
    //         if (flowIerval == null || flowIerval === undefined || flowIerval === '') {
    //             flowIerval = setInterval(doFlowIerval, 1500);
    //         }
    //         $('html, body').scrollTop($('#Images li').eq($('#Images li').length - 1).offset().top);
    //     }
    // });
});