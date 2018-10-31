$(function () {
    var $slides = $('.slide li');
    var len = $slides.length;
    var nowli = 0;
    var prevli = 0;
    var $prev = $('.prev');
    var $next = $('.next');
    var timer = null;
    $slides.not(':first').css({'opacity': 0});

    $slides.each(function (index, el) {
        var $li = $('<li>');
        if (index == 0) {
            $li.addClass('active');
        }
        $li.appendTo($('.points'));
    });

    $points = $('.points li');
    timer = setInterval(autoplay, 4000);

    $('.pos_center_con').mouseenter(function () {
        clearInterval(timer);
    });

    $('.pos_center_con').mouseleave(function () {
        timer = setInterval(autoplay, 4000);
    });

    function autoplay() {
        nowli++;
        move();
        $points.eq(nowli).addClass('active').siblings().removeClass('active');
    };

    $points.click(function () {
        nowli = $(this).index();
        $(this).addClass('active').siblings().removeClass('active');
        move();
    });
    $prev.click(function () {
        nowli--;
        move();
        $points.eq(nowli).addClass('active').siblings().removeClass('active');
    });
    $next.click(function () {
        nowli++;
        move();
        $points.eq(nowli).addClass('active').siblings().removeClass('active');

    });

    function move() {
        if (nowli == prevli) {
            return;
        }

        if (nowli < 0) {
            nowli = len - 1;
            prevli = 0
            $slides.eq(nowli).animate({'opacity': 1}, 800);
            $slides.eq(prevli).animate({'opacity': 0}, 800);
            prevli = nowli;
            return;
        }

        if (nowli > len - 1) {
            nowli = 0;
            prevli = len - 1;
            $slides.eq(nowli).animate({'opacity': 1}, 800);
            $slides.eq(prevli).animate({'opacity': 0}, 800);
            prevli = nowli;
            return;
        }

        if (prevli < nowli) {
            $slides.eq(nowli).animate({'opacity': 1}, 800);
            $slides.eq(prevli).animate({'opacity': 0}, 800);
            prevli = nowli;
        }
        else {
            $slides.eq(nowli).animate({'opacity': 1}, 800);
            $slides.eq(prevli).animate({'opacity': 0}, 800);
            prevli = nowli;
        }
    }
})
//猜你喜欢
$(document).ready(function () {
    $("#guess1").addClass('add');
    $("#guess1").hover(function () {
        $("#guess1").addClass('add');
        $("#guess2").removeClass('add');
        $("#guess3").removeClass('add');
    });
});
$("#guess2").hover(function () {
    $("#guess2").addClass('add');
    $("#guess1").removeClass('add');
    $("#guess3").removeClass('add');
});

$("#guess3").hover(function () {
    $("#guess3").addClass('add');
    $("#guess2").removeClass('add');
    $("#guess1").removeClass('add');
});

//我的订单
$("#order_show").hide();
$("#my_order").hover(function () {
    $("#order_show").show();
}, function () {
    $("#order_show").hide();
})
// 鼠标移动到list的div上的时候list div不会被隐藏
$("#order_show").hover(function () {
    $("#order_show").show();
}, function () {
    $("#order_show").hide();
})

//上传头像
// document.getElementById('file').onchange = function () {
//     var imgFile = this.files[0];
//     var fr = new FileReader();
//     fr.onload = function () {
//         document.getElementById('image').getElementsByTagName('img')[0].src = fr.result;
//     };
//     fr.readAsDataURL(imgFile);
// };
