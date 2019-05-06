layui.define(['jquery','layer'],function(exports){
	var	$ = layui.$,
		layer = parent.layer === undefined ? layui.layer : top.layer;
	var customerFrom = {
			// 表单序列化Json 序列化嵌套对象
			serializeJson : function(from) {
				var serializeObj = {};
				var aray = from.serializeArray();
				$(aray).each(function() {
					if(serializeObj[this.name]) {
						if($.isArray(serializeObj[this.name])) {
							serializeObj[this.name].push(this.value);
						} else {
							serializeObj[this.name] = [serializeObj[this.name],this.value];
						}
					} else { 
						if(this.name.indexOf(".")>0) {
							//检查是否有嵌套对象
							var names = this.name.split(".");
							var objName = names[0];
							var propertyName = names[1];
							// 如果不存在 创建新对象
							if(!serializeObj[objName]) {
								serializeObj[objName] = {};
							}
							serializeObj[objName][propertyName] = this.value;
						} else {
							serializeObj[this.name] = this.value;
						}
					}
				});
				return serializeObj;
			}
	};
	exports('customerFrom', customerFrom);
})
