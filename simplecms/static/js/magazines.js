$(function() {
  var $body = $(document.body);
  var $posts = $('.posts');
  var $covers = $('.cover');
  // var $coverImgs = $('.cover > img');

  var redirect = function(target) {
    /* global WebViewJavascriptBridge */

    // 把相对路径搞成绝对路径，不然app不认识
    if (target.slice(0, 4) !== 'http') {
      target = location.protocol + '//' + location.host + target;
    }

    try {
      WebViewJavascriptBridge.callHandler('openInNewView', target);
    } catch (err) {
      location.href = target;
    }
  };

  var onBridgeReady = function(bridge) {
    bridge.init();
    bridge.callHandler('setScrollDecelerationRateNormal');
  };

  if ('WebViewJavascriptBridge' in window) {
    onBridgeReady(WebViewJavascriptBridge);
  } else {
    document.addEventListener('WebViewJavascriptBridgeReady', function() {
      onBridgeReady(WebViewJavascriptBridge);
    }, false);
  }

  $covers
    .css({
      height: $posts.width() * 380 / 640
    });

  // $coverImgs
  //   .on('load', function() {
  //     $(this).addClass('loaded');
  //   });

  // setTimeout(function() {
  //   $coverImgs.addClass('loaded');
  // }, 1000);

  $body
    .on('click', 'a', function(event) {
      var $this = $(this);
      var url = $this.attr('href');
      var origin_url = $this.data('origin-url');

      event.preventDefault();

      if (origin_url === url) {

        // 普通文章
        redirect(url);

      } else {

        // 菜单菜谱之类需要调用原生的
        $.ajax({
            type: 'head',
            url: origin_url,
            timeout: 500
          })
          .always(function() {
            redirect(url);
          });

      }
    });
});
