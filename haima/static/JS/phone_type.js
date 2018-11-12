var addressInit = function (_cmbBrand, _cmbModel, _cmbConfiguration, defaultBrand, defaultModel, defaultConfiguration) {
    var cmbBrand = document.getElementById(_cmbBrand);
    var cmbModel = document.getElementById(_cmbModel);
    var cmbConfiguration = document.getElementById(_cmbConfiguration);

    // var cmbVolume = document.getElementById(_cmbVolume);

    function cmbSelect(cmb, str) {
        for (var i = 0; i < cmb.options.length; i++) {
            if (cmb.options[i].value == str) {
                cmb.selectedIndex = i;
                return;
            }
        }
    }

    function cmbAddOption(cmb, str, obj) {
        var option = document.createElement("OPTION");
        cmb.options.add(option);
        option.innerText = str;
        option.value = str;
        option.obj = obj;
    }

    function changeModel() {
        cmbConfiguration.options.length = 0;
        if (cmbModel.selectedIndex == -1) return;
        var item = cmbModel.options[cmbModel.selectedIndex].obj;
        for (var i = 0; i < item.configurationList.length; i++) {
            cmbAddOption(cmbConfiguration, item.configurationList[i], null);
        }
        cmbSelect(cmbConfiguration, defaultConfiguration);
    }

    function changeBrand() {
        cmbModel.options.length = 0;
        cmbModel.onchange = null;
        if (cmbBrand.selectedIndex == -1) return;
        var item = cmbBrand.options[cmbBrand.selectedIndex].obj;
        for (var i = 0; i < item.modelList.length; i++) {
            cmbAddOption(cmbModel, item.modelList[i].name, item.modelList[i]);
        }
        cmbSelect(cmbModel, defaultModel);
        changeModel();
        cmbModel.onchange = changeModel;
    }

    for (var i = 0; i < brandList.length; i++) {
        cmbAddOption(cmbBrand, brandList[i].name, brandList[i]);
    }
    cmbSelect(cmbBrand, defaultBrand);
    changeBrand();
    cmbBrand.onchange = changeBrand;
};

var brandList = [
    {
        name: '请选择手机品牌', modelList: [
            {name: '请选择手机型号', configurationList: ['请选择配置']}
        ]
    },
    {
        name: '苹果', modelList: [
            {name: 'XS MAX', configurationList: ['4G+64G', '4G+256G', '4G+512G']},
            {name: 'XS', configurationList: ['4G+64G', '4G+256G', '4G+512G']},
            {name: 'X', configurationList: ['3G+64G', '3G+256G']},
            {name: '8plus', configurationList: ['3G+64G', '3G+256G']},
            {name: '8', configurationList: ['3G+64G', '3G+256G']},
            {name: '7plus', configurationList: ['3G+32G', '3G+128G', '3G+256G']},
            {name: '7', configurationList: ['3G+32G', '3G+128G', '3G+256G']},
            {name: '6s plus', configurationList: ['2G+16G', '2G+32G', '2G+64G', '2G+128G']},
            {name: '6s', configurationList: ['2G+16G', '2G+32G', '2G+64G', '2G+128G']},
            {name: '6plus', configurationList: ['2G+16G', '2G+32G', '2G+64G', '2G+128G']},
            {name: '6', configurationList: ['2G+16G', '2G+32G', '2G+64G']},
            {name: 'SE', configurationList: ['2G+16G', '2G+32G', '2G+64G']},
            {name: '5s', configurationList: ['1G+16G', '1G+64G']},
            {name: '5', configurationList: ['1G+16G', '1G+32G', '1G+64G']},
        ]
    },
    {
        name: '华为', modelList: [
            {name: 'Mate20', configurationList: ['6G+64G', '6G+128G']},
            {name: 'Mate20 pro', configurationList: ['6G+128G', '6G+256G', '8G+256G']},
            {name: 'Mate20x', configurationList: ['6G+128G', '8G+256G']},
            {name: 'P20 pro', configurationList: ['4G+64G', '6G+64G', '6G+128G', '6G+256G', '8G+256G']},
            {name: 'P20', configurationList: ['6G+64G', '4G+128G', '6G+128G']},
            {name: 'Mate10 pro', configurationList: ['4G+64G', '6G+64G', '6G+128G']},
            {name: 'Mate10', configurationList: ['4G+32G', '4G+64G', '6G+128G']},
            {name: 'Nova3', configurationList: ['4G+128G', '6G+64G', '6G+128G']},
            {name: '麦芒7', configurationList: ['6G+64G']},
            {name: '麦芒6', configurationList: ['4G+64G']},
            {name: 'Nova3e', configurationList: ['4G+64G', '4G+128G']},
            {name: 'P9', configurationList: ['3G+32G', '3G+64G']},
            {name: 'P9 plus', configurationList: ['4G+64G', '4G+128G']},
        ]
    },
    {
        name: '荣耀', modelList: [
            {name: '10', configurationList: ['4G+64G', '6G+64G', '6G+128G', '8G+128G']},
            {name: 'Note10', configurationList: ['6G+64G', '6G+128G', '8G+128G']},
            {name: 'V10', configurationList: ['4G+64G', '6G+64G', '6G+128G', '6G+256G']},
            {name: '9', configurationList: ['4G+64G', '6G+64G', '6G+128G']},
            {name: '8', configurationList: ['3G+32G', '4G+32G', '4G+64G']},
            {name: '7', configurationList: ['1G+4G', '3G+16G', '3G+32G', '3G+64G']},
            {name: 'play', configurationList: ['4G+64G', '6G+64G', '6G+128G']},
            {name: 'V9', configurationList: ['4G+64G', '6G+64G', '6G+128G']},
            {name: '畅玩7x', configurationList: ['4G+32G', '4G+64G', '4G+128G']},
            {name: '畅玩6x', configurationList: ['3G+32G', '4G+32G', '4G+64G']},
        ]
    },
    {
        name: '小米', modelList: [
            {name: '8', configurationList: ['6G+64G', '6G+128G', '6G+256G', '8G+128G']},
            {name: 'Mix2s', configurationList: ['4G+64G', '6G+64G', '6G+128G', '8G+256G']},
            {name: 'Mix3', configurationList: ['6G+128G', '8G+128G', '8G+256G']},
            {name: '6', configurationList: ['4G+64G', '6G+64G', '6G+128G']},
            {name: 'Mix2', configurationList: ['6G+64G', '4G+128G', '6G+128G']},
            {name: 'Mix2s', configurationList: ['6G+64G', '6G+128G', '6G+256G']},
            {name: '8se', configurationList: ['4G+64G', '6G+64G', '6G+128G', '8G+256G']},
            {name: '6x', configurationList: ['4G+32G', '4G+64G', '6G+64G', '6G+128G']},
            {name: 'Max3', configurationList: ['4G+64G', '6G+128G']},
            {name: 'Max2', configurationList: ['4G+32G', '4G+64G', '4G+128G']},
            {name: 'Mix', configurationList: ['4G+128G', '6G+256G']},
            {name: '5', configurationList: ['3G+32G', '3G+64G', '4G+128G']},
            {name: '5x', configurationList: ['4G+32G', '4G+64G']},
            {name: '5s', configurationList: ['4G+32G', '4G+64G', '4G+128G']},
            {name: '4', configurationList: ['2G+16G', '2G+32G', '3G+16G', '3G+32G', '3G+64G']},
            {name: 'Max', configurationList: ['2G+16G', '3G+32G', '3G+64G', '4G+128G']},
        ]
    },
    {
        name: '红米', modelList: [
            {name: 'Note4x', configurationList: ['4G+64G', '4G+16G', '3G+32G', '3G+16G','2G+32G']},
            {name: '4x', configurationList: ['4G+64G', '3G+32G', '2G+16G']},
            {name: 'Note3', configurationList: ['3G+32G', '2G+16G']},
            {name: 'Note5', configurationList: ['3G+32G', '4G+64G','6G+64G','6G+128G']},
            {name: 'Note4', configurationList: ['2G+16G', '3G+32G', '4G+64G']},
            {name: '5plus', configurationList: ['3G+32G', '4G+64G']},
            {name: '4a', configurationList: ['2G+16G']},
            {name: '6pro', configurationList: ['3G+32G', '4G+32G', '4G+64G']},
        ]
    },
    {
        name: 'OPPO', modelList: [
            {name: 'Findx', configurationList: ['8G+128G', '8G+256G']},
            {name: 'R17', configurationList: ['6G+128G', '8G+128G']},
            {name: 'R15', configurationList: ['4G+128G', '6G+128G']},
            {name: 'R11s', configurationList: ['4G+64G', '6G+128G']},
            {name: 'R11', configurationList: ['4G+64G', '6G+128G']},
            {name: 'R9s', configurationList: ['4G+64G']},
            {name: 'R9', configurationList: ['4G+64G']},
            {name: 'R9plus', configurationList: ['4G+64G', '4G+128G']},
            {name: 'R7', configurationList: ['3G+16G']},
            {name: 'R7s', configurationList: ['3G+32G', '4G+32G']},
            {name: 'A37', configurationList: ['2G+16G']},
            {name: 'A5', configurationList: ['3G+64G', '4G+32G', '4G+64G']},
            {name: 'A57', configurationList: ['4G+32G', '3G+32G']},
            {name: 'A33', configurationList: ['2G+16G']},
            {name: 'A59s', configurationList: ['4G+32G']},
            {name: 'A59', configurationList: ['3G+32G']},
            {name: 'A53', configurationList: ['2G+16G']},
        ]
    },
];


// 传select数据
$(function () {
    $("#assess_button").click(function () {
        brand = $("#cmbBrand").val();
        if (brand == '请选择手机品牌') {
            $(".error_mes1").show();
            return false
        }
        else {
            model = $("#cmbModel").val();
            configuration = $("#cmbConfiguration").val();
            color = $("#phone_color").val();
            GT = $("#GT").val();
            face = $("#face").val();
            maintain = $("#maintain").val();
            UT = $("#UT").val();
            $.post('/assess_ajax/', {
                'brand': brand,
                'model': model,
                'configuration': configuration,
                'color': color,
                'GT': GT,
                'face': face,
                'maintain': maintain,
                'UT': UT,
            }, function (data) {
                $("#assess_price").text(data.price);
                $("#price_hid").val(data.price);
            }, 'json')
        }
    })
});

$("#close_fix").click(function () {
    $("#price_res").hide();
});

$("#assess_button").click(function () {
    $("#price_res").show();
});

$("#assess_button").click(function () {
    $("#assess_price").text('正在估价请稍等...')
});