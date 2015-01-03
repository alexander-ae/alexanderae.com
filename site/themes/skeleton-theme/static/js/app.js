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

    /* Google plus */
    window.___gcfg = {lang: 'es-419'};
    (function() {
        var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
        po.src = 'https://apis.google.com/js/plusone.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
    })();
});

