"""FORMAT contracts for v1.3; these do not claim model/game execution."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILLS=ROOT/".agents/skills"
def read(skill,file="workflow.md"):
 return (SKILLS/("gs-"+skill)/"references"/file).read_text(encoding="utf-8")
class V13WorkflowTests(unittest.TestCase):
 def test_canonical_aliases_forward_once(self):
  for old,new in (("help","next-step"),("settings","project-settings"),("changelog","write-changelog")):
   self.assertTrue((SKILLS/("gs-"+new)/"SKILL.md").is_file())
   text=read(old)
   for phrase in ("original arguments unchanged","exactly once","gs-"+new):self.assertIn(phrase,text)
  self.assertIn("studio.py settings",read("project-settings"))
 def test_prototype_routes_and_phases(self):
  text=read("prototype")
  for phrase in ("browser-sketch","Phases 6–9"):self.assertIn(phrase,text)
  for file in ("one-shot-0-door.md","one-shot-1-card.md","one-shot-2-build.md","one-shot-2c-self-check.md","one-shot-3-handover.md","one-shot-4-change.md","one-shot-5-grow.md","one-shot-files.md"):
   self.assertTrue((SKILLS/"gs-prototype/references"/file).is_file());self.assertIn(file,text)
 def test_iteration_grow_ownership(self):
  change=read("prototype","one-shot-4-change.md")
  self.assertIn("hand edits",change);self.assertIn("-- <",change)
  grow=read("prototype","one-shot-5-grow.md")
  for phrase in ("sampled","nothing there is","clean fail","NOT ASSESSED"):self.assertIn(phrase,grow)
 def test_story_scope_and_evidence(self):
  text=read("story-done")
  for phrase in ("### Planned","### Actual","Own calls","CHANGED, not accepted","testable"):self.assertIn(phrase,text)
  self.assertNotIn("Leave out a file that a `Complete` story",text)
  self.assertNotIn("nothing broke",read("dev-story"))
 def test_lenses_and_parent_review(self):
  for skill,lens in (("design-system","lens-qa-lead.md"),("art-bible","lens-technical-artist.md"),("architecture-review","lens-engine.md"),("code-review","lens-engine.md")):
   self.assertTrue((SKILLS/("gs-"+skill)/"references"/lens).is_file())
  for phrase in ("helper-result/1","parent"):self.assertIn(phrase,read("code-review"))
 def test_web_and_cut_execute_only_configured_argv(self):
  web=read("setup-engine","web.md")
  self.assertIn('test: ["npm", "test"]',web)
  self.assertIn("do not write AGENTS.md",web)
  self.assertNotIn("@docs/",web)
  self.assertIn("Never evaluate a TSV",read("cut"))
  self.assertIn("commands.test",read("prototype","one-shot-5-grow.md"))
 def test_role_route_and_checkpoint_contracts(self):
  import tomllib
  role=lambda n:tomllib.loads((ROOT/".codex/agents"/("gs-"+n+".toml")).read_text(encoding="utf-8"))["developer_instructions"]
  prototype=role("prototyper")
  for phrase in ("browser-sketch", "Phases 6–9", "explicit exception", "sampled replay"):
   self.assertIn(phrase,prototype)
  self.assertNotIn("Reliability:",prototype)
  for name in ("art-director","audio-director","economy-designer","game-designer","level-designer","narrative-director","systems-designer","world-builder","writer"):
   for phrase in ("checkpoint --append", "DISABLED", "checkpoint --save", "unbounded history"):
    self.assertIn(phrase,role(name))
 def test_native_guidance_survives_canonical_routes(self):
  self.assertIn("architecture, code/test roots",read("onboard"))
  self.assertIn("Native `skill-lint`",read("skill-test"))
  for phrase in ("studio.py stories", "next.action/path", "BLOCKED/REVIEW STATUS"):
   self.assertIn(phrase,read("sprint-status"))
  self.assertNotIn("runs on the session's model and not this skill's",read("start"))
 def test_web_test_setup_documents_native_scaffold_and_separate_ci(self):
  for name in ("2-plan.md", "3-directories.md", "4-ci.md"):
   text=read("test-setup",name)
   self.assertNotIn("test-scaffold.sh",text,name)
   self.assertIn("SKIPPED",text,name)
  ci=read("test-setup","4-ci.md").split("### Web",1)[1]
  self.assertIn("separate",ci)
  self.assertIn("authorized",ci)
 def test_documented_web_scaffold_commands_match_actual_json_and_writes(self):
  import json, re, shlex, subprocess, sys, tempfile
  web=read("test-setup","3-directories.md").split("#### Web",1)[1]
  commands=re.findall(r"^python \.game-studio/runtime/studio\.py test-scaffold web --root <project-root>.*$",web,re.M)
  self.assertEqual(len(commands),2,"Web instructions must provide actual preview/apply entry points")
  for custom_root in (None,"qa/web"):
   with self.subTest(test_root=custom_root), tempfile.TemporaryDirectory() as folder:
    root=Path(folder)
    config='engine:\n  name: Web\n  version: "8.3.4"\n'
    if custom_root:
     config+='  test_root: '+custom_root+'\n'
     (root/custom_root).mkdir(parents=True)
    (root/"project.yaml").write_text(config,encoding="utf-8")
    prefix=custom_root or "tests"
    expected={prefix+"/README.md",prefix+"/unit/.gitkeep",prefix+"/integration/.gitkeep",prefix+"/smoke/critical-paths.md","production/qa/evidence/.gitkeep","playwright.config.ts"}
    def invoke(command):
     argv=shlex.split(command)
     argv[0]=sys.executable
     argv[1]=str(ROOT/argv[1])
     argv[argv.index("<project-root>")]=str(root)
     result=subprocess.run(argv,cwd=root,text=True,encoding="utf-8",capture_output=True)
     self.assertEqual(result.returncode,0,result.stderr+result.stdout)
     return json.loads(result.stdout)
    for command,status in zip(commands,("WOULD_CREATE","CREATED")):
     result=invoke(command)
     rows={row["path"]:row for row in result["files"]}
     self.assertEqual({path for path,row in rows.items() if row["status"]==status},expected)
     self.assertEqual(rows[".github/workflows/tests.yml"]["status"],"SKIPPED")
     self.assertIn("ci_adapter",{need["id"] for need in result["needs"]})
     actual={p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}-{"project.yaml"}
     self.assertEqual(actual,set() if status=="WOULD_CREATE" else expected)
    existing=root/prefix/"README.md"
    existing.write_text("User-owned test instructions\n",encoding="utf-8")
    again=invoke(commands[1])
    self.assertEqual(existing.read_text(encoding="utf-8"),"User-owned test instructions\n")
    self.assertTrue(all(row["status"] in {"EXISTS","SKIPPED"} for row in again["files"]))
    self.assertFalse((root/".github/workflows/tests.yml").exists())
 def test_code_review_failed_helper_does_not_erase_completed_parent_assessment(self):
  text=read("code-review")
  phase_seven=text.split("## Phase 7:",1)[1].split("## Phase 8:",1)[0]
  phase_eight=text.split("## Phase 8:",1)[1].split("## Phase 9:",1)[0]
  for phrase in ("parent fallback", "same evidence fields", "NOT ASSESSED"):
   self.assertIn(phrase,phase_seven)
  for phrase in ("completed parent assessment", "technical verdict", "Independence", "no independent sign-off"):
   self.assertIn(phrase,phase_eight)
  self.assertNotIn("result that was empty or malformed — or any report section",phase_eight)
  checks=(ROOT/".game-studio/resources/testing/skills/code-review.md").read_text(encoding="utf-8")
  for phrase in ("malformed helper", "completed parent assessment", "incomplete parent", "CHANGES REQUIRED", "independence"):
   self.assertIn(phrase,checks)
 def test_cut_story_guard_precedes_progress_and_honors_scope_restore(self):
  text=read("dev-story")
  gate=text.split("## Phase 2:",1)[1].split("## Phase 3:",1)[0]
  for phrase in ("selected story", "cut by /cut", "cut by $gs-cut", "all workflow tiers", "no implementation", "existing scope authorization", "re-read", "Ready"):
   self.assertIn(phrase,gate)
  self.assertIn("cut status remains",text.split("## Phase 3:",1)[1].split("## Phase 4:",1)[0])
  restore=read("cut").split("## Afterwards",1)[1]
  for phrase in ("existing scope authorization", "re-read", "Ready", "does not delete"):
   self.assertIn(phrase,restore)
 def test_story_done_reports_actual_reviewer_identity(self):
  for document in ("workflow.md","review-gates.md"):
   text=read("story-done",document)
   self.assertIn("parent assessment (lead-programmer lens); no independent review",text)
   self.assertIn("actual participant ID",text)
   self.assertIn("role: lead-programmer",text)
   self.assertNotIn("Reviewed by is `lead-programmer`",text)
   self.assertNotIn("`lead-programmer` when LP-CODE-REVIEW ran",text)
  checks=(ROOT/".game-studio/resources/testing/skills/story-done.md").read_text(encoding="utf-8")
  self.assertIn("parent assessment (lead-programmer lens); no independent review",checks)
  self.assertIn("actual participant ID",checks)
 def test_no_merge_or_retired_host(self):
  for path in SKILLS.rglob("*.md"):
   text=path.read_text(encoding="utf-8")
   self.assertNotRegex(text,r"(?m)^(?:<<<<<<<(?: .*)?|=======|>>>>>>>(?: .*)?)$",str(path))
   for phrase in ("CLAUDE_CODE_EFFORT_LEVEL","${CLAUDE_SKILL_DIR}",".claude/"):self.assertNotIn(phrase,text,str(path))
if __name__=="__main__":unittest.main()
