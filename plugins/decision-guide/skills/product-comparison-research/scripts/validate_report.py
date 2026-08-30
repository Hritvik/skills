#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT_FIELDS={"schemaVersion","status","reportId","title","category","market","currency","updatedAt","brief","methodology","winnerId","products","rejected","sources","limitations"}
PRODUCT_FIELDS={"id","brand","name","modelNumber","segment","capacity","availability","price","score","reviews","warranty","strengths","caveats","verdict","priceVerdict","sourceIds"}
SOURCE_FIELDS={"id","url","publisher","type","collectedAt","supports","quality"}

def require(value,fields,label,errors):
    if not isinstance(value,dict): errors.append(f"{label} must be an object"); return
    missing=sorted(fields-value.keys())
    if missing: errors.append(f"{label} missing: {', '.join(missing)}")

def validate(report):
    errors=[]; require(report,ROOT_FIELDS,"report",errors)
    if errors:return errors
    if report["schemaVersion"]!=1:errors.append("schemaVersion must be 1")
    if report["status"] not in {"prototype","verified"}:errors.append("status must be prototype or verified")
    products=report["products"] if isinstance(report["products"],list) else []
    sources=report["sources"] if isinstance(report["sources"],list) else []
    if not products:errors.append("products must be a non-empty array")
    if not isinstance(report["sources"],list):errors.append("sources must be an array")
    for i,item in enumerate(products):require(item,PRODUCT_FIELDS,f"products[{i}]",errors)
    for i,item in enumerate(sources):require(item,SOURCE_FIELDS,f"sources[{i}]",errors)
    product_ids={item.get("id") for item in products if isinstance(item,dict)}
    source_ids={item.get("id") for item in sources if isinstance(item,dict)}
    if report["winnerId"] not in product_ids:errors.append("winnerId must reference a product")
    weights=report.get("methodology",{}).get("weights",{})
    if not isinstance(weights,dict) or not all(isinstance(v,(int,float)) for v in weights.values()) or sum(weights.values())!=100:errors.append("methodology.weights must be numeric values totaling 100")
    for i,item in enumerate(products):
        for source_id in item.get("sourceIds",[]):
            if source_id not in source_ids:errors.append(f"products[{i}] references unknown source {source_id}")
    return errors

def main():
    if len(sys.argv)!=2:raise SystemExit("usage: validate_report.py REPORT.json")
    path=Path(sys.argv[1])
    try:report=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:raise SystemExit(f"invalid report: {exc}")
    errors=validate(report)
    if errors:
        print("Report validation failed:")
        for error in errors:print(f"- {error}")
        raise SystemExit(1)
    print(f"Valid report: {path}")

if __name__=="__main__":main()
