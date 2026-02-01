# AGENTS.md - Vocabulary Notebook Assistant Guidelines

## Project Overview
This is a personal vocabulary notebook project designed to help users learn English words. The assistant helps translate words, provide phonetics and example sentences, generate audio pronunciations using TTS, and record them in VocabularyNotebook.md for later study.

## Commands
Since this is a documentation-based project, there are no traditional build/lint/test commands. However, here are useful operations:

### File Operations
- Create new vocabulary entry: `touch VocabularyNotebook.md` (if doesn't exist)
- View vocabulary: `cat VocabularyNotebook.md`
- Search vocabulary: `grep -i "word" VocabularyNotebook.md`
- Backup vocabulary: `cp VocabularyNotebook.md VocabularyNotebook_backup_$(date +%Y%m%d).md`

### Audio Generation
- Generate TTS audio: `/Users/aserlili/Documents/Codes/PersonalAssistant/tools/TTS/tts.sh "[word]" --output audio/[word].mp3`
- Batch audio generation: Use shell script to process all words
- Audio directory: `audio/` (automatically created if not exists)

### Validation
- Check markdown syntax: Use any markdown linter
- Verify phonetic format: Ensure IPA brackets [] are properly used
- Validate structure: Check each entry follows the prescribed format
- Verify audio files exist: `ls -la audio/`

## Vocabulary Recording Format

### Recommended Format (Table-based with Audio)
```markdown
# Vocabulary Notebook

| Word | Phonetic | Translation | Example Sentences |
|------|----------|-------------|-------------------|
| compatibility | /kəmˌpætəˈbɪləti/ <audio controls><source src="audio/compatibility.mp3" type="audio/mpeg">🔊</audio> | 兼容性, 相容性, 协调性 | The new software has excellent compatibility with older systems. (新软件与旧系统有极佳的兼容性。)<br>Check compatibility before purchasing hardware. (购买硬件前请检查兼容性。)<br>The couple's compatibility was evident in their shared interests. (这对情侣的协调性在他们共同的兴趣中显而易见。) |
| format | /ˈfɔːrmæt/ <audio controls><source src="audio/format.mp3" type="audio/mpeg">🔊</audio> | 格式, 版式, 格局 | Please follow the specified format when submitting your report. (提交报告时请遵循指定格式。)<br>The document is available in digital format. (该文档有数字格式版本。)<br>She changed the format of the presentation to make it more engaging. (她改变了演示文稿的版式使其更具吸引力。) |
```

### Alternative Detailed Format (with Audio)
```markdown
## Word

**Phonetic:** [/ˈfɔːrmæt/]<audio controls><source src="audio/word.mp3" type="audio/mpeg">🔊</audio>

**Definition:** A particular way in which something is arranged or presented

**Part of Speech:** noun

**Example Sentences:**
1. Please follow the specified format when submitting your report.
2. The document is available in both digital and print format.

**Date Added:** 2026-02-01

---
```

### Alternative Detailed Format
```markdown
## Word

**Phonetic:** [/ˈfɔːrmæt/]

**Definition:** A particular way in which something is arranged or presented

**Part of Speech:** noun

**Example Sentences:**
1. Please follow the specified format when submitting your report.
2. The document is available in both digital and print format.

**Date Added:** 2026-02-01

---
```

## Code Style Guidelines

### File Structure
- Main vocabulary file: `VocabularyNotebook.md`
- Backup files: `VocabularyNotebook_backup_YYYYMMDD.md`
- This guide: `AGENTS.md`
- Audio files: `audio/[word].mp3` (TTS generated pronunciations)

### Markdown Formatting
1. Use `##` for word headers (H2 level)
2. Use **bold** for field labels (Phonetic, Definition, etc.)
3. Use IPA brackets `[]` for phonetics
4. Use numbered lists for example sentences
5. Use horizontal rule `---` between entries
6. Use ISO date format `YYYY-MM-DD` for dates

### Content Guidelines
1. **Phonetics:** Always provide IPA transcription in brackets
2. **Translations:** Provide multiple common Chinese translations separated by commas, focusing on most frequently used meanings
3. **Examples:** Maximum 4 example sentences. Each English sentence must include Chinese translation in parentheses. Examples should correspond to different translation meanings provided
4. **Translation Quality:** Provide accurate, natural Chinese translations for both word meanings and example sentences
5. **Example Selection:** Choose examples that demonstrate common usage contexts and key meanings, covering the various translations provided

### Entry Structure Rules
1. Each word starts with `## WordName`
2. Phonetic transcription immediately follows word name
3. All field labels are bolded with colons
4. Example sentences are numbered
5. Date is always included at the end
6. Horizontal rule separates entries

### Writing Style
- Keep definitions under 20 words when possible
- Example sentences should demonstrate common usage
- Use simple, clear language in definitions
- Include context that helps understand word usage
- Avoid overly technical or obscure examples

### Quality Standards
- Verify phonetic accuracy using reliable sources
- Ensure example sentences are grammatically correct
- Check spelling and punctuation
- Maintain consistency in formatting across all entries
- Review for clarity and educational value

## Assistant Interaction Guidelines

### When Adding New Words
1. Always ask user which format they prefer if not specified
2. Provide pronunciation assistance when needed
3. Offer synonyms and antonyms when helpful
4. Include context-specific examples when user mentions usage scenario
5. Suggest related words or word families when beneficial
6. **Generate audio pronunciation**: Always use TTS skill to create audio file for new words
7. **Add audio icon**: Include 🔊 emoji after phonetic transcription for clickable audio playback

### When Searching/Reviewing
1. Use case-insensitive search
2. Group similar words together when helpful
3. Provide quick review summaries when requested
4. Suggest review strategies based on learning patterns

### Error Handling
- If phonetic transcription unavailable, mark as [TBD]
- If unsure about word usage, ask user for context
- If file access issues occur, suggest alternative locations
- Always confirm major changes before implementing

## File Maintenance
- Regular backups recommended
- Consider alphabetizing entries periodically
- Review and update outdated examples
- Remove duplicate entries
- Consider categorizing by difficulty level or topic when collection grows

## Accessibility Considerations
- Use clear, readable formatting
- Provide both US and UK pronunciations when significantly different
- Include context that helps non-native speakers understand usage
- Consider adding difficulty ratings for advanced learners
- **Audio Support**: All words include 🔊 audio icon for pronunciation playback
- **TTS Integration**: Automated audio generation for all vocabulary entries
