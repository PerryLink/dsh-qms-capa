export type QmsErrorCode='E_QMS_NCR_FIELD_MISSING'|'E_QMS_NCR_DUPLICATE'|'E_QMS_LOT_UNRESOLVED'|'E_QMS_IMPACT_INCOMPLETE'|'E_QMS_STEP_ILLEGAL'
export class QmsError extends Error{readonly code:QmsErrorCode;constructor(code:QmsErrorCode,message:string){super(`${code}: ${message}`);this.name='QmsError';this.code=code}}
export function dedupeKey(n:{plant:string;material:string;lot:string;defect_code:string;found_date:string}){return [n.plant,n.material,n.lot,n.defect_code,n.found_date].join('|')}
export function validateNcr(n:any){for(const k of ['plant','material','lot','defect_code','found_date']){if(typeof n?.[k]!=='string'||!n[k].trim())throw new QmsError('E_QMS_NCR_FIELD_MISSING',`missing ${k}`)}}
