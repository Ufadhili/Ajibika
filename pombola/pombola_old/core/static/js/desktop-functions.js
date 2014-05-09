//generic re-usable hide or show with class states
//todo: add states to trigger elem if provided
function hideShow(elem, trig) {
  elem.toggleClass(function() {
    if ($(this).is('.open')) {
      $(this).hide().removeClass('open');
      trig.removeClass('active');
      return 'closed';
    } else {
      $(this).show().removeClass('closed');
      trig.addClass('active');
      return 'open';
    }
  });
}


$(function(){
  /*
   * auto complete
   */
    $('input.search-autocomplete-name')
    .each(function(){
      var element = $(this);
      var source = element.data('source') || "/search/autocomplete/";
      element.autocomplete({
          source: source,
          minLength: 2,
          html: true,
          select: function(event, ui) {
              if (ui.item) return window.location = ui.item.url;
          }
      });
    });
    
    
    // hide/show home intro
    $('.home-read-more').on('click', function(e){
      e.preventDefault();
      hideShow($('#home-intro span.details'), $(this));
      if($('.home-read-more.active').length !== 0){
        $(this).text('less');
      }else{
        $(this).text('more');
      }
    });
    
    // auto-advance cycles through featured MPs; it also immediately replaces the
    // featured MP in the page (since we assume that has been frozen by caching)
    var auto_advance_enabled = false;
    var auto_advance_delay = 12000; // milliseconds
    var auto_advance_timeout = false;
        
    function transitionDiv(height) {
      return '<div class="featured-person featured-person-loading" style="height:'
        + $('#home-featured-person').height() + 'px"><p>loading...</p></div>';      
    }
    
    // important to delegate this (with on()) because the contents change each auto-advance
    $('#home-featured-person').on("click", '.feature-nav > a',
        function(e, is_auto_advancing){
          e.preventDefault();
          if (! is_auto_advancing) { // user clicked
            auto_advance_enabled = false;
            if (auto_advance_timeout) {
              clearTimeout(auto_advance_timeout);
            }
          }
          var m = $(this).attr('href').match(/(before|after)=([-\w]+)$/);
          if (m.length==3) { // wee sanity check: found direction [1] and slug [2]
            // fix the container height to stop content below jumping up when contents fadeOut
            $('#home-featured-person').css("height", $('#home-featured-person').height() + "px");
            $('.featured-person', '#home-featured-person').fadeOut('fast',
              function(){
                 $('#home-featured-person').html(transitionDiv())
                    .load(
                      "person/featured/" + m[1] + '/' + m[2],
                      function() {
                        $('#home-featured-person').css("height","auto");
                      }
                    );
              })
          }
        }
    );
    
    if (auto_advance_enabled) {
      $('#home-featured-person').html(transitionDiv()).load(
          'person/featured/' + Math.floor(Math.random()*100) // some random index of featured person
      );
      function auto_advance(){
        if (auto_advance_enabled){
          $('a.feature-next', '#home-featured-person').trigger("click", true);
          auto_advance_timeout = window.setTimeout(auto_advance, auto_advance_delay);
        }
      }
      auto_advance_timeout = window.setTimeout(auto_advance, auto_advance_delay);
    }
    
    /*
     * enable dialog based feedback links
     */
      $('a.feedback_link')
        .on(
            'click',
            function(event) {
                // Note - we could bail out here if the window is too small, as
                // we'd be on a mobile and it might be better just to send them to
                // the feedback page. Not done as this js should only be loaded on
                // a desktop.
    
                // don't follow the link to the feedback page.
                event.preventDefault();
    
                // create a div to use in the dialog
                var dialog_div = $('<div>Loading...</div>');
    
                // Load the initial content for the dialog
                dialog_div.load( event.target.href + ' #ajax_dialog_subcontent' );
    
                // Form subission should be done using ajax, and only the ajax_dialog_subcontent should be shown.
                var handle_form_submission = function( form_submit_event ) {
                    form_submit_event.preventDefault();
                    var form = $(form_submit_event.target);
                    form.ajaxSubmit({
                        success: function( responseText ) {
                            dialog_div.html( $(responseText).find('#ajax_dialog_subcontent') );
                        }
                    });
                };
                
                // catch all form submissions and do them using ajax
                dialog_div.on( 'submit', 'form', handle_form_submission );
            
                // Show the dialog
                dialog_div.dialog({
                  modal: true,
                  minHeight: 320,
                  width: 500,
                  title: 'Leave Feedback'
                });
    
            }
        );

  // /*
  //  * Comments: hover and show tools
  //  */
  // $('.comments li').hover(function() {
  //   $(this).addClass('hovered');
  // },
  // function() {
  //   $(this).removeClass('hovered');
  // });

  /*
   * Main nav hover
   */
  $('#main-menu ul > li')
    .on( 'mouseover', function () {
        var $menu_heading = $(this);

        if($menu_heading.children('ul').length === 1){

            // close other menus that might be open
            $menu_heading.siblings('.active').trigger('mouseout');

            $menu_heading.addClass('active');
        }
    })
    .on( 'mouseout', function () {
        $(this).removeClass('active');
    })
    .on ('touchstart', function ( e ) {
        // If we are not active then this is probably a tap on a tablet. Trigger a
        // mouseover event instead.
        var $menu_heading = $(this);

        if ( $menu_heading.children('ul').length === 1 && ! $menu_heading.hasClass('active') ) {
            e.preventDefault();                 // don't follow through with a click
            $menu_heading.trigger('mouseover'); // show the menu
            // TODO - some how cancel the menu - atm it'll stay up now until you navigate away from page or click on another menu heading
        }
    });
  
  /* carry search terms across when switching between search pages */
  $("#search-hansard-instead").click(function(e){
    e.preventDefault();
    location.href="/search/hansard?q=" + escape($('#core-search,#id_q,#loc').first().val());
  });
  $("#search-core-instead").click(function(e){
    e.preventDefault();
    location.href="/search?q=" + escape($('#id_q,#loc').first().val());
  });
});
