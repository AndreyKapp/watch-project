$('.header__content-photo__sliders').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.header__content-number__sliders'
  });
document.querySelector(".burger").addEventListener('click',function(){
    this.classList.toggle('active');
    document.querySelector('nav').classList.toggle('open');
})