---
date: 2026-05-22
authors:
  - moita
categories:
  - 工程实践
  - 文件系统
tags:
  - CPP
  - 几何处理
  - 计算机图形学
---

# libigl 基本用法

项目地址：[libigl](https://github.com/libigl/libigl)

libigl 是一个用 C++ 编写的开源几何处理库，采用 MPL-2.0 许可证。它主要用于几何网格处理、网格简化、参数化、重建等任务，广泛应用于计算机图形学、几何处理和计算机视觉等领域。

<!-- more -->

## 1. 安装与配置

### 1.1 依赖环境

- 需要 C++ 编译器（支持 C++11 及以上）
- 支持 CMake 的构建系统
- 依赖 Eigen（线性代数库）
- 可选：支持 OpenGL、GLFW 等用于可视化

### 1.2 安装步骤

- 克隆源码仓库：

```bash
git clone --recursive https://github.com/libigl/libigl.git
```

- 使用 CMake 生成项目：

```bash
cd libigl
mkdir build
cd build
cmake ..
make
```
- 在你的项目中引入 libigl 头文件和库文件

## 2. 基本用法

### 2.1 载入和显示网格

- 使用 libigl 提供的函数载入网格（如 OBJ、OFF 格式）
- 利用 libigl 的可视化工具（如 igl::opengl::glfw::Viewer）显示网格

### 2.2 简单示例

```cpp
#include <igl/readOFF.h>
#include <igl/opengl/glfw/Viewer.h>

int main() {
    Eigen::MatrixXd V;
    Eigen::MatrixXi F;
    igl::readOFF("mesh.off", V, F);
    igl::opengl::glfw::Viewer viewer;
    viewer.data().set_mesh(V, F);
    viewer.launch();
}
```

## 3. 核心功能模块

### 3.1 网格处理

- **网格简化**：`igl::decimate`，减少多边形数量
- **细分**：`igl::subdivide`，细分网格
- **平滑**：`igl::cotangent_smoothing`，拉普拉斯平滑

### 3.2 几何操作

- **网格重心**：`igl::barycenter`
- **法线计算**：`igl::per_face_normals`，`igl::per_vertex_normals`
- **边界检测**：`igl::boundary_loop`

### 3.3 参数化与重建

- **UV映射**：`igl::map_vertices_to_circle`
- **网格重建**：`igl::arap`（阿拉普拉斯-贝尔特拉米方法）

### 3.4 其他功能

- **距离场计算**：`igl::signed_distance`
- **体积计算**：`igl::volume`

## 4. 高级用法与扩展

### 4.1 自定义着色器

- 利用 libigl 的 OpenGL 接口自定义渲染效果

### 4.2 结合其他库

- 结合 Eigen 进行线性代数运算
- 结合 OpenGL 进行高级可视化

### 4.3 插件与扩展

- 开发自定义的几何处理算法
- 利用 libigl 的插件机制扩展功能

## 5. 资源与学习资料

- 官方文档：[libigl Documentation](https://libigl.github.io/)
- 示例代码：[libigl Examples](https://libigl.github.io/tutorial/)
- 相关论文：[libigl Paper](https://arxiv.org/abs/1804.05590)
