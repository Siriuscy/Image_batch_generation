# Image_batch_generation

图片批量生成工具，支持模板导出导入、背景图设置、文本编辑等功能。

## 功能特点

1. 模板系统
   - 支持导出当前画布为Excel模板
   - 支持导入Excel模板批量生成图片
   - 支持设置元素名称便于后续修改

2. 背景图功能
   - 支持设置背景图并自动填充整个画布
   - 背景图自动置于最底层
   - 可在模板中设置是否使用背景图

3. 文本编辑
   - 支持添加单行文本和多行文本
   - 支持设置字体、大小、颜色等属性
   - 支持文本对齐方式调整

## 使用说明

### 基本操作

1. 添加元素
   - 点击"添加文本"按钮添加单行文本
   - 点击"添加多行文本"按钮添加分区块文本
   - 点击"上传图片"按钮添加普通图片
   - 点击"设置背景"按钮添加背景图片

2. 编辑元素
   - 点击文本可以直接编辑内容
   - 选中文本后可以调整字体属性
   - 可以拖拽调整元素位置和大小

### 模板使用

1. 导出模板
   - 点击"导出模板"按钮
   - 为画布中的元素命名
   - 系统会生成包含两个工作表的Excel文件：
     - 工作表1：对象信息（包含所有元素的详细属性）
     - 工作表2：模板信息（包含元素名称，用于批量生成）

2. 导入模板
   - 准备Excel模板文件
   - 准备所需的图片文件（包括背景图）
   - 点击"导入模板"按钮
   - 选择模板文件和图片文件
   - 系统会根据模板批量生成图片

### 背景图使用说明

1. 单张编辑时
   - 点击"设置背景"按钮上传背景图
   - 背景图会自动缩放以填满整个画布
   - 背景图会自动置于最底层
   - 背景图不可选择和编辑

2. 模板批量生成时
   - 在Excel模板的第二列"背景图"中填写背景图文件名（不含扩展名）
   - 如果某张图片不需要背景图，对应行的"背景图"列留空
   - 确保背景图文件和其他图片文件一起上传
   - 系统会根据模板自动处理背景图

## 注意事项

1. 文件命名
   - 图片文件名不要包含特殊字符
   - Excel中填写的文件名不要包含扩展名
   - 确保所有引用的图片文件都已上传

2. 背景图设置
   - 背景图会被拉伸以填满画布，可能会导致图片变形
   - 建议使用分辨率合适的图片作为背景
   - 背景图设置后不可编辑，需要重新设置才能更改

3. 模板使用
   - 请勿修改Excel模板的格式和结构
   - 确保元素名称在两个工作表中保持一致
   - 批量生成时请耐心等待处理完成