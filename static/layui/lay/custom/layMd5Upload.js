layui.extend({
    fileMd5: '{/}' + ctxStatic + 'js/browser-md5-file-1.0.0/browser-md5-file'
}).define(['table', 'form', 'upload', 'layer', 'element', 'fileMd5'],function(exports) {
    var $ = layui.jquery,
        table=layui.table,
        form = layui.form,
        upload = layui.upload,
        layer = layui.layer,
        element = layui.element,
        fileMd5 = layui.fileMd5,
        fileMime = '*',
        fileSize = 100*1024*1024,
        fileExts = 'doc|docx|pdf|xls|xlsx|ppt|pptx|gif|jpg|jpeg|bmp|png|rar|zip',
        fileNum = 0,
        fileListView,
        uploadListIns;

    layui.link(ctxStatic + 'css/public.css');
    layui.link(ctxStatic + 'layui/css/layui.css');

    //创建监听函数
    var xhrOnProgress = function(fun) {
        //绑定监听
        xhrOnProgress.onprogress = fun;
         //使用闭包实现监听绑
        return function() {
            //通过$.ajaxSettings.xhr();获得XMLHttpRequest对象
            var xhr = $.ajaxSettings.xhr();
            //判断监听函数是否为函数
            if (typeof xhrOnProgress.onprogress !== 'function')
                return xhr;
            //如果有监听函数并且xhr对象支持绑定时就把监听函数绑定上去
            if (xhrOnProgress.onprogress && xhr.upload) {
                xhr.upload.onprogress = xhrOnProgress.onprogress;
            }
            return xhr;
         }
    };

    var Class = function (options) {
        console.log(options);
        let that = this;
        that.options = options;
        that.register();
        that.init();
        that.events();
    };

    Class.prototype.register = function () {

    };

    Class.prototype.init=function(){
        let that = this,
            options = that.options;

        fileSize = !that.strIsNull(options.size) ? options.size : fileSize;
        fileExts = !that.strIsNull(options.exts) ? options.exts : fileExts;
        fileMime = !that.strIsNull(options.acceptMime) ? options.acceptMime : fileMime;
        fileNum = !that.strIsNull(options.number) ? options.number : fileNum;

        layer.open({
            type: 1,
            area: ['900px', '500px'], //宽高
            resize: true,
            maxmin: true,
            content:
                '<div class="layui-upload">' +
                    '<button type="button" class="layui-btn layui-btn-normal" id="fileList" style="float: left;margin: 5px 5px 10px 5px;">添加附件</button>' +
                    '<button type="button" class="layui-btn" id="fileAction" style="float: left;margin: 5px 5px 10px 5px;">开始上传</button>' +
                    '<button type="button" class="layui-btn" id="hideFileAction" style="display: none;">开始上传</button>' +
                    '<div class="layui-upload-list">' +
                        '<table class="layui-table" lay-size="sm" id="extend-uploader-form" lay-filter="extend-uploader-form">' +
                            '<thead>' +
                                '<tr>' +
                                    '<th><div class="layui-table-cell laytable-cell-2-status" align="center"><span>文件名</span></div></th>' +
                                    '<th><div class="layui-table-cell laytable-cell-2-status" align="center"><span>大小</span></div></th>' +
                                    '<th><div class="layui-table-cell laytable-cell-2-status" align="center"><span>验证状态</span></div></th>' +
                                    '<th><div class="layui-table-cell laytable-cell-2-status" align="center"><span>文件验证</span></div></th>' +
                                    '<th><div class="layui-table-cell laytable-cell-2-status" align="center"><span>上传状态</span></div></th>' +
                                    '<th><div class="layui-table-cell laytable-cell-2-status" align="center"><span>进度</span></div></th>' +
                                    '<th><div class="layui-table-cell laytable-cell-2-status" align="center"><span>操作</span></div></th>' +
                                '</tr>' +
                            '</thead>' +
                            '<tbody id="fileListView"></tbody>' +
                        '</table>' +
                    '</div>' +
                '</div>',
            success: function(layero, index){
                fileListView = $('#fileListView');
                uploadListIns = upload.render({
                    elem: '#fileList',
                    url: options.url,                                                       // 这里设置自己的上传接口
                    headers:{                                                               // 接口的请求头, layui 2.2.6 开始新增
                        'X-CSRFToken': $("meta[name=csrf-token]").attr("content")
                    },
                    xhr: xhrOnProgress,
                    progress: function(index, value) {                                      //上传进度回调 value进度值
                        element.progress('file' + index, value+'%');                        //设置页面进度条
                    },
                    field: 'file',                                                          // 设定文件域的字段名
                    accept: 'file',                                                         // 指定允许上传时校验的文件类型
                    acceptMime: fileMime,                                                   // 规定打开文件选择框时，筛选出的文件类型，值为用逗号隔开
                    exts: fileExts,                                                         // 许上传的文件后缀。一般结合 accept 参数类设定
                    auto: false,                                                            // 是否选完文件后自动上传
                    multiple: true,
                    bindAction: '#hideFileAction',                                          // 指向一个按钮触发上传，一般配合 auto: false 来使用
                    size: fileSize,
                    number: fileNum,
                    drag: true,                                                             // 是否接受拖拽的文件上传，设置 false 可禁用。不支持ie8/9
                    choose: function(obj) {
                        var uploadThat = this;
                        obj.preview(function(index, file, result) {     //读取本地文件
                            var files = uploadThat.files = obj.pushFile();    //将每次选择的文件追加到文件队列

                            let tr = $([
                                '<tr id="upload-'+ index +'">',
                                    '<td class="name" align="center"><a class="upload-img-prev-link" href="javascript:;">'+ file.name +'</a></td>',
                                    '<td align="center">'+ that.formatFileSize(file.size) + '</td>',
                                    '<td class="verify-state" align="center">等待验证</td>',
                                    '<td class="verify-progress">',
                                        '<div class="layui-progress layui-progress-big layui-progress-radius-fix" lay-showpercent="true" lay-filter="file-verify'+index+'">',
                                        '<div class="layui-progress-bar" lay-percent="0%">',
                                        '<span class="layui-progress-text">0%</span>',
                                        '</div>',
                                        '</div>',
                                    '</td>',
                                    '<td class="upload-state" align="center">等待上传</td>',
                                    '<td class="upload-progress">',
                                        '<div class="layui-progress layui-progress-big layui-progress-radius-fix" lay-showpercent="true" lay-filter="file'+index+'">',
                                        '<div class="layui-progress-bar" lay-percent="0%">',
                                        '<span class="layui-progress-text">0%</span>',
                                        '</div>',
                                        '</div>',
                                    '</td>',
                                    '<td class="operate" align="center">',
                                        '<button class="layui-btn layui-btn-sm file-reload layui-hide">重传</button>',
                                        '<button class="layui-btn layui-btn-sm layui-btn-danger file-delete">删除</button>',
                                    '</td>',
                                '</tr>'].join(''));

                            //单个重传
                            tr.find('.file-reload').on('click', function(){
                                $(this).addClass("layui-btn-disabled").prop("disabled", true).text("重传中…");
                                obj.upload(index, file);
                            });

                            //删除
                            tr.find('.file-delete').on('click', function(){
                              delete files[index]; //删除对应的文件
                              tr.remove();
                              uploadListIns.config.elem.next()[0].value = ''; //清空 input file 值，以免删除后出现同名文件不可选
                            });

                            fileListView.append(tr);

                            // 文件校验 计算MD5
                            fileMd5(file, function (err, md5) {
                                if (!$.isEmptyObject(err)) {
                                    // 文件md5 计算失败
                                    tr.children('td.verify-state').html('<span style="color: #ff5722;">验证失败</span>');
                                    setTimeout(function () {
                                        element.progress('file-verify' + index, '0%');
                                    }, 200);
                                    return;
                                }
                                // 添加 md5 属性
                                file.md5 = md5;
                                tr.children('td.verify-state').html('<span style="color: #5FB878;">验证成功</span>');

                            }, function (progress) {
                                element.progress('file-verify' + index, progress+'%');
                            });
                        });
                    },
                    before: function(obj) {

                    },
                    done: function(res, index, upload) {
                        //上传成功
                        if(res.code === '0'){
                            let tr = fileListView.find('tr#upload-'+ index);
                            tr.children('td.verify-progress').find('.layui-progress-bar').css('background-color','#86EAA1');
                            tr.children('td.upload-state').html('<span style="color: #5FB878;">上传成功</span>');
                            tr.children('td.upload-progress').find('.layui-progress-bar').css('background-color','#86EAA1');

                            tr.children('td.operate').find('.file-reload').text("重传").attr("disabled", false).removeClass("layui-btn-disabled");
                            tr.children('td.operate').find('.file-reload').addClass('layui-hide');
                            return delete this.files[index]; //删除文件队列已经上传成功的文件
                        }
                        this.error(index, upload);
                    },
                    allDone: function(obj) {
                        // 当文件全部被提交后，才触发
                        $('#fileAction').text("开始上传").attr("disabled", false).removeClass("layui-btn-disabled");
                    },
                    error: function(index, upload){
                        let tr = fileListView.find('tr#upload-'+ index);
                        tr.children('td.upload-state').html('<span style="color: #ff5722;">上传失败</span>');

                        //重置页面进度条
                        setTimeout(function () {
                            tr.children('td.upload-progress').find('.layui-progress-bar').css('background-color','#ff5722');
                            element.progress('file' + index, '0%');
                        }, 100);

                        // 显示重传
                        tr.children('td.operate').find('.file-reload').text("重传").attr("disabled", false).removeClass("layui-btn-disabled");
                        tr.children('td.operate').find('.file-reload').removeClass('layui-hide');
                    }
                });
            },
            end:function () {
                // 可以自行添加按钮关闭,关闭请清空rowData
                if(options.openEnd && typeof options.openEnd==='function') {
                    options.openEnd();
                }
            }
        });
    };

    Class.prototype.events=function () {
        let that = this,
            options = that.options;

        $('#fileAction').click(function () {
            let uoloadConfig = uploadListIns.config;
            let files = uoloadConfig.files;
            if ($.isEmptyObject(files)) {
                // 待上传文件列表为空
                return layer.msg('请选择上传文件', {icon: 5,time: 2000,shift: 6}, function(){});
            }

            let fileNum = Object.keys(uoloadConfig.files).length;
            if (uoloadConfig.number && fileNum > uoloadConfig.number) {
                // 上传文件数超过最大限制数
                return layer.msg('同时最多只能上传的数量为：' + uoloadConfig.number,
                    {icon: 5,time: 2000,shift: 6},
                    function(){});
            }

            let $uploadBtn = $(this);
            $uploadBtn.addClass("layui-btn-disabled").prop("disabled", true).text("上传中…");

            let ajaxArray = [];
            for (let fileIndex in files) {
                if (!$.isEmptyObject(files[fileIndex].md5)) {
                    let tr = fileListView.find('tr#upload-'+ fileIndex);
                    // MD5 不为空，先进行MD5校验
                    ajaxArray.push(
                        new Promise(function (resolve, reject) {
                            $.ajax({
                                method: 'POST',
                                url : options.md5Url,
                                data : JSON.stringify({
                                    md5Id: files[fileIndex].md5,
                                }),
                                headers:{'X-CSRFToken': $("meta[name=csrf-token]").attr("content")},
                                contentType : 'application/json',
                                dataType : 'json',
                                beforeSend: function() {
                                    element.progress('file' + fileIndex, '1%');
                                },
                                success : function(res) {
                                    if(res.code === '0') {
                                        tr.children('td.verify-progress').find('.layui-progress-bar').css('background-color','#86EAA1');
                                        tr.children('td.upload-state').html('<span style="color: #5FB878;">上传成功</span>');
                                        tr.children('td.upload-progress').find('.layui-progress-bar').css('background-color','#86EAA1');
                                        tr.children('td.operate').find('.file-reload').addClass('layui-hide');
                                        // 更新进度条
                                        element.progress('file' + fileIndex, '100%');
                                        // md5 查询成功，使用md5上传，删除要上传文件列表
                                        delete files[fileIndex]
                                    }
                                    resolve(res);
                                },
                                error : function(event) {
                                    resolve({code: '-1', msg: '请求失败'});
                                }
                            })
                        })
                    );
                }
            }

            Promise.all(ajaxArray).then(function (resList) {
                // 全部请求成功
                if ($.isEmptyObject(files)) {
                    return $uploadBtn.text("开始上传").attr("disabled", false).removeClass("layui-btn-disabled");
                }
                $('#hideFileAction').trigger('click');
            });
        });
    };

    Class.prototype.formatFileSize=function(size){
        let fileSize = 0;
        if(size/1024>1024){
            let len = size/1024/1024;
            fileSize = len.toFixed(2) + " MB";
        }else if(size/1024/1024>1024){
            let len = size/1024/1024;
            fileSize = len.toFixed(2) + " GB";
        }else{
            let len = size/1024;
            fileSize = len.toFixed(2) + " KB";
        }
        return fileSize;
    };

    Class.prototype.strIsNull=function (str) {
        return typeof str == "undefined" || str == null || str === "";
    };

    var layMd5Upload = {
        render: function (options) {
            return new Class(options);
        }
    };

    exports('layMd5Upload', layMd5Upload);
});