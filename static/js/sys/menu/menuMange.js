layui.extend({
	treetable: '{/}' + ctxStatic + '/layui/lay/tree/treetable',
	requests: '{/}' + ctxStatic + '/layui/requests'
});	
	    
layui.use(['table', 'treetable', 'requests', 'layer'], function() {
    var $ = layui.jquery,
    	layer = parent.layer === undefined ? layui.layer : top.layer,
    	table = layui.table,
    	treetable = layui.treetable,
    	requests = layui.requests;

    // 渲染表格
    layer.load();
    var menuListIns = treetable.render ({
        treeColIndex: 1,						// 树形图标显示在第几列
        treeSpid: 1,							// 最上级的父级id
        treeIdName: 'id',						// id字段的名称
        treePidName: 'parentId',				// pid字段的名称
        treeDefaultClose: false,				// 是否默认折叠
        treeLinkage: true,						// 父级展开时是否自动展开所有子级
        elem: '#menulist',
        url: ctx + 'sys/menu/manage',
        page: false,
        cols: [[
            {type: 'numbers'},
            {field: 'name', minWidth: 170, title: '菜单名称'},
            {field: 'href', align: 'center', title: '链接'},
            {templet: '#menu-icon', width: 80,  align: 'center', title: '图标'},
            {field: 'sort', width: 80, align: 'center', title: '排序'},
            {templet: '#menu-operate', width: 180, align: 'center', title: '操作'}
        ]],
        done: function () {
            layer.closeAll('loading');
        }
    });
    
    //列表操作
    table.on('tool(menulist)', function(obj){
		switch (obj.event) {
		
		case "add":
			addSublevelMenu(obj.data);
			break;
			
		case "edit":
			editMenu(obj.data);
			break;
			
		case "del":
			delMenu(obj.data);
			break;
			
		default:
			break;
		}
    });
    
    // 添加子级菜单
    function addSublevelMenu(data) {
    	openAddMenu(data.id);
	}
    
    function editMenu(data) {
    	var editMenuIndex = layui.layer.open({
            type: 2,
            title: '编辑菜单', 		// 不显示标题栏
            closeBtn: 1,			// 关闭按钮
            shade: 0, 				// 遮罩
            shadeClose: false, 		// 是否点击遮罩关闭
            anim: 0, 				// 弹出动画
            isOutAnim: true, 		// 关闭动画
            scrollbar: false, 		// 是否允许浏览器出现滚动条
            maxmin: true, 			// 最大最小化
            id: 'LAY_EditMenu', 	// 用于控制弹层唯一标识
            moveType: 1,
            content: [ctx + 'sys/menu/edit/' + data.id],
            success : function(layero, index){
                var body = layui.layer.getChildFrame('body', index);
                setTimeout(function(){
                    layui.layer.tips('点击此处返回菜单列表', '.layui-layer-setwin .layui-layer-close', {
                        tips: 3
                    });
                },500)
            },
            end:function(index) {
            	menuListIns.reload();
           }
    	});
    	layui.layer.full(editMenuIndex);
        window.sessionStorage.setItem("editMenuIndex", editMenuIndex);
        $(window).on("resize",function() {
        	layui.layer.full(window.sessionStorage.getItem("editMenuIndex"));
        })
		
	}
    
    // 删除菜单
    function delMenu(data) {
        layer.msg('确定要删除此菜单?', {
        	time: 0, 
        	btn: ['确定', '取消'],
            btn1: function(index, layero) {
            	requests.delMenu(data, index, ctx + 'sys/menu/del', menuListIns);
            },
            btn2: function(index, layero) {
            	layer.close(index);
            }
        });
    }
    
    // 添加菜单
    $('#btn-add').click(function () {
    	openAddMenu('1');
    });
    
    // 打开添加菜单页面
    function openAddMenu(id) {
    	var addMenuIndex = layui.layer.open({
            type: 2,
            title: '增加菜单', 		// 不显示标题栏
            closeBtn: 1,			// 关闭按钮
            shade: 0, 				// 遮罩
            shadeClose: false, 		// 是否点击遮罩关闭
            anim: 0, 				// 弹出动画
            isOutAnim: true, 		// 关闭动画
            scrollbar: false, 		// 是否允许浏览器出现滚动条
            maxmin: true, 			// 最大最小化
            id: 'LAY_AddMenu', 		// 用于控制弹层唯一标识
            moveType: 1,
            content: [ctx + 'sys/menu/add/' + id],
            success : function(layero, index) {
                var body = layui.layer.getChildFrame('body', index);
                setTimeout(function(){
                    layui.layer.tips('点击此处返回菜单列表', '.layui-layer-setwin .layui-layer-close', {
                        tips: 3
                    });
                },500)
            },
            cancel: function(index, layero) {
            },
            end:function(index) {
            	menuListIns.reload();
           }
    	});
    	layui.layer.full(addMenuIndex);
        window.sessionStorage.setItem("addMenuIndex", addMenuIndex);
        //改变窗口大小时，重置弹窗的宽高，防止超出可视区域（如F12调出debug的操作）
        $(window).on("resize",function() {
        	layui.layer.full(window.sessionStorage.getItem("addMenuIndex"));
        })
    }

    // 全部展开
    $('#btn-expand').click(function () {
        treetable.expandAll('#menulist');
    });

    // 全部折叠
    $('#btn-fold').click(function () {
        treetable.foldAll('#menulist');
    });
});