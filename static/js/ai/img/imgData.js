layui.extend({
	requests: '{/}' + ctxStatic + 'layui/requests'
});

layui.use(['form', 'layer', 'table', 'requests'],function(){
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery,
        table = layui.table,
        requests = layui.requests;

    layer.load();
    var imgDataListIns =  table.render({
        elem: '#imgDataList',
        title: '图片流水',							//  定义 table 的大标题（在文件导出等地方会用到）layui 2.4.0 新增
        method : 'GET',							    // 	接口http请求类型，默认：get
        url : ctx + 'ai/img/img_data/page',
        toolbar: '#imgDataListToolBar',
        contentType: 'application/json',			// 	发送到服务端的内容编码类型
        cellMinWidth : 50, 							//	（layui 2.2.1 新增）全局定义所有常规单元格的最小宽度（默认：60），一般用于列宽自动分配的情况。其优先级低于表头参数中的 minWidth
        loading : true, 							//	是否显示加载条
        page : true,
        limit : 15, 								//	每页显示的条数（默认：10）。值务必对应 limits 参数的选项。优先级低于 page 参数中的 limit 参数。
        limits : [10,15,20,25], 					//	每页条数的选择项
        id : "imgDataList", 						//	设定容器唯一ID
        text: { 									//	自定义文本
            none: '暂无相关数据' 						//	默认：无数据。注：该属性为 layui 2.2.5 开始新增
        },
        parseData: function(res) { 					//解析成 table 组件所规定的数据 layui 2.4.0 开始新增
        	return {
              'code': res.code, 					//解析接口状态
              'msg': res.msg, 						//解析提示文本
              'count': res.total, 					//解析数据长度
              'data': res.data 						//解析数据列表
            };
        },
        request: {									// 定义前端 json 格式
        	  pageName: 'page', 					// 页码的参数名称，默认：page
        	  limitName: 'pageSize' 				// 每页数据量的参数名，默认：limit
        },
        cols : [[
            {field: 'appId', title: '应用ID', align:'center'},
            {field: 'appSysCode', title: '系统代号', align:'center'},
            {field: 'pageNum', title: '总数', align:'center', sort: 'true'},
            {field: 'successNum', title: '成功数', align:'center', sort: 'true'},
            {field: 'failNum', title: '失败数', align:'center', sort: 'true'},
            {templet: '#imgData-isHandle', align: 'center', title: '处理进度'},
            {templet: '#imgData-isPush', align: 'center', title: '推送进度'},
            {field: 'createDate', title: '创建时间', align:'center', sort: 'true', templet: function(d) {
                return new Date(d.createDate).toLocaleString();
            }},
            {field: 'updateDate', title: '更新时间', align:'center', sort: 'true', templet: function(d) {
                return new Date(d.updateDate).toLocaleString();
            }},
            {field: 'remarks', title: '备注', align:'center'},
            {templet:'#imgDataListBar', title: '操作', fixed:"right", align: 'center'}
        ]],
        done: function(res, curr, count) {
        	layer.closeAll('loading');
        }
    });

    form.on('submit(search)', function(data) {
    	imgDataListIns.reload({
    		where: data.field,
    		page: {curr: 1}
    	});
    	return false;
    });

    //列表操作
    table.on('tool(imgDataList)', function(obj){
		switch (obj.event) {

		case "add":
			// addDict(obj.data.id);
			break;

		case "edit":
			break;

		case "del":
		    // delDict(obj.data);
			break;

        case "browse":
            browseImg(obj.data.id);
            browseFiles(obj.data.id);
            // browseDemo(obj.data.id);
            break;

		default:
			break;
		}
    });

    // 浏览图片
    function browseImg(data) {
    	let url = ctx + 'ai/img/img_files/flow_page/' + data + '.html';

    	layui.layer.open({
            type: 2,
            title: '图片管理', 		// 不显示标题栏
            area: ['25%','95%'],
            offset: 'r',
            resize: true,
            closeBtn: 1,			// 关闭按钮
            shade: 0, 				// 遮罩
            shadeClose: false, 		// 是否点击遮罩关闭
            anim: 0, 				// 弹出动画
            isOutAnim: true, 		// 关闭动画
            scrollbar: false, 		// 是否允许浏览器出现滚动条
            maxmin: true, 			// 最大最小化
            id: 'LAY_IMG', 		    // 用于控制弹层唯一标识
            moveType: 1,
            content: [url],
            success : function(layero, index) {
            },
            cancel: function(index, layero) {
            },
            end:function(index) {
            	imgDataListIns.reload();
           }
    	});
	}

	// 浏览源文件
    function browseFiles(data) {
    	let url = ctx + 'ai/img/img_source_files/flow_page/' + data + '.html';

    	layui.layer.open({
            type: 2,
            title: '文件管理', 		// 不显示标题栏
            area: ['40%','95%'],
            offset: 'l',
            resize: true,
            closeBtn: 1,			// 关闭按钮
            shade: 0, 				// 遮罩
            shadeClose: false, 		// 是否点击遮罩关闭
            anim: 0, 				// 弹出动画
            isOutAnim: true, 		// 关闭动画
            scrollbar: false, 		// 是否允许浏览器出现滚动条
            maxmin: true, 			// 最大最小化
            id: 'LAY_FILE', 		// 用于控制弹层唯一标识
            moveType: 1,
            content: [url],
            success : function(layero, index) {
            },
            cancel: function(index, layero) {
            },
            end:function(index) {
            	imgDataListIns.reload();
           }
    	});
	}

	// 西安演示
    function browseDemo(data) {
    	let url = data === "" || data == null || data === undefined ?
            (ctx + 'ai/img/files_demo/manage') : (ctx + 'ai/img/files_demo/manage/' + data);

    	let filesDemoIndex = layui.layer.open({
            type: 2,
            title: '文件处理', 		// 不显示标题栏
            closeBtn: 1,			// 关闭按钮
            shade: 0, 				// 遮罩
            shadeClose: false, 		// 是否点击遮罩关闭
            anim: 0, 				// 弹出动画
            isOutAnim: true, 		// 关闭动画
            scrollbar: true, 		// 是否允许浏览器出现滚动条
            maxmin: true, 			// 最大最小化
            id: 'LAY_FILE_DEMO', 	// 用于控制弹层唯一标识
            moveType: 1,
            content: [url],
            success : function(layero, index) {
                setTimeout(function(){
                    layui.layer.tips('点击此处返回菜单列表', '.layui-layer-setwin .layui-layer-close', {
                        tips: 3
                    });
                },500)
            },
            cancel: function(index, layero) {
            },
            end:function(index) {
                $(window).unbind("resize", filesDemoResize);
            	imgDataListIns.reload();
           }
    	});

    	layui.layer.full(filesDemoIndex);
        window.sessionStorage.setItem("filesDemoIndex", filesDemoIndex);
        //改变窗口大小时，重置弹窗的宽高，防止超出可视区域（如F12调出debug的操作）
        $(window).on("resize", filesDemoResize = function() {
            layui.layer.full(window.sessionStorage.getItem("filesDemoIndex"));
        });
	}

    //控制表格编辑时文本的位置【跟随渲染时的位置】
    $("body").on("click",".layui-table-body.layui-table-main tbody tr td",function() {
        $(this).find(".layui-table-edit").addClass("layui-"+$(this).attr("align"));
    });
});