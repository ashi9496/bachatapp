$(document).ready(function(){

    $nav = $('.nav');
    $togglecollapse = $('.toggle-collapse')

    /**click event on toggle menu */
    $togglecollapse.click(function(){
        $nav.toggleClass('collapse')
    })
    //   owl carousel
    $('.owl-carousel').owlCarousel();

});