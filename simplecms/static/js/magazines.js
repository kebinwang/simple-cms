$(function() {
  var $body = $(document.body);
  var $covers = $('.cover > img');

  $covers
    .on('load', function() {
      $(this).addClass('loaded');
    });

  setTimeout(function() {
    $covers.addClass('loaded');
  }, 1000);

  $body
    .on('click', 'a', function(event) {
      var $this = $(this);
      var url = $this.attr('href');
      var origin_url = $this.data('origin-url');

      if (origin_url !== url) {
        event.preventDefault();

        $body.animate({
          opacity: '.5'
        }, 'fast');

        $.ajax({
            type: 'head',
            url: origin_url,
            timeout: 500
          })
          .always(function() {
            location.href = url
            $body.removeAttr('style');
          });
      }
    })
});
