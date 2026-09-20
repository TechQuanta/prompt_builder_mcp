"""Pure deterministic operations for Prompt Builder clients."""
from __future__ import annotations
from typing import Any

OPTIONS={"provider":("ChatGPT","Claude","Gemini","Universal"),"task":("Write","Plan","Analyze","Code","Research","Image prompt"),"audience":("General","Beginner","Professional","Executive","Children"),"tone":("Clear","Concise","Creative","Technical","Friendly","Persuasive"),"output":("Markdown","JSON","Table","Checklist","Email","Step-by-step"),"depth":("Quick","Balanced","Thorough"),"style":("Zero-shot","Few-shot","Socratic","Chain of thought","Role-based"),"language":("English","Hindi","Spanish","French","German")}
SLIDERS=("creativity","detail","structure")
def get_prompt_schema()->dict[str,Any]: return {"schema_version":"1.0","type":"prompt_brief","required":["user_prompt"],"properties":{"user_prompt":{"type":"string","description":"The user's only free-text input."},**{k:{"type":"string","enum":list(v),"optional":True} for k,v in OPTIONS.items()},"constraints":{"type":"array","items":{"type":"string"},"optional":True},**{k:{"type":"integer","minimum":0,"maximum":100,"optional":True} for k in SLIDERS}}}
def validate_prompt_brief(brief:dict[str,Any])->dict[str,Any]:
 if not isinstance(brief,dict):raise ValueError("brief must be a JSON object.")
 missing=[] if isinstance(brief.get("user_prompt"),str) and brief["user_prompt"].strip() else ["user_prompt"]
 for k,allowed in OPTIONS.items():
  if k in brief and brief[k] not in allowed:raise ValueError(f"{k} must be one of: {', '.join(allowed)}.")
 for k in SLIDERS:
  if k in brief and(not isinstance(brief[k],int) or not 0<=brief[k]<=100):raise ValueError(f"{k} must be an integer from 0 to 100.")
 if "constraints" in brief and(not isinstance(brief["constraints"],list) or not all(isinstance(v,str) for v in brief["constraints"])):raise ValueError("constraints must be a list of strings.")
 return {"valid":not missing,"score":100 if not missing else 0,"missing_fields":missing}
def generate_prompt_variants(brief:dict[str,Any])->dict[str,Any]:
 validation=validate_prompt_brief(brief); selected={k:v for k,v in brief.items() if k!="user_prompt" and v not in(None,"None",[],50)};base="\n".join([f"User request: {brief.get('user_prompt','[Enter your prompt]')}"]+[f"{k.replace('_',' ').title()}: {v if not isinstance(v,list) else '; '.join(v)}" for k,v in selected.items()]);return {"validation":validation,"normalized_brief":{"user_prompt":brief.get("user_prompt"),**selected},"variants":{"focused":f"{base}\n\nGive a direct, useful answer.","detailed":f"{base}\n\nExplain important decisions and cover relevant edge cases.","structured":f"{base}\n\nUse headings, a short summary, and a final checklist."}}
