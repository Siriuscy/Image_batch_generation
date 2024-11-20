fetch('fonts-config.json')
    .then(response => response.json())
    .then(data => {
        const fontSelector = document.getElementById('fontSelector');
        const dynamicFonts = document.getElementById('dynamicFonts');
        data.fonts.forEach(font => {
            const fontFace = `
                @font-face {
                    font-family: '${font.name}';
                    src: url('${font.path}') format('${font.format}');
                }
            `;
            dynamicFonts.innerHTML += fontFace; // 添加到样式中
            const option = document.createElement('option');
            option.value = font.name; // 字体名称
            option.textContent = font.name; // 显示名称
        fontSelector.appendChild(option);
        })
    });