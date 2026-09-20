"""Deterministic Prompt Refiner schema and variant operations."""
from __future__ import annotations
from typing import Any

BASE_OPTIONS={"task":("Write","Research","Plan","Code","Image prompt"),"tone":("Clear","Concise","Creative","Technical","Friendly","Persuasive"),"output":("Markdown","JSON","Table","Checklist","Email","Step-by-step")}
TYPE_OPTIONS={"Write":{"writing_form":("Email","Post","Article","Script","Ad copy"),"audience":("General","Beginner","Professional","Executive")},"Research":{"research_mode":("Compare","Explain","Evaluate","Summarize"),"source_policy":("Cite sources","Primary sources","No web sources"),"depth":("Quick","Balanced","Thorough")},"Plan":{"planning_horizon":("Today","This week","30 days","Quarter"),"audience":("Individual","Team","Leadership","Customer")},"Code":{"code_language":("Python","TypeScript","JavaScript","SQL","Java"),"code_framework":("React","Next.js","FastAPI","Django","Node.js"),"code_intent":("Write","Debug","Review","Refactor","Explain")},"Image prompt":{"visual_style":("Photorealistic","Editorial","Illustration","3D render","Minimal"),"aspect_ratio":("1:1","4:5","16:9","9:16"),"lighting":("Natural","Studio","Cinematic","Soft")}}
ALL_OPTIONS={**BASE_OPTIONS}
for _group in TYPE_OPTIONS.values():
 for _key,_values in _group.items(): ALL_OPTIONS[_key]=tuple(dict.fromkeys((*ALL_OPTIONS.get(_key,()),*_values)))

def get_prompt_schema()->dict[str,Any]: return {"schema_version":"1.1","type":"prompt_refinement","required":["user_prompt"],"properties":{"user_prompt":{"type":"string","description":"The only free-text input."},**{k:{"type":"string","enum":list(v),"optional":True} for k,v in ALL_OPTIONS.items()}},"control_groups":TYPE_OPTIONS}
def validate_prompt_brief(brief:dict[str,Any])->dict[str,Any]:
 if not isinstance(brief,dict):raise ValueError("brief must be a JSON object.")
 missing=[] if isinstance(brief.get("user_prompt"),str) and brief["user_prompt"].strip() else ["user_prompt"]
 task=brief.get("task")
 for key,value in brief.items():
  if key in ALL_OPTIONS and value not in ALL_OPTIONS[key]:raise ValueError(f"{key} has an unsupported value: {value!r}.")
 specific_keys=set().union(*(set(group) for group in TYPE_OPTIONS.values()))
 invalid=specific_keys.intersection(brief)-set(TYPE_OPTIONS.get(task,{}))
 if invalid:raise ValueError(f"{', '.join(sorted(invalid))} is not available for task {task!r}.")
 return {"valid":not missing,"score":100 if not missing else 0,"missing_fields":missing}
def generate_prompt_variants(brief:dict[str,Any])->dict[str,Any]:
 validation=validate_prompt_brief(brief); selected={k:v for k,v in brief.items() if k!="user_prompt" and v not in(None,"None",[],50)};base="\n".join([f"User request: {brief.get('user_prompt','[Enter your prompt]')}"]+[f"{k.replace('_',' ').title()}: {v}" for k,v in selected.items()]);return {"validation":validation,"normalized_brief":{"user_prompt":brief.get("user_prompt"),**selected},"variants":{"focused":f"{base}\n\nGive a direct, useful answer.","detailed":f"{base}\n\nExplain important decisions and cover relevant edge cases.","structured":f"{base}\n\nUse clear headings, a short summary, and a final checklist."}}
