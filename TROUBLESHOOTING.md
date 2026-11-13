# 故障排查 — dsh-qms-capa

每条按「症状 / 原因 / 动作」写。报错原文都是 `<一句人话>（E_XXX）｜下一步：<动作>`，
把 `E_XXX` 和这句话一起发到 issue 即可定位；不要把真实工厂数据贴进 issue。

## 1. NCR 记录缺字段（E_QMS_NCR_FIELD_MISSING）

- **症状**：`NCR 记录缺少 plant 字段（E_QMS_NCR_FIELD_MISSING）｜下一步：补上 plant/material/lot/defect_code/found_date 五列后再导入`
- **原因**：CSV 少了一列，或表头写成了中文 / 大小写不一致（如 `Plant`、`批次`）。
- **动作**：把表头改成 `plant,material,lot,defect_code,found_date`，每行都填非空值，再跑 `qms_ncr`。

## 2. 找不到 NCR / CAPA / 8D 编号（E_QMS_NCR_NOT_FOUND / E_QMS_RECORD_NOT_FOUND）

- **症状**：`找不到这个 NCR 编号（E_QMS_NCR_NOT_FOUND）｜下一步：先 qms_ncr 导入这条 NCR，再引用它返回的编号`
- **原因**：引用了不存在的编号，或把上一轮的临时编号用在了新的空库里。
- **动作**：先用 `qms_ncr` 导入并记下返回的 `ncrs[]`；CAPA / 8D 用同一次运行返回的 `capa_id` / `eightd_id`。

## 3. 影响面评估缺快照（E_QMS_IMPACT_INCOMPLETE）

- **症状**：`影响面评估缺少库存或途中快照（E_QMS_IMPACT_INCOMPLETE）｜下一步：在 snapshots 里同时给出 stock 和 intransit 两个批次清单`
- **原因**：`snapshots` 只给了 `stock` 或只给了 `intransit`，工具无法判断召回提示。
- **动作**：两个字段都传数组（可以为空数组），再调 `qms_impact`；批次别名先用 `qms_batch_alias` 指到正式批号。

## 还不行

```sh
node samples/quickstart/run.mjs --check   # 自带样例必须通过
node --test test/*.test.mjs               # 15 项测试
```

仍失败时请在 <https://github.com/PerryLink/dsh-qms-capa/issues> 附上：包版本、最小合成输入、完整报错那一行。
