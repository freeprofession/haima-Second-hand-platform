var index = 0;
var dex = new Array();
var fileArray = new Array();


function FFile(obj) {
    this.FileSet = {
        name: obj.name ? obj.name : null,								//唯一名,用来与其他文件区分
        fileInput: obj.fileInput ? obj.fileInput : null,				//html file控件
        upButton: obj.upButton ? obj.upButton : null,					//提交按钮
        pre: obj.pre ? obj.pre : null,									//预览地址
        url: obj.url ? obj.url : null,									//ajax地址
        fileFilter: obj.fileFilter ? obj.fileFilter : [],							                            //过滤后的文件数组
        filter: obj.filter ? obj.filter : function (files) {
            var arrFiles = [];
            for (var i = 0, file; i < files.length; i++) {
                file = files[i];
                var key;
                var observable;
                var subscription;
                var token;
                var putExtra = {
                    mimeType: ["image/png", "image/jpeg", "image/gif"] || null,
                };
                var config = {
                    region: qiniu.region.z0
                };
                var observer = {
                    next(res) {
                        console.log(res.total.percent);
                        var ajaxbg = $("#background,#progressBar");
                        ajaxbg.show();
                    },
                    error(err) {
                        console.log(err)

                    },
                    complete(res) {
                        var ajaxbg = $("#background,#progressBar");
                        ajaxbg.hide();
                        console.log(res)
                        fileArray[res['index']] = res['key']
                        console.log(fileArray[res['index']])
                    }
                }
                if (file.type.indexOf("image") == 0) {
                    arrFiles.push(file);
                    $.ajax({
                        url: "/gettokendata/",
                        data: {'index': index},
                        type: "POST",
                        async: false,
                        success: function (data) {//请求成功后调用的函数
                            token = data;
                            dex.push(index)
                            observable = qiniu.upload(file, key, token, putExtra, config)
                            subscription = observable.subscribe(observer) // 上传开始
                            index++;
                        },
                        error: function () {//请求失败后调用的函数
                            console.log(err);
                        }
                    });
                } else {
                    alert('文件"' + file.name + '"不是图片。');
                }
            }
            return arrFiles;
        },
    }
    this.init();
}

FFile.prototype = {
    //获取选择文件，file控件或拖放
    funGetFiles: function (e) {
        // 获取文件列表对象
        var files = e.target.files;
        //继续添加文件
        this.FileSet.fileFilter = this.FileSet.fileFilter.concat(this.FileSet.filter(files));
        this.funDealFiles();
        return this;
    },
    //选中文件的处理与回调
    funDealFiles: function () {
        for (var i = 0, file; file = this.FileSet.fileFilter[i]; i++) {
            //增加唯一索引值
            file.index = i;
        }
        //执行选择回调
        this.onSelect(this.FileSet.fileFilter);
        return this;
    },
    onSelect: function (files) {
        var html = '',
            self = this,
            i = 0;
        $(this.FileSet.pre).html();//清空预览地址
        var funAppendImage = function () {
            file = files[i];
            if (file) {
                var reader = new FileReader()
                reader.onload = function (e) { //生成的图片
                    html += '<div id="js-uploadList_' + self.FileSet.name + i + '" class="img-box">';
                    html += '<div class="img-border">';
                    html += '<span class="js-upload_delete icon-delete_fill red" data-index="' + i + '"></span>';
                    html += '<img src="' + e.target.result + '">';
                    html += '</div>';
                    html += '</div>';
                    i++;
                    funAppendImage();
                }
                reader.readAsDataURL(file);
            } else {
                $(self.FileSet.pre).html(html);
                if (html) {
                    //删除方法
                    $(".js-upload_delete").click(function () {
                        // var ajaxbg = $("#background,#progressBar");
                        // ajaxbg.show();
                        self.funDeleteFile(files[parseInt($(this).attr("data-index"))]);
                        dex.splice((parseInt($(this).attr("data-index"))), 1)
                        self.onSelect(self.FileSet.fileFilter);
                        return false;
                    });
                }
            }
        };
        funAppendImage();
    },
    //删除对应的文件
    funDeleteFile: function (fileDelete) {
        var arrFile = [];
        for (var i = 0, file; file = this.FileSet.fileFilter[i]; i++) {
            if (file != fileDelete) {
                arrFile.push(file);
            } else {
                this.onDelete(fileDelete);
            }
        }
        this.FileSet.fileFilter = arrFile;
        return this;
    },

    onDelete: function (file) {//清除图片
        let self = this;
        $("#js-uploadList_" + self.FileSet.name + file.index).empty();
    },
    //文件上传
    funUploadFile: function () {
        var postArray = [];
        // var ajaxbg = $("#background,#progressBar");
        // ajaxbg.show();
        var form = document.getElementById('pub_goods');
        for (var i = 0; i < dex.length; i++) {
            j = dex[i]
            console.log(fileArray[j])
            postArray.push(fileArray[j])
        }
        var filelist = document.getElementById('filelist');
        console.log(JSON.stringify(postArray))
        filelist.value = JSON.stringify(postArray)

        // console.log(dex);
        // console.log(fileArray)
        // console.log(postArray)
        form.submit();

        // $.ajax({
        //     type: "POST",
        //     url: '/pub_success/',
        //     data: $('#pub_goods').serialize(),
        //     success: function (data) {
        //     },
        //     error: function (data) {
        //     }
        // });
        // var self = this;
        // for (var i = 0, file; file = this.FileSet.fileFilter[i]; i++) {
        //     (function (file) {
        //         var formData = new FormData();
        //         formData.append(self.FileSet.name, file);
        //         $.ajax({
        //             url: self.FileSet.url,
        //             type: 'post',
        //             data: formData,
        //             contentType: false,
        //             processData: false,
        //             success: function (data) {
        //                 self.FileSet.onSuccess(data);
        //                 self.funDeleteFile(file);
        //             },
        //             error: function (data) {
        //                 self.FileSet.onFailure(data);
        //             }
        //         })
        //         if (!self.FileSet.fileFilter.length) {
        //             //执行完成
        //             self.FileSet.onComplete();
        //         }
        //     })(file);
        // }

    }
    ,

    init: function () {
        var self = this;
        if (self.FileSet.fileInput == null || self.FileSet.pre == null || self.FileSet.upButton == null) {
            console.log('必须提供 input的id 预览区的id 以及 button的id');
            return false;
        }
        //文件选择控件选择
        if (self.FileSet.fileInput) {
            $(self.FileSet.fileInput).on('change', function (e) {
                var files = e.target.files;
                if (self.FileSet.fileFilter.length + files.length > 5) {
                    alert('最多上传5张图片')
                    return
                }
                self.funGetFiles(e);
            })
        }

        //上传按钮提交
        if (self.FileSet.upButton) {
            $(self.FileSet.upButton).on('click', function (e) {
                goods_id = $('#goods_id').val();
                if (goods_id) {
                } else {
                    if (checkform()) {
                        if (dex.length == 0) {
                            alert('请添加商品图片')
                            return
                        }

                    }
                }
                self.funUploadFile(e);

            })
        }
    }
}
