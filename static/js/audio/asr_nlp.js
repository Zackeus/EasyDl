layui.extend({
    context: '{/}' + ctxStatic + 'layui/lay/custom/context/context'
});

layui.use(['form','layer','jquery', 'context'],function() {
	var form = layui.form,
        layer = layui.layer,
		$ = layui.$,
        context = layui.context;

		// Settings
	var audio, timeout, isPlaying;

	var volume = localStorage.volume || 0.5;

	// 音量设置
	var setVolume = function(value){
		audio.volume = localStorage.volume = value;
		$('.volume .pace').css('width', value * 100 + '%');
		$('.volume .slider a').css('left', value * 100 + '%');
	};

	// 预加载
	var beforeLoad = function(){
		var endVal = this.seekable && this.seekable.length ? this.seekable.end(0) : 0;
		$('.progress .loaded').css('width', (100 / (this.duration || 1) * endVal) +'%');
	};

	// 播放结束
	var ended = function() {
		pause();
		audio.currentTime = 0;
	};

	// 音量滑动
	$('.volume .slider').slider({max: 1, min: 0, step: 0.01, value: volume, slide: function(event, ui){
		setVolume(ui.value);
		$(this).addClass('enable');
		$('.mute').removeClass('enable');
	}, stop: function(){
		$(this).removeClass('enable');
	}}).children('.pace').css('width', volume * 100 + '%');

	// 静音
	$('.mute').click(function(){
		if ($(this).hasClass('enable')){
			setVolume($(this).data('volume'));
			$(this).removeClass('enable');
		} else {
			$(this).data('volume', audio.volume).addClass('enable');
			setVolume(0);
		}
	});

	// 重播
	$('.repeat').on('click', function() {
		console.log('重播');
	});

	// 设置滑动条滑动值
	var setProgress = function(value) {
		var currentSec = parseInt(value % 60) < 10 ? '0' + parseInt(value % 60) : parseInt(value % 60),
			ratio = value / audio.duration * 100;

		$('.timer').html(parseInt(value/60) + ':' + currentSec);
		$('.progress .pace').css('width', ratio + '%');
		$('.progress .slider a').css('left', ratio + '%');

		updateAsrData(value * 1000);
	};

	// 更新滑动条
	var updateProgress = function() {
		setProgress(audio.currentTime);
	};

	// 更新音频转写
	var updateAsrData = function(ms) {
		$('#asrDatas li').each(function (i, e) {
			if ($(e).data('bg') > ms) {
				if ($('#asrDatas li').eq(i === 0 ? 0 : i - 1).data('bg') < ms) {
					// 确认当前转写位置
					var mainContainer = $('#asrDatasDiv'),
					  scrollToContainer = $('#asrDatas li').eq(i === 0 ? 0 : i - 1);

					// 非动画效果
					mainContainer.scrollTop(
						scrollToContainer.offset().top - mainContainer.offset().top + mainContainer.scrollTop() - 250
				  	);
				}

				// for (index = i; index <= $('#asrDatas').children('li').length; index++) {
				// 	$('#asrDatas li').eq(index).css('visibility', 'hidden');
				// }
				// return false;
				$(e)[0].style.visibility='hidden';

				// 控制标签栏隐藏
				let $font = $(e).children('.layim-chat-text').children('font');
				if (!$.isEmptyObject($font.attr("id"))) {
					$font.each(function (ii, ee) {
						$('.' + $(ee).attr("id")).next().css('display', 'none');
					});
				}
			} else {
				$(e)[0].style.visibility='visible';

				// 控制标签栏显示
				let $font = $(e).children('.layim-chat-text').children('font');
				if (!$.isEmptyObject($font.attr("id"))) {
					$font.each(function (ii, ee) {
						$('.' + $(ee).attr("id")).next().css('display', 'inline-block');
					});
				}
			}
        });
	};

	// 滑动快进
	$('.progress .slider').slider({step: 0.1, slide: function(event, ui){
		$(this).addClass('enable');
		setProgress(audio.duration * ui.value / 100);
		clearInterval(timeout);
	}, stop: function(event, ui){
		audio.currentTime = audio.duration * ui.value / 100;
		$(this).removeClass('enable');
		timeout = setInterval(updateProgress, 500);
	}});

	// 播放
	var play = function() {
		audio.play();
		$('.playback').addClass('playing');
		timeout = setInterval(updateProgress, 500);
		isPlaying = true;
	};

	// 暂停
	var pause = function(){
		audio.pause();
		$('.playback').removeClass('playing');
		clearInterval(updateProgress);
		isPlaying = false;
	};

	// 播放暂停
	$('.playback').on('click', function(){
		if ($(this).hasClass('playing')){
			pause();
		} else {
			play();
		}
	});

	// 上一曲
	$('.rewind').on('click', function(){
		console.log('上一曲');
	});

	// 下一曲
	$('.fastforward').on('click', function(){
		console.log('下一曲');
	});

	// 加载音频
	var loadMusic = function() {
		audio = $('audio')[0];
		audio.volume = $('.mute').hasClass('enable') ? 0 : volume;
		audio.addEventListener('progress', beforeLoad, false);
		audio.addEventListener('durationchange', beforeLoad, false);
		// audio.addEventListener('canplay', afterLoad, false);
		audio.addEventListener('ended', ended, false);
	};

	loadMusic();

	// 初始化 layui
	layer.tips('', '#asrDatas', {tips: [1, '#000'], time: 1});

    // 监听语义标签复选框
    form.on('checkbox(lexer)',function(data) {
        if (data.elem.checked) {
            // 选中
            $("font#" + data.value).addClass("lexer_font_show").removeClass("lexer_font__hide");
            // $("font." + data.value).addClass("lexer_font_show").removeClass("lexer_font__hide");
        } else {
            // 关闭
            $("font#" + data.value).addClass("lexer_font__hide").removeClass("lexer_font_show");
            // $("font." + data.value).addClass("lexer_font__hide").removeClass("lexer_font_show");
        }
    });

    // 监听鼠标悬停
    $(".layim-chat-text font").mouseover(function() {
        layer.tips(
            $(this).data("ne-title"),
            this,
            {tips: [1, '#000'], time: 0},
        );
    }).mouseout(function() {
        layer.closeAll('tips');
    });

    // 右键菜单初始化
    context.init({preventDoubleContext: false});
    context.settings({compress: true});

    context.attach('.layui-form-checkbox', [
        {header: '信息栏'},
        {id: 'speaker', text: '发音人', href: '#'},
        {id: 'bg', text: '起始时间', href: '#'},
        {id: 'ed', text: '结束时间', href: '#'},
        {id: 'onebest', text: '原始语句', href: '#'},
        {text: '回放', action: function(o, e) {
			e.preventDefault();
			pause();
			let uiVal = $('#' + $(o).prev().val()).data('bg') / 1000 / audio.duration;
			setProgress(audio.duration * uiVal);
		    audio.currentTime = audio.duration * uiVal;
		    play();
		}},
    ], function (obj) {
        let $font = $('#' + $(obj).prev().val());
        $('#speaker').children().text('发音人：' + $font.data('speaker'));
        $('#bg').children().text('起始时间：' + $font.data('bg'));
        $('#ed').children().text('结束时间：' + $font.data('ed'));
        $('#onebest').children().text('原始语句：' + $font.data('onebest'));
    });
});
