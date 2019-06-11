layui.use(['form','layer','jquery'], function() {
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer,
        element = layui.element;
        $ = layui.jquery;

        $("body").on("click",".site-doc-icon li",function() {
        	var iconCode = $(this).children('div.code').text();
    		// 给父页面传值
    		var $$ = parent.layui.jquery;
    		$$('#icon').val(iconCode);
    		$$('#iconCode').val(iconCode);
    		$$("#iconStyle").attr('class', 'layui-icon ' + iconCode);
    		parent.layer.close(parent.layer.getFrameIndex(window.name));
        })
        
//    $.get(ctxStatic + '/layui-2.2.5/css/icon/icon.css',function(data) {
//    	console.log(data);
//        var iconHtml = '';
//        for(var i=1;i<data.split(".layui-icon-").length;i++){
//            iconHtml += "<li class='layui-col-xs4 layui-col-sm3 layui-col-md2 layui-col-lg1'>"+
//                            "<i class='layui-icon seraph layui-icon-" + data.split(".layui-icon-")[i].split(":before")[0] + "'></i>" +
//                            "layui-icon-" + data.split('.layui-icon-')[i].split(':before')[0] +
//                        "</li>";
//        }
//        $(".icons").html(iconHtml);
//        $(".iconsLength").text(data.split(".layui-icon-").length-1);
//    })

});
