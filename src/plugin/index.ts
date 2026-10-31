import type{Context}from'@deepseek-ai/cordis';import{createTools}from'./tools.js';import{openQms}from'./storage.js'
export const name='dsh-qms-capa';export const inject=['tools','storageDomain']
export async function apply(ctx:Context):Promise<void>{const{ncrs,aliases,capas,eightd}=await openQms(ctx);for(const t of createTools({ncrs,aliases,capas,eightd}))ctx.tools.register(t)}
