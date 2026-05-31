---
date: 2026-05-23
authors:
  - moita
categories:
  - 工程实践
  - 文件系统
tags:
  - C
  - CPP
  - 多媒体
---

# stb 基本用法

项目地址：[stb](https://github.com/nothings/stb)

stb 是一组由 Sean T. Barrett 开发的单文件、公共领域（或MIT许可证）C/C++库，旨在提供易于集成和使用的功能，涵盖图像处理、字体、音频、图形等多个方面。

<!-- more -->

## 使用方法总览

- 每个库通常是一个单一的头文件（.h）
- 在项目中只需定义特定宏，然后包含对应的头文件
- 只在一个源文件中定义实现宏，避免重复定义

## 具体用法步骤

### 1. 下载stb库

可以直接从[GitHub仓库](https://github.com/nothings/stb)下载所需的头文件，例如 `stb_image.h`、`stb_truetype.h` 等。

### 2. 在项目中引入库文件

- 只在一个源文件中定义实现宏
- 其他文件只需包含头文件

### 3. 定义实现宏

在某个源文件（如 `main.c` 或 `main.cpp`）中加入：

```c
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
```

这样会在该文件中生成库的实现代码。

### 4. 在其他文件中包含头文件

在需要使用库功能的其他文件中，只需包含头文件：

```c
#include "stb_image.h"
```

## 常用库及其用法

### 1. 图像加载（`stb_image.h`）

- 支持格式：JPG、PNG、TGA、BMP、PSD、GIF、HDR、PIC
- 主要函数：
    - `stbi_load()`：加载图像，返回像素数据
    - `stbi_image_free()`：释放像素数据

- 示例：

```c
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

int width, height, channels;
unsigned char *img = stbi_load("image.png", &width, &height, &channels, 0);
if (img) {
    // 使用图像数据
    stbi_image_free(img);
}
```

### 2. 图像写入（`stb_image_write.h`）

- 支持格式：PNG、TGA、BMP
- 主要函数：
    - `stbi_write_png()`：写入PNG
    - `stbi_write_bmp()`：写入BMP
    - `stbi_write_tga()`：写入TGA

- 示例：

```c
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

unsigned char pixels[width * height * channels];
// 填充pixels数据
stbi_write_png("output.png", width, height, channels, pixels, width * channels);
```

### 3. 字体渲染（`stb_truetype.h`）

- 解析、解码和光栅化TrueType字体
- 主要函数：
    - `stb_truetype_fontinfo`：字体信息结构
    - `stb_truetype_GetGlyphBitmap()`：获取字符光栅图

- 示例：

```c
#define STB_TRUETYPE_IMPLEMENTATION
#include "stb_truetype.h"

// 加载字体文件到内存
unsigned char ttf_buffer[1<<20];
FILE *fontFile = fopen("font.ttf", "rb");
fread(ttf_buffer, 1, sizeof(ttf_buffer), fontFile);
fclose(fontFile);

stbtt_fontinfo font;
stbtt_InitFont(&font, ttf_buffer, stbtt_GetFontOffsetForIndex(ttf_buffer, 0));
```

### 4. 图像缩放（`stb_image_resize2.h`）

- 支持高质量缩放
- 主要函数：
    - `stb_resize()`：缩放图像
- 示例：

```c
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include "stb_image_resize.h"

unsigned char *resized = malloc(new_width * new_height * channels);
stb_resize(input_pixels, resized, width, height, channels, new_width, new_height);
```

### 5. 其他常用库

- `stb_ds.h`：类型安全的动态数组和哈希表
- `stb_sprintf.h`：快速的 `sprintf` 实现
- `stb_textedit.h`：文本编辑器核心
- `stb_voxel_render.h`：体素渲染
- `stb_dxt.h`：实时Dxt压缩
- `stb_easy_font.h`：快速字体绘制
