import{defineDomain,domainTable}from'@deepseek-ai/dsh-storage-domain';import type{Context}from'@deepseek-ai/cordis';import{z}from'zod'
const ncr=z.object({ncr_id:z.string(),plant:z.string(),material:z.string(),lot:z.string(),defect_code:z.string(),found_date:z.string(),quantity:z.number(),source:z.string(),recurrence_of:z.string().optional(),created_at:z.string()});const alias=z.object({alias:z.string(),canonical:z.string()})
const eightd=z.object({eightd_id:z.string(),ncr_id:z.string(),state:z.enum(['d1','d2','d3','d4','d5','d6','d7','d8','closed']),data:z.record(z.string(),z.string()),created_at:z.string(),updated_at:z.string()})
const capa=z.object({capa_id:z.string(),ncr_id:z.string(),grade:z.enum(['A','B','C']),owner:z.string(),due_date:z.string(),state:z.enum(['opened','contained','root_cause','corrective','verified','closed']),created_at:z.string(),updated_at:z.string()})
export type EightDRecord=z.infer<typeof eightd>;
export type CapaRecord=z.infer<typeof capa>;
export type NcrRecord=z.infer<typeof ncr>;export type AliasRecord=z.infer<typeof alias>;export type Table<T>={get(k:string):T|undefined;entries():IterableIterator<[string,T]>;size:number;put(k:string,v:T):Promise<void>}
export const qmsSpec=defineDomain({name:'qms',version:1,tables:{ncrs:domainTable<string,NcrRecord>(ncr),aliases:domainTable<string,AliasRecord>(alias),capas:domainTable<string,CapaRecord>(capa),eightd:domainTable<string,EightDRecord>(eightd)}})
export async function openQms(ctx:Context){const d=await ctx.storageDomain.open(qmsSpec);ctx.effect(()=>()=>d.close(),'dsh-qms-capa.domainClose');return{ncrs:d.table('ncrs') as Table<NcrRecord>,aliases:d.table('aliases') as Table<AliasRecord>,capas:d.table('capas') as Table<CapaRecord>,eightd:d.table('eightd') as Table<EightDRecord>}}
