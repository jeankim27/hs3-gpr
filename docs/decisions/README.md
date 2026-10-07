# Decision records

One short file per decision that changes the design. They are the project's memory: a year from
now, nobody will remember why we picked 20 MHz, but this folder will.

- **Trade study** (`q1-baseline/2-trades/TS-*.md`) = how we compared the options. Long, with analysis.
- **Decision record** (this folder, `DR-*.md`) = what we decided and why. Short, permanent.

## How to write one

1. Copy [`DR-000-template.md`](DR-000-template.md) to `DR-00X-short-name.md` (next free number).
2. Fill it in; set **Status: Proposed**; open a pull request.
3. Discuss in the PR. When the team agrees, set **Status: Accepted** and merge.
4. Update the register: affected variables get `status: frozen` (or `derived`) and `source: DR-00X`.
5. Never edit an accepted record's decision. If it changes, write a new DR that **supersedes** it.

## Index

| ID | Decision | Status |
|---|---|---|
| [DR-001](DR-001-center-frequency.md) | Center frequency and bandwidth | Proposed |
