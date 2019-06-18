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
    var dictListtIns =  table.render({
        elem: '#dictList',
        title: '字典表',								//  定义 table 的大标题（在文件导出等地方会用到）layui 2.4.0 新增
        method : 'GET',							    // 	接口http请求类型，默认：get
        url : ctx + 'sys/dict/page',
        toolbar: '#dictListToolBar',
        contentType: 'application/json',			// 	发送到服务端的内容编码类型
        cellMinWidth : 50, 							//	（layui 2.2.1 新增）全局定义所有常规单元格的最小宽度（默认：60），一般用于列宽自动分配的情况。其优先级低于表头参数中的 minWidth
        loading : true, 							//	是否显示加载条
        page : true, 
        limit : 15, 								//	每页显示的条数（默认：10）。值务必对应 limits 参数的选项。优先级低于 page 参数中的 limit 参数。
        limits : [10,15,20,25], 					//	每页条数的选择项
        id : "dictList", 							//	设定容器唯一ID
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
            {field: 'value', title: '键值', align:'center'},
            {field: 'label', title: '标签', align:'center'},
            {field: 'type', title: '类型', align:'center'},
            {field: 'description', title: '描述', align:'center'},
            {field: 'sort', title: '排序', sort: 'true', align:'center'},
            {field: 'remarks', title: '备注', align:'center'},
            {title: '操作', fixed:"right", align: 'center', templet:'#dictListBar'}
        ]],
        done: function(res, curr, count) {
        	layer.closeAll('loading');
        }
    });
    
    form.on('submit(search)', function(data) {
    	dictListtIns.reload({
    		where: data.field,
    		page: {curr: 1}
    	});
    	return false;
    });
    
    //头工具栏事件
    table.on('toolbar(dictList)', function(obj) {
      switch(obj.event) {
      
        case 'add':
        	addDict();
        break;
      };
    });
    
    //列表操作
    table.on('tool(dictList)', function(obj){
		switch (obj.event) {
		
		case "add":
			addDict(obj.data.id);
			break;
			
		case "edit":
			break;
			
		case "del":
		    delDict(obj.data);
			break;
			
		default:
			break;
		}
    });
    
    // 添加字典
    function addDict(data) {
    	var url = data === "" || data == null || data === undefined ?
            (ctx + 'sys/dict/add') : (ctx + 'sys/dict/add/' + data);
    	
    	var addDictIndex = layui.layer.open({
            type: 2,
            title: '添加字典', 		// 不显示标题栏
            closeBtn: 1,			// 关闭按钮
            shade: 0, 				// 遮罩
            shadeClose: false, 		// 是否点击遮罩关闭
            anim: 0, 				// 弹出动画
            isOutAnim: true, 		// 关闭动画
            scrollbar: false, 		// 是否允许浏览器出现滚动条
            maxmin: true, 			// 最大最小化
            id: 'LAY_AddDict', 		// 用于控制弹层唯一标识
            moveType: 1,
            content: [url],
            success : function(layero, index) {
                //改变窗口大小时，重置弹窗的宽高，防止超出可视区域（如F12调出debug的操作）
                $(window).on("resize", addDictResize = function() {
                    layui.layer.full(window.sessionStorage.getItem("addDictIndex"));
                });

                var body = layui.layer.getChildFrame('body', index);
                setTimeout(function() {
                    layui.layer.tips('点击此处返回字典列表', '.layui-layer-setwin .layui-layer-close', {
                        tips: 3
                    });
                }, 500)
            },
            cancel: function(index, layero) {
            },
            end:function(index) {
                $(window).unbind("resize", addDictResize);
            	dictListtIns.reload();
           }
    	});
    	layui.layer.full(addDictIndex);
        window.sessionStorage.setItem("addDictIndex", addDictIndex);
	}

	// 删除字典
    function delDict(data) {
        layer.msg('确定要删除此字典?', {
        	time: 0,
        	btn: ['确定', '取消'],
            btn1: function(index, layero) {
            	requests.doDelDict(data, index, dictListtIns);
            },
            btn2: function(index, layero) {
            	layer.close(index);
            }
        });
    }

    //控制表格编辑时文本的位置【跟随渲染时的位置】
    $("body").on("click",".layui-table-body.layui-table-main tbody tr td",function() {
        $(this).find(".layui-table-edit").addClass("layui-"+$(this).attr("align"));
    });

});