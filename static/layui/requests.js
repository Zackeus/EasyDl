layui.define(['jquery','layer'], function(exports) {
	let	$ = layui.$,
		layer = parent.layer === undefined ? layui.layer : top.layer;

	let requests = {
		// 提交 json 数据
		doJson: function(method, url, data, before, success, error) {
			$.ajax({
				method: method,
				url : url,
				data : typeof(data) === 'string' ? data : JSON.stringify(data),
				headers:{'X-CSRFToken': $("meta[name=csrf-token]").attr("content")},
				contentType : 'application/json',
				dataType : 'json',
				beforeSend: function() {
					before && before();
				},
				success : function(result) {
					success && success(result);
				},
				error : function(event) {
					error && error(event);
				}
			});
		},
		// post 提交json数据
		doPostJson: function (url, data, before, success, error) {
			requests.doJson('POST', url, data, before, success, error);
		},
		// Get 提交json数据
		doGetJson: function (url, data, before, success, error) {
			requests.doJson('GET', url, data, before, success, error);
		},
		// delete 提交json数据
		doDeleteJson: function (url, data, before, success, error) {
			requests.doJson('DELETE', url, data, before, success, error);
		},
		// put 提交json数据
		doPutJson: function (url, data, before, success, error) {
			requests.doJson('PUT', url, data, before, success, error);
		},
		// 用户登录请求
		doLogin: function (data, loginBtn) {
			requests.doPostJson(ctx + 'sys/user/login', data,
				function () {
					loginBtn.text("登录中...").attr("disabled","disabled").addClass("layui-disabled");
                },
				function (result) {
					if (result.code === "0") {
						location.href = ctx + 'sys/index';
					} else {
						layer.msg(result.msg, {icon: 5,time: 2000,shift: 6}, function(){});
						loginBtn.text("登录").attr("disabled",false).removeClass("layui-disabled");
					}
				},
				function (event) {
					// 错误信息
					layer.msg('响应失败', {icon: 5,time: 2000,shift: 6}, function(){});
					loginBtn.text("登录").attr("disabled",false).removeClass("layui-disabled");
                }
			)
        },
		// 根据父级菜单ID获取子级菜单列表
		doGetMenus: function (id, before, success, error) {
			requests.doGetJson(ctx + 'sys/menu' + '/' + id, null, before, success, error);
		},
		// 根据 id 查询子菜单最大最大排序值
		doGetMaxMenuSort: function (id, before, success, error) {
			requests.doGetJson(ctx + 'sys/menu/max_sort' + '/' + id, null, before, success, error);
        },
		// 添加菜单
		doAddMenu: function (data, btn) {
			requests.doPostJson(ctx + 'sys/menu', data,
				function() {
					btn.text("提交中...").attr("disabled","disabled").addClass("layui-disabled");
				},
				function (res) {
					if (res.code === "0") {
						layer.msg(res.msg, {icon: 6,time: 1000});
						parent.layer.close(parent.layer.getFrameIndex(window.name));
					} else {
						layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
						btn.text("提交").attr("disabled",false).removeClass("layui-disabled");
					}
                },
				function (event) {
					layer.msg('响应失败', {icon: 5,time: 2000,shift: 6}, function(){});
					btn.text("提交").attr("disabled",false).removeClass("layui-disabled");
                })
        },
		// 删除菜单
		doDelMenu: function (data, index, tableIns) {
			requests.doDeleteJson(ctx + 'sys/menu', data,
				function() {
					layer.close(index);
					layer.load();
				},
				function (res) {
					layer.closeAll('loading');
					if (res.code === "0") {
						layer.msg(res.msg, {icon: 6,time: 1000});
						tableIns.reload();
					} else {
						layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
					}
                },
				function (event) {
					layer.closeAll('loading');
					layer.msg('响应失败', {icon: 5,time: 2000,shift: 6}, function(){});
                })
        },
		// 修改菜单
		doEditMenu: function (data, btn) {
			requests.doPutJson(ctx + 'sys/menu', data,
				function() {
					btn.text("提交中...").attr("disabled","disabled").addClass("layui-disabled");
				},
				function (res) {
					if (res.code === "0") {
						layer.msg(res.msg, {icon: 6,time: 1000});
						parent.layer.close(parent.layer.getFrameIndex(window.name));
					} else {
						layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
						btn.text("提交").attr("disabled",false).removeClass("layui-disabled");
					}
                },
				function (event) {
					layer.msg('响应失败', {icon: 5,time: 2000,shift: 6}, function(){});
					btn.text("提交").attr("disabled",false).removeClass("layui-disabled");
                })
        },
		// 添加字典
		doAddDict: function (data, btn) {
			requests.doPostJson(ctx + 'sys/dict', data,
				function() {
					btn.text("提交中...").attr("disabled","disabled").addClass("layui-disabled");
				},
				function (res) {
					if (res.code === "0") {
						layer.msg(res.msg, {icon: 6,time: 1000});
						parent.layer.close(parent.layer.getFrameIndex(window.name));
					} else {
						layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
						btn.text("提交").attr("disabled",false).removeClass("layui-disabled");
					}
                },
				function (event) {
					layer.msg('响应失败', {icon: 5,time: 2000,shift: 6}, function(){});
					btn.text("提交").attr("disabled",false).removeClass("layui-disabled");
                })
        },
		// 删除字典
		doDelDict: function (data, index, tableIns) {
			requests.doDeleteJson(ctx + 'sys/dict', data,
				function() {
					layer.close(index);
					layer.load();
				},
				function (res) {
					layer.closeAll('loading');
					if (res.code === "0") {
						layer.msg(res.msg, {icon: 6,time: 1000});
						tableIns.reload();
					} else {
						layer.msg(res.msg, {icon: 5,time: 2000,shift: 6}, function(){});
					}
                },
				function (event) {
					layer.closeAll('loading');
					layer.msg('响应失败', {icon: 5,time: 2000,shift: 6}, function(){});
                })
        }
	};
	exports('requests', requests);
});
