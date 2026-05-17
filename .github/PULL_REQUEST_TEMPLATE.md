<!-- Use a Conventional Commit-style title, e.g. `feat(nlp): add Arabizi transliterator` -->

## Summary

<!-- What does this PR change and why? Link related issues with `Closes #NNN`. -->

## Type of change

- [ ] feat — new feature
- [ ] fix — bug fix
- [ ] docs — documentation only
- [ ] refactor — code change that neither adds a feature nor fixes a bug
- [ ] perf — performance improvement
- [ ] test — adding or fixing tests
- [ ] build / ci — build system or CI changes
- [ ] chore — other maintenance

## Checklist

- [ ] Tests added / updated and passing locally (`make test`)
- [ ] Lint and types clean (`make lint && make typecheck`)
- [ ] If touching `apps/api/src/helpdesk/nlp/`, NLP evals run and thresholds hold (`make evals`)
- [ ] If introducing UI strings, both `ar.json` and `en.json` are updated
- [ ] If architectural, an ADR is added under `docs/decisions/`
- [ ] If touching personal-data handling or outbound integrations, PDPL impact is described below

## PDPL / data-residency impact

<!-- Delete if not applicable. Otherwise: what personal data is touched, where does it travel, what's the lawful basis. -->

## Screenshots (UI changes only)

| Locale | Before | After |
|---|---|---|
| en |  |  |
| ar |  |  |

## Breaking changes

<!-- Delete if none. Otherwise describe migration steps and add `BREAKING CHANGE:` footer to the commit. -->
