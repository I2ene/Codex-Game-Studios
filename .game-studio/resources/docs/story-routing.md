# Story JSON and routing

Explicitly run `python .game-studio/runtime/studio.py stories --root <project-root>`.
Nothing is injected before skill loading. Consume count, complete, counts, stories,
unfinished and next. Each row has path, status as written and category. Plain/bold/
bold-colon/quote/list Status forms are supported. Leading Complete/Done words count;
Done. is complete, Not Done and Completed are not.

Rows sort IN_REVIEW → IN_PROGRESS → TODO (Ready/Not Started) → BLOCKED → OTHER/
NO_STATUS → COMPLETE, by filename inside a group. next.action is story-done or
dev-story with next.path/skill; otherwise NO STORIES, COMPLETE, BLOCKED or REVIEW
STATUS. This is a status-derived route, not a closure/quality verdict.

At minimal/no sprint, help and sprint-status use the same next/count contract.
story-done reruns it after an authorized status update. Never mark a blocked/unknown
unfinished set complete. Read blockers and recommend the needed action. No stories
requires a real brief before create-stories. All complete offers playtest/add stories/
raise rigor when appropriate; unavailable game/build evidence remains unassessed.
With a sprint, preserve sprint priority/dependency/cadence analysis rather than
substituting filename order for the sprint plan.
