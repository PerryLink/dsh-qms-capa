export type QmsErrorCode='E_QMS_NCR_FIELD_MISSING'|'E_QMS_NCR_DUPLICATE'|'E_QMS_LOT_UNRESOLVED'|'E_QMS_IMPACT_INCOMPLETE'|'E_QMS_STEP_ILLEGAL'|'E_QMS_NCR_NOT_FOUND'|'E_QMS_RECORD_NOT_FOUND'
/** User-facing text for every error code: one plain sentence plus one next action. */
const QMS_HUMAN:Record<QmsErrorCode,{text:string;next:string}>={
 E_QMS_NCR_FIELD_MISSING:{text:'NCR 记录缺少必填字段',next:'补上 plant/material/lot/defect_code/found_date 五列后再导入'},
 E_QMS_NCR_DUPLICATE:{text:'这条 NCR 已经在库里了',next:'要改数量请在原记录上更新，或换一个 found_date 再导入'},
 E_QMS_LOT_UNRESOLVED:{text:'这个批次别名没有对应的正式批号',next:'先用 qms_batch_alias 把别名指向正式批号'},
 E_QMS_IMPACT_INCOMPLETE:{text:'影响面评估缺少库存或途中快照',next:'在 snapshots 里同时给出 stock 和 intransit 两个批次清单'},
 E_QMS_STEP_ILLEGAL:{text:'这一步在记录当前状态下不能做',next:'先用 qms_capa 或 qms_8d 建单，再按状态一步步往前推'},
 E_QMS_NCR_NOT_FOUND:{text:'找不到这个 NCR 编号',next:'先 qms_ncr 导入这条 NCR，再引用它返回的编号'},
 E_QMS_RECORD_NOT_FOUND:{text:'找不到这条 CAPA 或 8D 记录',next:'用真实存在的编号，或先建单再引用'},
}
/** `human sentence（E_CODE）｜Next: one action` — the only text shown to end users. */
export function qmsErrorMessage(code:QmsErrorCode,text?:string){const h=QMS_HUMAN[code];return `${text??h.text}（${code}）｜下一步：${h.next}`}
export class QmsError extends Error{readonly code:QmsErrorCode;constructor(code:QmsErrorCode,text?:string){super(qmsErrorMessage(code,text));this.name='QmsError';this.code=code}}
export function dedupeKey(n:{plant:string;material:string;lot:string;defect_code:string;found_date:string}){return [n.plant,n.material,n.lot,n.defect_code,n.found_date].join('|')}
export function validateNcr(n:any){for(const k of ['plant','material','lot','defect_code','found_date']){if(typeof n?.[k]!=='string'||!n[k].trim())throw new QmsError('E_QMS_NCR_FIELD_MISSING',`NCR 记录缺少 ${k} 字段`)}}
