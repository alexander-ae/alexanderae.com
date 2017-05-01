$(document).ready(function() {
    /* addClass 'active' */
    $('a').each(function(){
        if ($(this).attr('href') === window.location.pathname ) {
            $(this).addClass('active');
        }
    })

    if ( window.location.pathname === '/' ) {
        $('.first-page').addClass('active');
    }

    if ($('body').hasClass('home') || $('body').hasClass('etiquetas')) {
        $('a.footnote-ref').parent().remove();
    }
});
