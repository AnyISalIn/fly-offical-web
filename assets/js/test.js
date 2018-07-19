
$("a").on({
    mouseenter: function() {
    $(this).parent().find(".new").addClass("news");
    },
    mouseleave: function() {
    $(this).parent().find(".new").removeClass("news");
    },
    click: function() {
    // Handle click...
    }
    });
