# 数据契约 1.0

顶层必需数组 papers、methods、groups、edges、surveys、research_tracks，metadata 为对象。允许附加审计字段。未知字符串用 null，列表用 []；必需 ID/名称不能空。ID 使用字母、数字、下划线、点、冒号或连字符，每个实体数组内唯一；边 ID 在全域与专题间全局唯一。勿用数组序号重建已有身份。

## papers

id、title（完整标题）、authors（原署名顺序字符串数组）、url、doi、arxiv_id；first_public_date、publication_date 分列，格式 YYYY / YYYY-MM / YYYY-MM-DD，精度不足不造日。date_basis 说明最早记录的证据范围，不把 arXiv v1 当绝对首次公开。venue、publication_status（preprint/accepted/published/unknown）。verification（verified/partial/pending/disputed）、provenance[]、evidence[]。字段级证据优先，总体已核不能掩盖缺项。

新增记录填 inclusion_reason、route_status（existing/new_branch/bridge）、related_method_ids。aliases、previous_ids、legacy 保存别名、合并身份和无损旧记录。

## methods

id、name、paper_ids（至少一个有效论文）、primary_group、group_ids（含主分类）、tags、aliases、modules；分析字段 problem、mechanism、contributions、value、scenarios、limitations 为字符串或 null。featured 布尔及 featured_reason；classification_basis、verification、provenance、evidence。一文多法写分拆理由，别名不得重复建方法。name 优先采用论文简称或简短技术短语（建议 ≤ 36 字符，清洗裸 LaTeX 数学语法，如 `$L^{2}DGS$` 转为 `L²DGS`），完整标题保存在 paper.title。problem 与 mechanism 分开提炼；只有单句机制概述时将 problem 置 null，不得复制 mechanism 充当 problem。

## groups

id、name、parent_id（一级 null，二级指一级）、definition、problem、rationale、representative_method_ids、index。survey_mappings 保存原综述分类及异同，candidate_alternatives 保存争议。主归属优先二级，可先保留一级待补，不创建无依据空壳。groups 数组须按“一级分类紧跟其全部二级子类”连续排列；增量新增二级子类时插入所属一级分类末尾并重排 index，不改变已有 ID。

## edges

id、source、target 指方法 ID，起点是前驱，终点是使用者；论文经 paper_ids 追溯。type 仅 direct/extension/borrow/theme。description、basis、claim_basis（fact/inference）、confidence（0–1；未校准用 null）、verification、evidence[]。theme 存储顺序无继承语义。已核非 theme 边必须为 fact，有原始全文证据、位置和核验日期；仅凭题名/元数据记录不得标为 fact；推断继承候选只能待核并明确显示。同一对方法已有技术边时不重复添加 theme 边。

## 来源和证据

provenance[]：survey_id（来自综述时）、reference_label（如 [42]）、locator（节/页/表）、url 或 source_id（本地材料键）、access_level（full_text/abstract/survey_paraphrase/metadata/legacy_import）。

evidence[]：field、url 或 source_id、source_type（primary_paper/survey/publisher/registry/legacy/synthetic）、access_level、locator、summary、可选短 quote、checked_at。支持哪个字段要明确。url_status 为 verified/pending/invalid 并保存访问日志；链接可达不等于支持论断。

## 其他顶层

surveys：id、title、url/source_id、authors、日期、access_level、taxonomy（原分类）、references（参考文献及编号）。

research_tracks：id、name、definition、enabled、method_ids、groups（同分类形状）、assignments（method、primary、memberships、role、reason）、edges（专题新增）、inclusions/exclusions（ID及理由）、global_edge_ids（可选，选择复用的全域边ID），可选 sections、update、date_audits、evidence。

metadata：schema_version="1.0"、domain、title、description、version、search_cutoff、search_range、search_log（实际 date/channel/query/scope/hits/included/excluded/failures）、coverage_limitations、first_html_delivered（交付记录）、review_decisions、unresolved、is_synthetic。统计由脚本计算，不能相信手填数量。完整示例见 assets/example-data.json。
