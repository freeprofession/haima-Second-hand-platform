// 展示商品图片

$(document).ready(function () {
    $('#up img').attr('src', $('#down img').eq(0).attr('src'));
    $('.zoom').css('background', 'url(' + $('#down img').eq(0).attr('src') + ') no-repeat')//打开即把第一张图地址给#up img
    $('#down img').eq(0).addClass("change_image");//打开即把第一个缩略图选中
    $('#down img').hover(function () {
        $('#down img').removeClass("change_image");//先清除所有选中
        $(this).addClass("change_image");//当前图片选中
        $('#up img').attr('src', $(this).attr('src'));//当前图片地址给#up img
        $('.zoom').css('background', 'url(' + $(this).attr('src') + ') no-repeat')
    });
});


// 商品信息 留言按钮
$(function () {
    var $tab_btn = $('.detail_tab li');
    var $tab_con = $('.tab_content');
    $tab_btn.click(function () {
        $(this).addClass('active').siblings().removeClass('active');
        $tab_con.eq($(this).index()).addClass('current').siblings().removeClass('current');
    })
})

// 限制留言字数
var checkLength = function (dom, maxLength) {
    var l = 0;
    for (var i = 0; i < dom.value.length; i++) {
        if (/[\u4e00-\u9fa5]/.test(dom.value[i])) {
            l += 2;
        } else {
            l++;
        }
        if (l > maxLength) {
            dom.value = dom.value.substr(0, i);
            break;
        }
    }
};

// 图片放大镜
(function ($) {
    $.fn.zoom = function () {
        var img = $(this).find("img");
        var span = $(this).find("span");
        var zoom = $(".zoom");
        //获取略缩图相对于窗口的位置
        var tLeft = $(img).offset().left;
        var tTop = $(img).offset().top;

        $(this).mousemove(function (e) {
            //获取鼠标坐标
            var mLeft = e.clientX;
            var mTop = e.clientY;

            //计算鼠标相对于图片区域的位置
            var l = mLeft - tLeft;
            var t = mTop - tTop;

            //鼠标移动时移动span
            $(span).css({
                "overflow": "hidden",
                "cursor": "move",
                "position": "fixed",
                "display": "block",
                "margin-left": (l + 80) + "px",
                "margin-top": (t + 100) + "px"
            });

            //计算偏移量
            var ll = (l / $(img).width()) * 200 + "%";
            var tt = (t / $(img).height()) * 300 + "%";

            //设置大图偏移
            $(zoom).css({
                "display": "block",
                "background-position": ll + " " + tt
            })
        });

        //解除绑定
        $(this).mouseout(function () {
            $(span).css("display", "none");
            $(zoom).css("display", "none");
        })
    }
})(jQuery);
$(".up").zoom();
