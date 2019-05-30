(function($){
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

	// 已准备好开始播放
	// var afterLoad = function(){
	// 	if (autoplay === true) play();
	// };

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

					// 动画效果
					// mainContainer.animate({
					// 	scrollTop: scrollToContainer.offset().top - mainContainer.offset().top +
					// 		mainContainer.scrollTop() - 250
					// }, 1);//2秒滑动到指定位置
				}

				for (index = i; index <= $('#asrDatas').children('li').length; index++) {
					$('#asrDatas li').eq(index).css('visibility', 'hidden');
				}
				return false;
			} else {
				$(e)[0].style.visibility='visible';
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
})(jQuery);