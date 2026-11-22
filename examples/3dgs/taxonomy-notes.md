# 3DGS 技术方向命名说明

本次根据领域综述的章节术语、代表方法的机制和现有分组范围修订导航名称。中文名称是对文献术语的编辑归纳，不宣称这21类是某篇综述的原始分类或唯一标准体系。

调整范围仅为分类名称、短说明、定义和命名依据；分类ID、493个方法的归属、484条关系、论文信息及核验状态均保持不变。图谱仍默认显示全部方法，没有精选主线或专题配置。

| 原名称 | 新名称 | 对应英文术语 | 方法数 | 命名依据 |
|---|---|---|---:|---|
| 基础表示 | 辐射场表示 | Radiance Field Representations | 2 | S1 II；S2 2.1 |
| 结构、压缩与 LOD | 3DGS 效率优化 | Efficient 3D Gaussian Splatting | 24 | S3 III-A |
| 抗混叠与视角稳定 | 高斯光栅化 | Gaussian Rasterization | 14 | S3 VI-C；P1 |
| 反射、材质与光照 | 外观建模 | Appearance Modeling | 34 | S2 3.2；S3 III-B、V-D |
| 细节、初始化与增密 | 高斯表示优化 | Gaussian Representation Optimization | 15 | S2 2.2；S3 VI-A、VI-D、VI-F |
| 稀疏视角与先验 | 稀疏视角重建 | Sparse-view Reconstruction | 7 | S2 2.5；S3 III-D |
| 替代基元与渲染 | 渲染基元设计 | Rendering Primitive Design | 12 | S1 III；S3 VI-B、VII-B |
| 表面与网格重建 | 三维几何重建 | 3D Geometry Reconstruction | 22 | S2 4.2；S3 V-B、VII-B |
| 动态表示与重建 | 动态场景重建 | Dynamic Scene Reconstruction | 28 | S1 IV-B；S2 2.4；S3 V-A |
| 街景与大范围场景 | 大规模场景重建 | Large-scale Scene Reconstruction | 12 | S2 2.5；S3 IV-C |
| 前馈与泛化重建 | 学习式三维重建 | Learning-based 3D Reconstruction | 38 | S2 2.5；S3 III-C；P2、P3、P4 |
| 相机优化与采集退化 | 鲁棒三维重建 | Robust 3D Reconstruction | 12 | S2 2.5；S3 III-B、VIII-B |
| 医疗与内镜 | 医学三维重建 | Medical 3D Reconstruction | 8 | S2 2.4；P5 |
| 编辑与运动控制 | 三维场景编辑 | 3D Scene Editing | 23 | S1 V；S2 3；S3 V-C |
| 物理仿真与交互 | 物理仿真 | Physics Simulation | 8 | S1 III-D；S2 3.3；S3 V-F |
| 3D / 4D 生成 | 3D/4D 内容生成 | 3D/4D Content Generation | 39 | S1 VI；S2 4.4；S3 IV-B |
| 语义与分割 | 三维语义理解 | 3D Semantic Understanding | 18 | S1 VII；S2 4.1；S3 V-E |
| 高斯 SLAM 与定位 | 3DGS-SLAM | 3D Gaussian Splatting SLAM | 64 | S1 VII-D；S2 4.2；S3 IV-C2 |
| 神经 SLAM 背景 | 神经隐式 SLAM | Neural Implicit SLAM | 66 | S2 4.2；P6 |
| 机器人与配准 | 机器人场景建模 | Scene Modeling for Robotics | 5 | S1 I、VII；P7 |
| 人体与头部 Avatar | 数字人建模 | Digital Human Modeling | 42 | S1 VIII；S2 4.3；S3 IV-A；P8 |

## 命名时的范围判断

- “高斯光栅化”同时容纳抗混叠、深度排序和透明度混合；StopThePop的主要机制是分层排序，不能把这一组都称为抗混叠方法。[P1]
- “学习式三维重建”采用较宽口径：MVSplat使用前馈预测，但GaussianObject使用生成式修复，Touch-GS使用视触觉监督，因此没有把现有38个条目全部改称“纯前馈重建”。[P2–P4]
- “三维几何重建”不等于所有方法都输出网格；“数字人建模”覆盖全身、头部及毛发，避免把不同层次的对象并列成标题。
- 当前分组仍有交叉：pixelSplat、Splatter Image等位于几何组，和学习式重建有重叠；部分渲染算子也位于表示优化组。这些是后续可单独复核的归属问题，本次没有用改名掩盖，也没有擅自移动方法。

## 来源

核对日期：2026-11-14。综述读取了网页章节，代表论文按摘要/论文页面核对术语和任务；这不等于完成全部收录论文的全文核验。

- S1：[Fei et al., 3D Gaussian Splatting as a New Era: A Survey](https://arxiv.org/html/2402.07181v2)，II–VIII。
- S2：[Wu et al., Recent Advances in 3D Gaussian Splatting](https://arxiv.org/html/2403.11134v2)，2–4。
- S3：[Bao et al., 3D Gaussian Splatting: Survey, Technologies, Challenges, and Opportunities](https://arxiv.org/html/2407.17418v2)，III–VII。
- P1：[StopThePop](https://arxiv.org/abs/2402.00525)，摘要：分层光栅化和深度重排序。
- P2：[MVSplat](https://arxiv.org/abs/2403.14627)，摘要：由稀疏多视角图像前馈预测高斯。
- P3：[GaussianObject](https://arxiv.org/abs/2402.10259)，摘要：少视角对象重建和生成式修复。
- P4：[Touch-GS](https://arxiv.org/abs/2403.09875)，摘要：视触觉监督的高斯重建。
- P5：[EndoGaussian](https://arxiv.org/abs/2401.12561)，摘要：动态内镜场景重建。
- P6：[NICE-SLAM](https://arxiv.org/abs/2112.12130)，论文标题及摘要：神经隐式SLAM。
- P7：[ManiGaussian](https://arxiv.org/abs/2403.08321)，摘要：机器人操作中的动态场景表示。
- P8：[GaussianAvatars](https://arxiv.org/abs/2312.02069)，摘要：可驱动的高斯头部化身。
