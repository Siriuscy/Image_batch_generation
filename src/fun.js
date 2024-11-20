const XLSX = require('xlsx');
// 获取画布元素
const canvas = new fabric.Canvas('canvas');
let selectedText = null; // 用于存储当前选中的文本对象
let rectangleCount = 0; // 计数器，用于跟踪添加的矩形数量
let historyStack = []; // 操作历史栈
const MAX_HISTORY_SIZE = 10; // 最大历史记录大小

// 存储生成的画布状态
let generatedCanvases = [];
let currentCanvasIndex = -1;

// 更新导航按钮状态
function updateNavigationButtons() {
    const prevButton = document.getElementById('prevCanvas');
    const nextButton = document.getElementById('nextCanvas');
    const counter = document.getElementById('canvasCounter');
    const downloadButton = document.getElementById('downloadCurrent');

    prevButton.disabled = currentCanvasIndex <= 0;
    nextButton.disabled = currentCanvasIndex >= generatedCanvases.length - 1;
    downloadButton.disabled = generatedCanvases.length === 0;

    if (generatedCanvases.length > 0) {
        counter.textContent = `${currentCanvasIndex + 1} / ${generatedCanvases.length}`;
    } else {
        counter.textContent = '0 / 0';
    }
}

// 显示指定索引的画布内容
function showCanvas(index) {
    if (index < 0 || index >= generatedCanvases.length) return;
    
    currentCanvasIndex = index;
    canvas.clear();
    canvas.loadFromJSON(generatedCanvases[index], function() {
        canvas.renderAll();
        updateNavigationButtons();
    });
}

// 导航按钮事件处理
document.getElementById('prevCanvas').addEventListener('click', function() {
    showCanvas(currentCanvasIndex - 1);
});

document.getElementById('nextCanvas').addEventListener('click', function() {
    showCanvas(currentCanvasIndex + 1);
});

// 下载当前画布
document.getElementById('downloadCurrent').addEventListener('click', async function() {
    if (currentCanvasIndex < 0) return;

    const dataURL = canvas.toDataURL({
        format: 'png',
        quality: 1
    });

    const blob = await (await fetch(dataURL)).blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `output_${currentCanvasIndex + 1}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
});

// 保存状态到历史栈的函数
function saveState() {
    const json = canvas.toJSON(['selectable', 'evented', 'name']);
    if (historyStack.length >= MAX_HISTORY_SIZE) {
        historyStack.shift();
    }
    historyStack.push(json);
}

// 恢复状态的函数
function restoreState(state) {
    canvas.loadFromJSON(state, function() {
        // 恢复每个对象的特定属性
        canvas.getObjects().forEach(obj => {
            if (obj.name === 'background') {
                obj.set({
                    selectable: false,
                    evented: false
                });
                obj.sendToBack();
            }
        });
        canvas.renderAll();
    });
}

// 处理文件上传
document.getElementById('imageUpload').addEventListener('change', function(event) {
    const file = event.target.files[0]; // 获取用户选择的文件
    if (!file) return; // 如果没有选择文件，则返回

    const reader = new FileReader(); // 创建 FileReader 对象
    reader.onload = function(e) {
        const base64Data = e.target.result; // 获取 Base64 数据 URL
        console.log('Base64 Data URL:', base64Data); // 输出 Base64 数据 URL

        // 使用 fabric.Image.fromURL 加载 Base64 数据
        fabric.Image.fromURL(base64Data, function(img) {
            console.log(`Image loaded and added to canvas: ${file.name}`);
            
            // 计算缩放比例
            const canvasAspectRatio = canvas.width / canvas.height; // 画布的宽高比
            const imgAspectRatio = img.width / img.height; // 图片的宽高比

            // 根据宽高比调整图片的大小
            if (canvasAspectRatio > imgAspectRatio) {
                img.scaleToHeight(canvas.height * 0.8); // 使图片高度为画布高度的80%
            } else {
                img.scaleToWidth(canvas.width * 0.8); // 使图片宽度为画布宽度的80%
            }
            console.log(`Image scaled to: ${img.width * img.scaleX} x ${img.height * img.scaleY}`);

            img.set({
                left: (canvas.width - img.width * img.scaleX) / 2, // 居中显示
                top: (canvas.height - img.height * img.scaleY) / 2, // 居中显示
                hasControls: true,
                hasBorders: true,
                name: file.name
            });

            // 将图片添加到画布
            canvas.add(img);
            saveState(); // 保存状态到历史栈
            canvas.renderAll(); // 重新渲染画布以显示新添加的图片
        }, {
            error: function(err) {
                console.error('Error loading image:', err); // 输出错误信息
            }
        });
    };

    reader.readAsDataURL(file); // 读取文件为 Data URL
});

// 处理添加文本的功能
function addSingleLineText() {
    const singleLineText = new fabric.IText('单行文本', {
        left: Math.random() * canvas.width/2,
        top: Math.random() * canvas.height/2,
        fontSize: 20,
        fill: '#000000',
        selectable: true,
        fontFamily: '思源汉字无衬线CN中等',
        textAlign: 'center' // 设置文本居中
    });
    canvas.add(singleLineText);
    saveState(); // 保存状态到历史栈
}

// 添加分区块文本的功能
function addMultiLineText() {
    const multiLineText = new fabric.Textbox('这是分区块文本', {
        left: Math.random() * canvas.width/2,
        top: Math.random() * canvas.height/2,
        width: 150,
        fontSize: 20,
        fill: '#000000',
        fontFamily: '思源汉字无衬线CN中等',
        lockScalingY: true,
        lockScalingX: true,
        selectable: true,
        splitByGrapheme: true
    });
    canvas.add(multiLineText);
    saveState(); // 保存状态到历史栈
}

// 绑定按钮点击事件
document.getElementById('addText').addEventListener('click', addSingleLineText);
document.getElementById('addMultiLineText').addEventListener('click', addMultiLineText);

// 处理文本点击事件
canvas.on('mouse:down', function(event) {
    if (event.target instanceof fabric.IText || event.target instanceof fabric.Textbox) {
        selectedText = event.target;
        document.getElementById('textPropertiesPanel').style.display = 'block'; // 显示文本属性面板
        document.getElementById('fontSize').value = selectedText.fontSize; // 设置当前字体大小
        document.getElementById('fontColor').value = selectedText.fill; // 设置当前字体颜色
        document.getElementById('fontSelector').value = selectedText.fontFamily; // 设置当前字体
        document.getElementById('text-align').value = selectedText.textAlign; // 设置当前文本对齐
    }
});

// 监听字体选择变化
document.getElementById('fontSelector').addEventListener('change', function() {
    if (selectedText) {
        const selectedFont = this.value;
        selectedText.set('fontFamily', selectedFont); // 更新字体
        canvas.renderAll(); // 重新渲染画布
    }
});

// 监听文本对齐选择变化
document.getElementById('text-align').addEventListener('change', function() {
    if (selectedText) {
        const selectedAlign = this.value;
        selectedText.set('textAlign', selectedAlign); // 更新对齐方式
        canvas.renderAll(); // 重新渲染画布
    }
});

// 监听字体大小输入框变化
document.getElementById('fontSize').addEventListener('input', function() {
    if (selectedText) {
        const newSize = parseInt(this.value, 10);
        if (!isNaN(newSize)) {
            selectedText.set('fontSize', newSize); // 更新字体大小
            canvas.renderAll(); // 重新渲染画布
        }
    }
});

// 监听字体颜色输入框变化
document.getElementById('fontColor').addEventListener('input', function() {
    if (selectedText) {
        const newColor = this.value;
        selectedText.set('fill', newColor); // 更新字体颜色
        canvas.renderAll(); // 重新渲染画布
    }
});

// 导出模板功能
document.getElementById('export-template').addEventListener('click', function() {
    // 显示遮罩层
    document.getElementById('overlay').style.display = 'block'; // 显示遮罩层

    // 获取 canvas 对象
    const canvasObjects = canvas.getObjects().filter(obj => obj.name !== 'background'); // 过滤掉背景图
    const canvasInfoTableBody = document.getElementById('canvas-info');

    // 清空表格内容
    canvasInfoTableBody.innerHTML = '';

    // 填充表格
    canvasObjects.forEach(obj => {
        const row = document.createElement('tr');
        
        // 创建输入框用于用户输入名称
        const nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.placeholder = '请输入名称'; // 提示用户输入名称

        // 获取字体颜色信息（如果对象有 fill 属性）
        const fontColor = (obj.type !== 'image') ? (obj.fill || '无') : '无'; // 如果是图片，字体颜色为“无”

        if (obj.type === 'image') {
            // 仅包括位置信息
            row.innerHTML = `
                <td>${nameInput.outerHTML}</td> <!-- 添加名称输入框 -->
                <td>${obj.type}</td>
                <td>${Math.round(obj.left)}</td> <!-- 保留整数 -->
                <td>${Math.round(obj.top)}</td> <!-- 保留整数 -->
                <td>无</td> <!-- 宽度 -->
                <td>无</td> <!-- 高度 -->
                <td>无</td> <!-- 字体颜色 -->
                <td>无</td> <!-- 文本对齐 -->
                <td>${obj.name || '无'}</td> <!-- 使用文件名称 -->
            `;
        } else if (obj.type === 'i-text' || obj.type === 'textbox') {
            // 包括文本信息，输出前五个字
            const textContent = obj.text || ''; // 获取文本内容
            const firstFiveChars = textContent.substring(0, 5); // 提取前五个字

            row.innerHTML = `
                <td>${nameInput.outerHTML}</td> <!-- 添加名称输入框 -->
                <td>${obj.type}</td>
                <td>${Math.round(obj.left)}</td> <!-- 保留整数 -->
                <td>${Math.round(obj.top)}</td> <!-- 保留整数 -->
                <td>${Math.round(obj.width)}</td> <!-- 保留整数 -->
                <td>${Math.round(obj.height)}</td> <!-- 保留整数 -->
                <td>${fontColor}</td> <!-- 字体颜色 -->
                <td>${obj.textAlign || '无'}</td> <!-- 文本对齐 -->
                <td>${firstFiveChars}</td> <!-- 输出前五个字 -->
            `;
        } else {
            // 包括其他信息
            row.innerHTML = `
                <td>${nameInput.outerHTML}</td> <!-- 添加名称输入框 -->
                <td>${obj.type}</td>
                <td>${Math.round(obj.left)}</td> <!-- 保留整数 -->
                <td>${Math.round(obj.top)}</td> <!-- 保留整数 -->
                <td>${Math.round(obj.width)}</td> <!-- 保留整数 -->
                <td>${Math.round(obj.height)}</td> <!-- 保留整数 -->
                <td>${fontColor}</td> <!-- 字体颜色 -->
                <td>${obj.textAlign || '无'}</td> <!-- 文本对齐 -->
            `;
        }

        canvasInfoTableBody.appendChild(row);
    });

    // 导出为图片
    const scaleFactor = 2; // 设置缩放因子，2表示导出为2倍高
    const imageData = canvas.toDataURL({ 
        multiplier: scaleFactor,
        format: 'jpg' }); // 导出为 PNG 格式
    const downloadLink = document.createElement('a');
    downloadLink.href = imageData; // 设置链接为导出的图像数据
    downloadLink.download = 'canvas-template.jpg'; // 设置下载文件名
    downloadLink.innerText = '下载图片'; // 设置链接文本
    document.getElementById('export-panel').appendChild(downloadLink); // 将链接添加到面板中


    // 显示面板
    document.getElementById('export-panel').style.display = 'block';
});

// 关闭面板
document.getElementById('close-panel').addEventListener('click', function() {
    document.getElementById('export-panel').style.display = 'none'; // 隐藏面板
    document.getElementById('overlay').style.display = 'none'; // 隐藏遮罩层
});

// 下载 Excel
document.getElementById('download-excel').addEventListener('click', function() {
    const canvasObjects = canvas.getObjects().filter(obj => obj.name !== 'background' || !obj.name);
    // const canvasObjects = canvas.getObjects();
    console.log('Canvas objects:', canvasObjects); // Debug log
    
    const data = canvasObjects.map(obj => {
        const fontColor = (obj.type !== 'image') ? (obj.fill || '无') : '无';
        const textContent = (obj.type === 'i-text' || obj.type === 'textbox') ? obj.text || '无' : '无';
        
        // 基本属性
        const baseProperties = {
            elementName: '', // 这个会从表格中获取
            type: obj.type,
            left: Math.round(obj.left),
            top: Math.round(obj.top),
            width: Math.round(obj.type === 'image' ? obj.getScaledWidth() : obj.width * obj.scaleX),
            height: Math.round(obj.type === 'image' ? obj.getScaledHeight() : obj.height * obj.scaleY)
        };

        // 根据对象类型添加特定属性
        if (obj.type === 'image') {
            return {
                ...baseProperties,
                fontColor: '无',
                textAlign: '无',
                content: obj.name || '无'
            };
        } else {
            return {
                ...baseProperties,
                fontColor: fontColor,
                textAlign: obj.textAlign || '无',
                fontSize: obj.fontSize || '无', // 保存字号信息
                fontFamily: obj.fontFamily || '无',  // 字体族
                charSpacing: obj.charSpacing || '无', // 字符间距
                lineHeight: obj.lineHeight || '无',  // 行高
                underline: obj.underline || false,  // 下划线
                fontWeight: obj.fontWeight || '无',  // 字体粗细
                fontStyle: obj.fontStyle || '无',    // 字体样式（斜体等）
                content: textContent
            };
        }
    });

    console.log('Final data array:', data); // Debug log

    // 从表格中获取用户输入的名称
    const tableRows = document.querySelectorAll('#canvas-info tr');
    Array.from(tableRows).forEach((row, index) => {
        if (data[index]) {
            const nameInput = row.querySelector('input[type="text"]');
            if (nameInput) {
                data[index].elementName = nameInput.value || '';
            }
        }
    });

    // 创建工作表1的数据
    const headers = ["元素名称", "类型", "左边距", "上边距", "宽度", "高度", "字体颜色", "文本对齐", "字号", 
                    "字体", "字符间距", "行高", "下划线", "字体粗细", "字体样式", "内容"];
    const worksheet1Data = [
        headers,
        ...data.map(item => [
            item.elementName,
            item.type,
            item.left,
            item.top,
            item.width,
            item.height,
            item.fontColor,
            item.textAlign,
            item.fontSize,
            item.fontFamily,
            item.charSpacing,
            item.lineHeight,
            item.underline,
            item.fontWeight,
            item.fontStyle,
            item.content
        ])
    ];

    // 创建工作表2的数据（横向排列）
    const elementNames = data.map(item => item.elementName).filter(name => name && name !== 'background');
    const worksheet2Data = [
        ["元素名称", "背景图", ...elementNames]  // 保留"背景图"列但不需要用户填写
    ];

    // 创建工作簿
    const wb = XLSX.utils.book_new();

    // 创建工作表1
    const ws1 = XLSX.utils.aoa_to_sheet(worksheet1Data);
    XLSX.utils.book_append_sheet(wb, ws1, "对象信息");

    // 创建工作表2
    const ws2 = XLSX.utils.aoa_to_sheet(worksheet2Data);
    XLSX.utils.book_append_sheet(wb, ws2, "模板信息");

    // 导出Excel文件
    XLSX.writeFile(wb, "canvas_objects.xlsx");
});

// 监听键盘事件以处理删除操作
document.addEventListener('keydown', function(event) {
    // Delete 键删除选中对象
    if (event.key === 'Delete' || event.key === 'Backspace') {
        // Check if we're currently editing text
        const activeObject = canvas.getActiveObject();
        if (activeObject && (activeObject.isEditing || (activeObject.type === 'i-text' && activeObject.hiddenTextarea === document.activeElement))) {
            return; // If we're editing text, let the default backspace behavior handle it
        }
        
        // Otherwise proceed with object deletion
        if (selectedText) {
            canvas.remove(selectedText);
            selectedText = null;
            canvas.renderAll();
            saveState();
        } else if (activeObject) {
            canvas.remove(activeObject);
            canvas.renderAll();
            saveState();
        }
    }
    
    // 撤回操作
    if ((event.metaKey || event.ctrlKey) && event.key === 'z') {
        if (historyStack.length > 1) { // 改为 > 1 以保留至少一个状态
            historyStack.pop(); // 移除当前状态
            const lastState = historyStack[historyStack.length - 1]; // 获取前一个状态
            restoreState(lastState);
        }
    }
});

// 批量生成功能
document.getElementById('autoGenerate').addEventListener('click', function() {
    document.getElementById('overlay').style.display = 'block';
    document.getElementById('batch-panel').style.display = 'block';
});

document.getElementById('close-batch-panel').addEventListener('click', function() {
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('batch-panel').style.display = 'none';
});

// 处理模板文件选择
document.getElementById('template-file').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    if (!file.name.endsWith('.xlsx')) {
        alert('请选择正确的Excel模板文件！');
        this.value = '';
        return;
    }
});

// 处理图片文件夹选择
document.getElementById('image-folder').addEventListener('change', function(e) {
    const files = Array.from(e.target.files);
    const imageFiles = files.filter(file => 
        file.type.startsWith('image/') || 
        file.name.toLowerCase().match(/\.(jpg|jpeg|png|gif)$/)
    );
    
    if (imageFiles.length === 0) {
        alert('所选文件夹中没有找到图片文件！');
        this.value = '';
        return;
    }
});

// 开始批量生成
document.getElementById('start-batch').addEventListener('click', async function() {
    const templateFile = document.getElementById('template-file').files[0];
    const imageFolder = document.getElementById('image-folder').files;
    
    if (!templateFile || imageFolder.length === 0) {
        alert('请先选择模板文件和图片文件夹！');
        return;
    }

    // 过滤出所有图片文件
    const imageFiles = Array.from(imageFolder).filter(file => 
        file.type.startsWith('image/') || 
        file.name.toLowerCase().match(/\.(jpg|jpeg|png)$/)
    );

    console.log('Found image files:', imageFiles.map(f => f.name));

    try {
        // 读取Excel文件
        const reader = new FileReader();
        reader.onload = async function(e) {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, {type: 'array'});
            
            // 获取两个工作表的数据
            const metadataSheet = workbook.Sheets[workbook.SheetNames[0]]; // 元数据表
            const contentSheet = workbook.Sheets[workbook.SheetNames[1]]; // 内容表
            
            // 转换为JSON格式
            const metadata = XLSX.utils.sheet_to_json(metadataSheet);
            const contentRows = XLSX.utils.sheet_to_json(contentSheet, {header: 1});
            
            // 获取表头（第一行）和数据（后续行）
            const headers = contentRows[0];
            
            console.log('Metadata:', metadata);
            console.log('Headers:', headers);
            console.log('Content rows:', contentRows);

            // 创建元素名称到元数据的映射
            const elementMetadata = {};
            metadata.forEach(item => {
                elementMetadata[item['元素名称']] = item;
            });

            // 创建进度显示
            const progressDiv = document.createElement('div');
            progressDiv.style.position = 'fixed';
            progressDiv.style.top = '50%';
            progressDiv.style.left = '50%';
            progressDiv.style.transform = 'translate(-50%, -50%)';
            progressDiv.style.background = 'white';
            progressDiv.style.padding = '20px';
            progressDiv.style.border = '1px solid black';
            progressDiv.style.zIndex = '1000';
            document.body.appendChild(progressDiv);

            try {
                // 清空之前的画布状态
                generatedCanvases = [];
                currentCanvasIndex = -1;
                updateNavigationButtons();

                // 处理每一行数据（跳过表头）
                for (let i = 1; i < contentRows.length; i++) {
                    const contents = contentRows[i];
                    if (!contents || contents.length === 0) continue; // 跳过空行

                    progressDiv.textContent = `正在生成第 ${i} 张图片，共 ${contentRows.length - 1} 张...`;

                    // 创建新的画布
                    canvas.clear();

                    // 首先处理背景图
                    const backgroundContent = contents[1]; // 背景图是第二列（索引1）
                    if (backgroundContent) {
                        // 查找匹配的背景图文件
                        const bgFile = imageFiles.find(file => {
                            const baseName = file.name.split('.')[0];
                            return baseName === backgroundContent.toString();
                        });

                        if (bgFile) {
                            console.log(`Found background image: ${bgFile.name}`);
                            // 读取并添加背景图
                            await new Promise((resolve, reject) => {
                                const bgReader = new FileReader();
                                bgReader.onload = function(event) {
                                    fabric.Image.fromURL(event.target.result, function(img) {
                                        if (!img) {
                                            console.error('Failed to create background image');
                                            reject(new Error('Failed to create background image'));
                                            return;
                                        }
                                        // 设置背景图大小以填满画布
                                        const scaleX = canvas.width / img.width;
                                        const scaleY = canvas.height / img.height;
                                        
                                        img.set({
                                            scaleX: scaleX,
                                            scaleY: scaleY,
                                            originX: "left",
                                            originY: 'top',
                                            left: 0,
                                            top: 0,
                                            selectable: false, // 背景图不可选择
                                            evented: false,     // 背景图不响应事件
                                            name: 'background'     // 背景图不响应事件

                                        });
                                        canvas.add(img);
                                        img.sendToBack();
                                        canvas.renderAll();
                                        resolve();
                                    });
                                };
                                bgReader.onerror = reject;
                                bgReader.readAsDataURL(bgFile);
                            });
                        }
                    }

                    // 处理其他元素（跳过第一列"元素名称"和第二列"背景图"）
                    for (let j = 2; j < headers.length; j++) {
                        const elementName = headers[j];
                        const content = contents[j];
                        const meta = elementMetadata[elementName];

                        if (!meta || !content) continue; // 跳过空内容或没有元数据的元素

                        console.log(`Processing element: ${elementName}, content: ${content}, type: ${meta['类型']}`);

                        if (meta['类型'] === 'image') {
                            // 查找匹配的图片文件
                            const imgFile = imageFiles.find(file => {
                                const baseName = file.name.split('.')[0];
                                return baseName === content.toString();
                            });

                            if (imgFile) {
                                console.log(`Found matching image: ${imgFile.name}`);
                                // 读取并添加图片
                                await new Promise((resolve, reject) => {
                                    const imgReader = new FileReader();
                                    imgReader.onload = function(event) {
                                        fabric.Image.fromURL(event.target.result, function(img) {
                                            if (!img) {
                                                console.error('Failed to create image');
                                                reject(new Error('Failed to create image'));
                                                return;
                                            }
                                            img.set({
                                                left: parseFloat(meta['左边距']),
                                                top: parseFloat(meta['上边距']),
                                                scaleX: parseFloat(meta['宽度']) / img.width,
                                                scaleY: parseFloat(meta['高度']) / img.height
                                            });
                                            canvas.add(img);
                                            canvas.renderAll();
                                            resolve();
                                        });
                                    };
                                    imgReader.onerror = reject;
                                    imgReader.readAsDataURL(imgFile);
                                });
                            } else {
                                console.warn(`No matching image found for: ${content}`);
                            }
                        } else if (meta['类型'] === 'i-text') {
                            // 添加可交互文本
                            const textObj = new fabric.IText(content.toString(), {
                                left: parseFloat(meta['左边距']),
                                top: parseFloat(meta['上边距']),
                                width: parseFloat(meta['宽度']),
                                height: parseFloat(meta['高度']),
                                fill: meta['字体颜色'],
                                textAlign: meta['文本对齐'],
                                fontSize: parseFloat(meta['字号']),
                                fontFamily: meta['字体'] || '思源汉字无衬线CN中等',
                                charSpacing: meta['字符间距'] !== '无' ? parseFloat(meta['字符间距']) : 0,
                                lineHeight: meta['行高'] !== '无' ? parseFloat(meta['行高']) : 1.16,
                                underline: meta['下划线'] === 'true',
                                fontWeight: meta['字体粗细'] !== '无' ? meta['字体粗细'] : 'normal',
                                fontStyle: meta['字体样式'] !== '无' ? meta['字体样式'] : 'normal'
                            });
                            canvas.add(textObj);
                            canvas.renderAll();
                        } else if (meta['类型'] === 'textbox') {
                            // 添加多行文本框
                            const textObj = new fabric.Textbox(content.toString(), {
                                left: parseFloat(meta['左边距']),
                                top: parseFloat(meta['上边距']),
                                width: parseFloat(meta['宽度']),
                                // height: parseFloat(meta['高度']),
                                fill: meta['字体颜色'],
                                textAlign: meta['文本对齐'],
                                fontSize: parseFloat(meta['字号']),
                                fontFamily: meta['字体'] || '思源汉字无衬线CN中等',
                                charSpacing: meta['字符间距'] !== '无' ? parseFloat(meta['字符间距']) : 0,
                                lineHeight: meta['行高'] !== '无' ? parseFloat(meta['行高']) : 1.16,
                                underline: meta['下划线'] === 'true',
                                fontWeight: meta['字体粗细'] !== '无' ? meta['字体粗细'] : 'normal',
                                fontStyle: meta['字体样式'] !== '无' ? meta['字体样式'] : 'normal',
                                splitByGrapheme: true,
                                lockScalingY: true,
                                lockScalingX: true
                            });
                            canvas.add(textObj);
                            canvas.renderAll();
                        }
                    }

                    // 等待所有元素渲染完成
                    await new Promise(resolve => setTimeout(resolve, 1000));

                    // 保存画布状态
                    generatedCanvases.push(JSON.stringify(canvas.toJSON()));
                }

                // 显示第一张图片
                if (generatedCanvases.length > 0) {
                    currentCanvasIndex = 0;
                    showCanvas(0);
                }

                document.body.removeChild(progressDiv);
                alert('批量生成完成！使用导航按钮查看所有生成的图片。');
                document.getElementById('overlay').style.display = 'none';
                document.getElementById('batch-panel').style.display = 'none';
            } catch (error) {
                console.error('Error during generation:', error);
                document.body.removeChild(progressDiv);
                alert('生成过程中出错：' + error.message);
            }
        };
        
        reader.readAsArrayBuffer(templateFile);
    } catch (error) {
        console.error('Error processing files:', error);
        alert('处理文件时出错，请检查文件格式是否正确！');
    }
});

// 添加背景图处理
const backgroundUpload = document.getElementById('backgroundUpload');
let backgroundImage = null;

backgroundUpload.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            fabric.Image.fromURL(event.target.result, function(img) {
                // 调整图片大小以填充画布
                const scaleX = canvas.width / img.width;
                const scaleY = canvas.height / img.height;
                
                img.set({
                    scaleX: scaleX,
                    scaleY: scaleY,
                    originX: "left",
                    originY: 'top',
                    left: 0,
                    top: 0,
                    selectable: false, // 背景图不可选择
                    evented: false,     // 背景图不响应事件
                    name: "background"
                });

                // 如果已存在背景图，先移除
                if (backgroundImage) {
                    canvas.remove(backgroundImage);
                }
                
                // 将新图片设置为背景并放到最底层
                backgroundImage = img;
                canvas.add(img);
                img.sendToBack();
                canvas.renderAll();
            });
        };
        reader.readAsDataURL(file);
    }
});
