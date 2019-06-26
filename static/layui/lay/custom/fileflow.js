layui.define(['flow','form','layer'], function (exports) {
    var flow = layui.flow,
        form = layui.form,
        layer = layui.layer,
        $ = layui.jquery;

    var imgData;
    var fileflow = {
        // 加载数据
        img: function (param) {
            $(param.elem).addClass('flow-img');
            flow.load({
                elem: param.elem,                                           //流加载容器
                done: function(page, next) {
                    $.ajax({
                        method: $.isEmptyObject(param.method) ? param.method : 'GET',
                        url : param.url,
                        // data : typeof(data) === 'string' ? data : JSON.stringify(data),
                        headers: $.isEmptyObject(param.headers) ? param.headers : '',
                        contentType : $.isEmptyObject(param.contentType) ? param.contentType : 'application/json',
                        dataType : 'json',
                        beforeSend: function() {
                            // before && before();
                        },
                        success : function(res) {
                            if (res.code === "0") {
                                var imgList = [];
                                    imgData = res.data;
                                var maxPage = param.imgNums*page < imgData.length ? param.imgNums*page : imgData.length;
                                setTimeout(function() {
                                    for(var i= param.imgNums*(page-1); i< maxPage; i++){
                                        imgList.push('<li>' +
                                            '<img layer-src="'+ imgData[i].src +'" src="'+ imgData[i].thumb +'" ' +
                                            'alt="'+ imgData[i].alt+'" data-sort="' + i + '">' +
                                            '<div class="operate"><div class="check">' +
                                            '<input type="checkbox" name="belle" lay-filter="choose" lay-skin="primary" ' +
                                            'title="'+imgData[i].alt+'">' +
                                            '</div><i class="layui-icon img_del">&#xe640;</i></div></li>');
                                    }
                                    next(imgList.join(''), page < (imgData.length/param.imgNums));
                                    form.render();
                                    $(param.elem + " li img").height($(param.elem + " li img").width() * 1.3);
                                }, 500);
                            } else {
                                next('', false);
                                layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
                            }
                        },
                        error : function(event) {
                            // error && error(event);
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
                done: function(page, next) {
                    $.ajax({
                        method: $.isEmptyObject(param.method) ? 'GET' : param.method,
                        url : param.url,
                        headers: $.isEmptyObject(param.headers) ? '' : param.headers,
                        contentType : $.isEmptyObject(param.contentType) ? 'application/json' : param.contentType,
                        dataType : 'json',
                        beforeSend: function() {
                            // before && before();
                        },
                        success : function(res) {
                            if (res.code === "0") {
                                var imgList = [];
                                    imgData = res.data;
                                var maxPage = param.imgNums*page < imgData.length ? param.imgNums*page : imgData.length;
                                setTimeout(function() {
                                    for(var i= param.imgNums*(page-1); i< maxPage; i++) {
                                        switch (imgData[i].format.toUpperCase()) {
                                            case 'PDF':
                                                imgList.push('<li>' +
                                                    '<img layer-src="'+ imgData[i].src +'" src="'+ imgData[i].thumb +'" ' +
                                                    'href="'+ imgData[i].src +'" alt="'+ imgData[i].alt+'" ' +
                                                    'data-sort="' + i + '">' +
                                                    '<div class="operate"><div class="check">' +
                                                    '<input type="checkbox" name="belle" lay-filter="choose" lay-skin="primary" ' +
                                                    'title="'+imgData[i].alt+'">' +
                                                    '</div><i class="layui-icon img_del">&#xe640;</i></div></li>');
                                                break;
                                            case 'JPG':
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

                                    if (param.done) {
                                        param.done();
                                    }
                                }, 500);
                            } else {
                                next('', false);
                                layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
                            }

                        },
                        error : function(event) {
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
