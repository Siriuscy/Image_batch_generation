// 初始化Fabric画布
var canvas = new fabric.Canvas('canvas');

// 获取文件上传控件
var imgUploader = document.getElementById('imgUploader');

// 当用户选择文件时触发
imgUploader.onchange = function (event) {
    var file = event.target.files[0]; // 获取文件对象

    if (file && file.type.match('image.*')) {
        var reader = new FileReader();

        // 文件读取完成后执行
        reader.onload = function (f) {
            var data = f.target.result;

            // 使用Fabric.js从URL加载图像
            fabric.Image.fromURL(data, function (img) {
                // 设置图像初始位置和缩放
                img.set({
                    left: 100,
                    top: 100,
                    angle: 0,
                    opacity: 1
                }).scale(0.5);

                // 将图像添加到画布中
                canvas.add(img);

                // 渲染画布
                canvas.renderAll();
            });
        };

        // 读取文件为Data URL
        reader.readAsDataURL(file);
    } else {
        alert("请选择有效的图像文件！");
    }
};