import report from "./reports/washing-machines-under-20000.json";

export const researchReport=report;

export type Product={id:string;name:string;model:string;icon:string;price:number;historicalLow:number|null;score:number;verdict:string;confidence:"High"|"Medium"|"Low";rating:number|null;reviewCount:number|null;sellers:number;positiveSignal:string;caveat:string;priceVerdict:string;priceVerdictTone:"good"|"fair"|"wait"};
export type ComparisonReport={updatedAt:string;winnerId:string;products:Product[]};

const tone=(verdict:string):Product["priceVerdictTone"]=>verdict.toLowerCase().includes("wait")?"wait":verdict.toLowerCase().includes("fair")||verdict.toLowerCase().includes("only")?"fair":"good";
const date=new Intl.DateTimeFormat("en-IN",{day:"numeric",month:"short",year:"numeric"}).format(new Date(report.updatedAt));

export const washingMachineComparison:ComparisonReport={
 updatedAt:date,
 winnerId:report.winnerId,
 products:report.products.map(item=>({
  id:item.id,
  name:item.name,
  model:`${item.capacity} · ${item.modelNumber}`,
  icon:"▣",
  price:item.price.current,
  historicalLow:item.price.historicalLow,
  score:item.score.overall,
  verdict:item.verdict,
  confidence:(item.score.confidence[0].toUpperCase()+item.score.confidence.slice(1)) as Product["confidence"],
  rating:item.reviews.displayedRating,
  reviewCount:item.reviews.displayedCount,
  sellers:item.sourceIds.filter(id=>id.includes("croma")||id.includes("flipkart")||id.includes("reliance")).length,
  positiveSignal:item.strengths[0],
  caveat:item.caveats[0],
  priceVerdict:item.priceVerdict,
  priceVerdictTone:tone(item.priceVerdict)
 }))
};
