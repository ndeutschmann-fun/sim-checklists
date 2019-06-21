$(window).scroll(function() {
  if ($(document).scrollTop() > 50) {
    $('.navbar').addClass('shrink');
    $('.navbar-brand').addClass('shrink');
  } else {
    $('.navbar').removeClass('shrink');
    $('.navbar-brand').removeClass('shrink');
  }
});
