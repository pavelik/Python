const nickname = document.getElementById('nickname');

$(document).ready(function () {
    $("html, body").scrollTop($(document).height());
});

$("a[href='#top']").click(function () {
    $("html, body").animate({
        scrollTop: 0
    }, "slow");
});
