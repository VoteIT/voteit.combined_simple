$('.yes_no_abstain_widget .enabled.votecontrol').live('click', function(event) {
    //Note: Don't block event here!
    $(event.target).siblings().removeClass('selected');
    $(event.target).addClass('selected');
})
