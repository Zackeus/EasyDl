layui.extend({
	requests: '{/}' + ctxStatic + '/layui/requests'
});

layui.use(['requests', 'form'],function(){
    var form = layui.form,
        $ = layui.jquery,
        requests = layui.requests;
    
    form.on('submit(addDict)', function(data) {
    	requests.doAddDict(data.field, $(this));
    	return false;
    });
    
    $('#closeDict').click(function () {
    	parent.layer.close(parent.layer.getFrameIndex(window.name));
    });
});