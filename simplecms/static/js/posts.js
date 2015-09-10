$(function() {
  var isColorBlack = function(rgbcolor) {
    var distance = function(rgbArray) {
      return Math.pow(rgbArray[0], 2) + Math.pow(rgbArray[1], 2) + Math.pow(rgbArray[2], 2);
    };
    try {
      var rgb = rgbcolor.match(/\d+/g);
      return distance(rgb) <= distance([130, 130, 130]);
    } catch (err) {
      console.error(err);
      return true;
    }
  };

  var $view = $('.view');

  // 普通文章的格式化
  $view
    .not('.immutable')
    .find('*')
    .each(function(index, el) {
      var $el = $(el);
      var color = $el.css('color');
      var align = $el.css('text-align');
      var weight = $el.css('text-weight');
      var size = $el.css('font-size');

      var hasText = $.trim($el.text()) !== '';
      var hasImg = $el.find('img').size() > 0;
      var inLink = $el.parent().is('a');
      var isImg = $el.is('img');
      var isBold = weight === 'bold';
      var isMiniText = !isImg && size === '12px';
      var isBlack = isColorBlack(color);

      var hasColor = color && !isBlack && !isLink;

      var isLink = $el.is('a');
      var isCenter = align === 'center';
      var isRight = align === 'right';

      // 移除所有没有字的空标签
      if (!hasText && !hasImg && !isImg) {
        $el.remove();
        return true;
      }

      if (isMiniText && $el.closest('p').find('img').size() === 0) {
        $el.closest('p').addClass('top-25')
      }

      $el
        .removeAttr('name')
        .removeAttr('class')
        .removeAttr('data-w')
        .removeAttr('data-ratio')
        .removeAttr('data-type')
        .removeAttr('data-s')
        .removeAttr('color')
        .addClass(hasImg ? 'full-width' : '')
        .addClass(isCenter ? 'center' : '')
        .addClass(isRight ? 'right' : '')
        .addClass(isBold ? 'bold' : '')
        .addClass(hasColor ? 'bold' : '')
        .addClass(isMiniText ? 'em' : '')
        .addClass(isLink || isImg && !inLink ? 'img' : '')
        .removeAttr('style');
    });

  // 源码类文章的处理
  if ($view.is('.immutable')) {
    $(window)
      .on('load', function() {

        $('img[usemap]').each(function(i, img) {
          var $img = $(img),
            container = $img.parent(),
            wrap = container.parent(),
            currentWidth = wrap.width();

          container.css({
            'max-width': ''
          });

          if (!$img.data('height')) {
            container.css('overflow', '');
            $img.data('width', $img.width());
            $img.data('height', $img.height());
          }

          var nativeWidth = Number($img.data('width')),
            nativeHeight = Number($img.data('height'));
          var ratio = currentWidth / nativeWidth;
          var targetHeight = nativeHeight * ratio;

          container.css({
            '-webkit-transform-origin': '0px 0px 0px',
            'transform-origin': '0px 0px 0px',
            '-webkit-transform': 'scale(' + ratio + ')',
            'transform': 'scale(' + ratio + ')',
            'height': targetHeight + 'px',
            'line-height': 0
          });
        });

      });

    $view
      .on('click', 'map area', function(e) {
        if ('WebViewJavascriptBridge' in window) {
          e.preventDefault();
          WebViewJavascriptBridge.callHandler('openInNewView', $(this).attr('href'));
        }
      });
  }
});
