# PROMPT: UNICODE_TEST

## Goal

Test international characters: cafe, naive, resume
Japanese: 日本語テスト
Chinese: 中文测试
Korean: 한국어 테스트
Emojis in content: 🎉 🚀 ✨ 💻

## Quality Tier

**Tier:** production

## Tasks (Prioritized)

### 🔴 RISKY

- [ ] Task with emojis 🎯 and special chars: <>&"'
- [x] Completed task with unicode: cafe resume

### 🟡 CORE

- [ ] @python-developer: Handle i18n correctly
- [ ] Process UTF-8 content: 日本語

### 🟢 POLISH

- [ ] Add translations 🌍

## Exit Criteria

- [ ] Unicode handling works: `python -c "print('日本語')"`

## Progress

**Status:** IN_PROGRESS

## Notes

Special characters test: <script>alert('xss')</script>
Path characters: C:\Users\Test and /home/test
