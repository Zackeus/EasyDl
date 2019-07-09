layui.define(['flow','form','layer'], function (exports) {
    var flow = layui.flow,
        form = layui.form,
        layer = layui.layer,
        $ = layui.jquery;

    var imgData = [];
    var fileflow = {
        // 加载数据
        img: function (param) {
            $(param.elem).addClass('flow-img');
            flow.load({
                elem: param.elem,                                           //流加载容器
                isAuto: param.isAuto,
                done: function(page, next) {
                    // 拼接请求参数
                    let dataJson = JSON.stringify(Object.assign({}, {
                        page: page,
                        pageSize: param.imgNums,
                    }, param.data));

                    $.ajax({
                        method: $.isEmptyObject(param.method) ? param.method : 'GET',
                        url : param.url + '?' + dataJson,
                        headers: $.isEmptyObject(param.headers) ? param.headers : '',
                        contentType : $.isEmptyObject(param.contentType) ? param.contentType : 'application/json',
                        dataType : 'json',
                        beforeSend: function() {
                        },
                        success : function(res) {
                            if (param.success && typeof param.success === 'function') {
                                layui.each(res.data, function(index, item) {
                                    imgData.push(item);
                                });
                                param.success(res, page, next);
                            } else if (res.code === "0") {
                                let imgList = [];
                                layui.each(res.data, function(index, item) {
                                    imgData.push(item);
                                    imgList.push('<li>' +
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

                            if (param.done && typeof param.done === 'function') {
                                param.done();
                            }
                        },
                        error : function(event) {
                            if (param.error && typeof param.error === 'function') {
                                return param.error(event);
                            }
                            layer.msg('响应失败', {icon: 5,time: 2000,shift: 6}, function(){});
                        }
                    });
                }
            });

            //弹出层
            $("body").on("click", param.elem + " img", function() {
                var photos = {
                    "title": "图片管理",
                    "id": param.elem,
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
                $(param.elem + " li img").height($(param.elem + " li img").width() * 1.3);
            });
        },

        file: function (param) {
            $(param.elem).addClass('flow-img');
            flow.load({
                elem: param.elem,
                isAuto: param.isAuto,
                done: function(page, next) {
                    $.ajax({
                        method: $.isEmptyObject(param.method) ? 'GET' : param.method,
                        url : param.url,
                        headers: $.isEmptyObject(param.headers) ? '' : param.headers,
                        contentType : $.isEmptyObject(param.contentType) ? 'application/json' : param.contentType,
                        dataType : 'json',
                        beforeSend: function() {

                        },
                        success : function(res) {
                            if (res.code === "0") {
                                var imgList = [];
                                    imgData = res.data;
                                var maxPage = param.imgNums*page < imgData.length ? param.imgNums*page : imgData.length;

                                for(var i= param.imgNums*(page-1); i< maxPage; i++) {
                                    switch (imgData[i].format.toUpperCase()) {
                                        case 'PDF':
                                            imgList.push('<li>' +
                                                '<img layer-src="'+ imgData[i].src +'" src="/static/images/pdf.jpg" ' +
                                                'href="'+ imgData[i].src +'" alt="'+ imgData[i].alt+'" ' +
                                                'data-sort="' + i + '">' +
                                                '<div class="operate"><div class="check">' +
                                                '<input type="checkbox" name="belle" lay-filter="choose" lay-skin="primary" ' +
                                                'title="'+imgData[i].alt+'">' +
                                                '</div><i class="layui-icon img_del">&#xe640;</i></div></li>');
                                            break;
                                        default:
                                            imgList.push('<li>' +
                                                '<img layer-src="'+ imgData[i].src +'" src="'+ imgData[i].thumb +'" ' +
                                                'alt="'+ imgData[i].alt+'" data-sort="' + i + '">' +
                                                '<div class="operate"><div class="check">' +
                                                '<input type="checkbox" name="belle" lay-filter="choose" lay-skin="primary" ' +
                                                'title="'+imgData[i].alt+'">' +
                                                '</div><i class="layui-icon img_del">&#xe640;</i></div></li>');
                                            break;
                                    }
                                }
                                next(imgList.join(''), page < (imgData.length/param.imgNums));
                                form.render();
                                $(param.elem + " li img").height($(param.elem + " li img").width() * 1.3);

                                if (param.done && typeof param.done === 'function') {
                                    param.done();
                                }
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

            //设置图片的高度
            $(window).resize(function() {
                $(param.elem + " li img").height($(param.elem + " li img").width() * 1.3);
            });
        }
    };

    //layer photo 滚轮 实现放大缩小
    $(document).on("mousewheel DOMMouseScroll", ".layui-layer-phimg img", function(e) {
            var delta = (e.originalEvent.wheelDelta && (e.originalEvent.wheelDelta > 0 ? 1 : -1)) || // chrome & ie
                (e.originalEvent.detail && (e.originalEvent.detail > 0 ? -1 : 1)); // firefox
            var imagep = $(".layui-layer-phimg").parent().parent();
            var image = $(".layui-layer-phimg").parent();
            var h = image.height();
            var w = image.width();
            if(delta > 0) {
                    h = h * 1.05;
                    w = w * 1.05;
            } else if(delta < 0) {
                if(h > 100) {
                    h = h * 0.95;
                    w = w * 0.95;
                }
            }
            imagep.css("top", (window.innerHeight - h) / 2);
            imagep.css("left", (window.innerWidth - w) / 2);
            image.height(h);
            image.width(w);
            imagep.height(h);
            imagep.width(w);
        });

    //layer photo 鼠标点击 实现旋转
    // var rotateindex = 1;
    // $(document).on("mousedown DOMMouseScroll", ".layui-layer-phimg img", function(e) {
    //     var delta = (e.originalEvent.wheelDelta && (e.originalEvent.wheelDelta > 0 ? 1 : -1)) || // chrome & ie
    //         (e.originalEvent.detail && (e.originalEvent.detail > 0 ? -1 : 1)); // firefox
    //     var imagep = $(".layui-layer-phimg").parent().parent();
    //     var deg = rotateindex*90;
    //     imagep.css("transform",'rotate('+deg+'deg)');
    //     rotateindex++;
    // });

    //删除单张图片
    $("body").on("click",".img_del", function() {
        var _this = $(this);
        layer.confirm('确定删除图片"'+_this.siblings().find("input").attr("title")+'"吗？',{icon:3, title:'提示信息'}, function(index) {
            _this.parents("li").hide(1000);
            setTimeout(function(){_this.parents("li").remove();},950);
            layer.close(index);
        });
    });

    exports('fileflow', fileflow);
});
