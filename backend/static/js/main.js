$(document).ready(function () {
  let $currentNumInfo = $(".current__slide-number");
  let $totalNumInfo = $(".total__slide-number");
  let $slickElement = $(".header__content-photo__sliders");

  $slickElement.on(
    "init reInit afterChange",
    function (event, slick, currentSlide, nextSlide) {
      //currentSlide is undefined on init -- set it to 0 in this case (currentSlide is 0 based)
      let i = (currentSlide ? currentSlide : 0) + 1;
      $currentNumInfo.text(i);
      $totalNumInfo.text(slick.slideCount);
    }
  );

  // $slickElement.slick({
  //   autoplay: true,
  //   dots: true,
  // });
  $slickElement.slick({
    arrows: true,
    infinite: false,
    prevArrow: $(".slider__controls .slider__prev"),
    //   '<button type="button" class="slick-prev"><img src="images/chevron-left.png" alt=""></button>',
    nextArrow: $(".slider__controls .slider__next"),
    //   '<button type="button" class="slick-next"><img src="images/chevron-left.png" alt=""></button>',
  });
});
