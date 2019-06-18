// layui.extend({
// 	requests: '{/}' + ctxStatic + '/layui/requests'
// });
//
// layui.use(['requests', 'form','layer','jquery'], function() {
//     let form = layui.form,
//         layer = parent.layer === undefined ? layui.layer : top.layer,
//         $ = layui.jquery,
//         requests = layui.requests;
//
//     $(".loginBody .seraph").click(function(){
//         layer.msg("这只是做个样式，至于功能，你见过哪个后台能这样登录的？还是老老实实的找管理员去注册吧",{
//             time:5000
//         });
//     });
//
//     //登录按钮
//     form.on("submit(login)", function(data) {
//     	requests.doLogin(data.field, $(this));
// 		// 阻止form表单submit
// 		return false;
//     });
//
//     //表单输入效果
//     $(".loginBody .input-item").click(function(e){
//         e.stopPropagation();
//         $(this).addClass("layui-input-focus").find(".layui-input").focus();
//     });
//
//     $(".loginBody .layui-form-item .layui-input").focus(function(){
//         $(this).parent().addClass("layui-input-focus");
//     });
//
//     $(".loginBody .layui-form-item .layui-input").blur(function(){
//         $(this).parent().removeClass("layui-input-focus");
//         if($(this).val() !== ''){
//             $(this).parent().addClass("layui-input-active");
//         }else{
//             $(this).parent().removeClass("layui-input-active");
//         }
//     });
// });



layui.extend({
	requests: '{/}' + ctxStatic + 'layui/requests'
});

layui.use(['requests', 'form','layer','jquery'], function() {
    let form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery,
        requests = layui.requests;

    $(".login-background .social-media-section").click(function(){
        layer.msg("这只是做个样式，至于功能，你见过哪个后台能这样登录的？还是老老实实的找管理员去注册吧",{
            time:5000
        });
    });

    //自定义验证规则
    form.verify({
        loginName: function (value) {
            if (value.length < 1) {
                return '请输入账号';
            }
        },
        password: function (value) {
            if (value.length < 1) {
                return '请输入密码';
            }
        }
    });

    //提交
    form.on('submit(user-login-submit)', function (data) {
        requests.doLogin(data.field, $(this));
        return false;
    });

    $(window).resize(function () {
        try {
            //解决移动端输入法弹出收回提示位置错误问题
            layui.layer.closeAll('tips'); //关闭所有的tips层
        } catch (e) { }
    });
});

