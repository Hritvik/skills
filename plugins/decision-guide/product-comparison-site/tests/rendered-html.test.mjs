import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render(){
 const workerUrl=new URL("../dist/server/index.js",import.meta.url);
 workerUrl.searchParams.set("test",`${process.pid}-${Date.now()}`);
 const {default:worker}=await import(workerUrl.href);
 return worker.fetch(new Request("http://localhost/",{headers:{accept:"text/html"}}),{ASSETS:{fetch:async()=>new Response("Not found",{status:404})}},{waitUntil(){},passThroughOnException(){}});
}

test("renders the verified comparison workspace",async()=>{
 const response=await render(); const html=await response.text();
 assert.equal(response.status,200);
 assert.match(html,/Washing machines under ₹20,000/);
 assert.match(html,/Samsung 7 kg Ecobubble/);
 assert.match(html,/Compare selected/);
 assert.match(html,/Research limitations/);
 assert.match(html,/Rejected after review/);
 assert.doesNotMatch(html,/AquaPro|Prototype data/);
});

test("includes accessible evidence and comparison surfaces",async()=>{
 const page=await readFile(new URL("../app/page.tsx",import.meta.url),"utf8");
 assert.match(page,/role="dialog"/);
 assert.match(page,/aria-modal="true"/);
 assert.match(page,/tabIndex=\{-1\}/);
 assert.match(page,/trapDialogFocus/);
 assert.match(page,/Evidence for/);
 assert.match(page,/Comparison of/);
 assert.match(page,/onKeyDown/);
 assert.match(page,/\.limitations\.map/);
 assert.match(page,/\.rejected\.map/);
});

test("comparison dialog supports scannable decision controls",async()=>{
 const page=await readFile(new URL("../app/page.tsx",import.meta.url),"utf8");
 assert.match(page,/Hide identical rows/);
 assert.match(page,/Highlight differences/);
 assert.match(page,/aria-pressed=\{hideIdentical\}/);
 assert.match(page,/aria-pressed=\{highlightDiffs\}/);
 assert.match(page,/className=\{isBest\?"bestCell":rowSame\?"sameValue":undefined\}/);
 assert.match(page,/hideIfSame=\{hideIdentical\}/);
});

test("validates the canonical report before every build",async()=>{
 const packageJson=JSON.parse(await readFile(new URL("../package.json",import.meta.url),"utf8"));
 assert.match(packageJson.scripts.build,/validate_report\.py/);
 assert.match(packageJson.scripts.test,/node --test/);
});
