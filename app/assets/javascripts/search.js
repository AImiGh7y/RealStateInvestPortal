$(function() {
  $("#search").autocomplete({
    source: $("#search").data("source"),
    minLength: 1,
    classes: {
      "ui-autocomplete": "custom-autocomplete",
      "ui-menu-item": "custom-menu-item",
      "ui-state-focus": "custom-state-focus"
    },
    select: function(event, ui) {
      if (ui.item.value === $(event.target).val()) {
        return false;
      }
      $(event.target).val(ui.item.value);
    }
  });
});
