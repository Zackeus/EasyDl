layui.define(['jquery','layer'], function(exports) {
	let	$ = layui.$,
		layer = parent.layer === undefined ? layui.layer : top.layer;

	let requests = {
		// post 提交json数据
		doPostJson: function (url, data, before, success, error) {
			$.ajax({
				method: 'POST',
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
		// Get 提交json数据
		doGetJdon: function (url, data, before, success, error) {
			$.ajax({
				method: 'GET',
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
        }
	};
	exports('requests', requests);
});
