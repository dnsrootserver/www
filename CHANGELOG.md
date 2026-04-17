# Changelog

## 1.1.0 (2026-04-18)

### Features
- **73 skills** across 4 categories (28 free + 45 premium)
- **18 built-in tools** (added: regex_extract, json_parse, loop, schedule, retry, notify, download, compress, template)
- **Bilingual support** — Full English and Chinese descriptions and triggers
- **Premium skill packs**:
  - DevOps Pack (15 skills): Docker, K8s, server monitor, log analysis, deploy, SSL, port scan, backup, CI/CD, infra audit, Nginx, MySQL, Redis, disk, process
  - Data Pack (15 skills): CSV, Excel, JSON, API, scraper, viz, SQL, clean, merge, convert, regex, validate, mock, schema, sample
  - Social Pack (15 skills): Twitter, Reddit, RSS, HN, GitHub, arXiv, PH, YouTube, LinkedIn, Medium, Dev.to, SO, news, blog, analytics
- **12 new free skills**: hash-generator, json-formatter, uuid-generator, base64-encode, url-shortener, ip-lookup, dns-lookup, ping-test, port-check, whois-lookup, ssl-check, cron-helper, password-gen, text-stats, lorem-ipsum, color-picker, qr-generator, ascii-art, morse-code, pig-latin, word-counter
- Category and tag system for skills
- Premium flag for paid skills
- Product Hunt launch materials
- Gumroad product page template

### Improvements
- Upgraded Jinja2 template engine
- Better error handling in tools
- Rich terminal UI with icons
- Interactive chat mode with help/skills/tools commands
- JSON output mode for automation

## 1.0.0 (2026-04-18)

### Features
- Core YAML-based skill engine
- 10 built-in tools
- 8 built-in skills
- CLI with init, run, chat, list, validate, doctor commands
- Jinja2 template support
- Regex trigger matching
- Rich terminal UI
