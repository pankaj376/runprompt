# runprompt

A single-file Python script for running [Dotprompt](https://google.github.io/dotprompt/) files.

[Dotprompt](https://google.github.io/dotprompt/) is an prompt template format for LLMs where a `.prompt` file contains the prompt and metadata (model, schema, config) in a single file.

[Quick start](#quick-start) | [Examples](#examples) | [Configuration](#configuration) | [Providers](#providers) | [Caching](#caching) | [Spec compliance](#spec-compliance)

## Quick start

```bash
curl -O https://raw.githubusercontent.com/chr15m/runprompt/main/runprompt
chmod +x runprompt
```

Create `hello.prompt`:

```handlebars
---
model: anthropic/claude-sonnet-4-20250514
---
Say hello to {{name}}!
```

Run it:

```bash
export OPENAI_API_KEY="your-key"
echo '{"name": "World"}' | ./runprompt hello.prompt
```

(You can get an OpenAI key from here: <https://platform.openai.com/api-keys>)

## Examples

In addition to the following, see the [tests folder](tests/) for more example `.prompt` files.

### Basic prompt with stdin

```handlebars
---
model: anthropic/claude-sonnet-4-20250514
---
Summarize this text: {{STDIN}}
```

```bash
cat article.txt | ./runprompt summarize.prompt
```

The special `{{STDIN}}` variable always contains the raw stdin as a string.

### Structured JSON output

Extract structured data using an output schema:

```handlebars
---
model: anthropic/claude-sonnet-4-20250514
input:
  schema:
    text: string
output:
  format: json
  schema:
    name?: string, the person's name
    age?: number, the person's age
    occupation?: string, the person's job
---
Extract info from: {{text}}
```

```bash
echo "John is a 30 year old teacher" | ./runprompt extract.prompt
# {"name": "John", "age": 30, "occupation": "teacher"}
```

Schema uses [Picoschema](https://google.github.io/dotprompt/reference/picoschema/) format. Fields ending with `?` are optional. The format is `field: type, description`.

### Chaining prompts

Pipe structured output between prompts:

```bash
echo "John is 30" | ./runprompt extract.prompt | ./runprompt generate-bio.prompt
```

The JSON output from the first prompt becomes template variables in the second.

### Executable prompt files

Make `.prompt` files directly executable with a shebang:

```handlebars
#!/usr/bin/env runprompt
model: anthropic/claude-sonnet-4-20250514
---
Hello, I'm {{name}}!
```

```bash
chmod +x hello.prompt
echo '{"name": "World"}' | ./hello.prompt
```

Note: `runprompt` must be in your PATH, or use a relative/absolute path in the shebang (e.g. `#!/usr/bin/env ./runprompt`).

### CLI overrides

Override frontmatter values from the command line:

```bash
./runprompt --model anthropic/claude-haiku-4-20250514 hello.prompt
./runprompt --output.format json extract.prompt
```

Note: CLI overrides set frontmatter values (model, config, output format, etc.), not template variables. To pass template variables, use stdin:

```bash
echo '{"name": "Alice"}' | ./runprompt hello.prompt
```

## Template syntax

Templates use [Handlebars syntax](https://google.github.io/dotprompt/reference/template/). Supported features:

- Variable interpolation: `{{variableName}}`, `{{object.property}}`
- Comments: `{{! this is a comment }}`
- Iteration: `{{#each items}}...{{/each}}` with `@index`, `@first`, `@last`, `@key`
- Sections: `{{#key}}...{{/key}}` (renders if truthy)
- Inverted sections: `{{^key}}...{{/key}}` (renders if falsy)

## Configuration

### Environment variables

Set API keys for your providers:

```bash
export ANTHROPIC_API_KEY="..."  # https://console.anthropic.com/settings/keys
export OPENAI_API_KEY="..."     # https://platform.openai.com/api-keys
export GOOGLE_API_KEY="..."     # https://aistudio.google.com/app/apikey
export OPENROUTER_API_KEY="..." # https://openrouter.ai/settings/keys
```

### Custom endpoint (Ollama, etc.)

Use `OPENAI_BASE_URL` or `BASE_URL` to point at any OpenAI-compatible endpoint:

```bash
# Use Ollama
export OPENAI_BASE_URL="http://localhost:11434/v1"
./runprompt hello.prompt

# Or via CLI flag
./runprompt --base-url http://localhost:11434/v1 hello.prompt
```

When a custom base URL is set, the provider prefix in the model string is ignored and the OpenAI-compatible API format is used.

### RUNPROMPT_* overrides

Override any frontmatter value via environment variables prefixed with `RUNPROMPT_`:

```bash
export RUNPROMPT_MODEL="anthropic/claude-haiku-4-20250514"
./runprompt hello.prompt
```

This is useful for setting defaults across multiple prompt runs.

### Verbose mode

Use `-v` to see request/response details:

```bash
./runprompt -v hello.prompt
```

## Providers

Models are specified as `provider/model-name`:

| Provider | Model format | API key |
|----------|--------------|---------|
| Anthropic | `anthropic/claude-sonnet-4-20250514` | [Get key](https://console.anthropic.com/settings/keys) |
| OpenAI | `openai/gpt-4o` | [Get key](https://platform.openai.com/api-keys) |
| Google AI | `googleai/gemini-1.5-pro` | [Get key](https://aistudio.google.com/app/apikey) |
| OpenRouter | `openrouter/anthropic/claude-sonnet-4-20250514` | [Get key](https://openrouter.ai/settings/keys) |

[OpenRouter](https://openrouter.ai) provides access to models from many providers (Anthropic, Google, Meta, etc.) through a single API key.

## Caching

Enable response caching to avoid redundant API calls during development:

```bash
# Enable caching with -c or --cache
./runprompt --cache hello.prompt

# Second run with same input uses cached response
./runprompt --cache hello.prompt
```

You can also enable the cache across a whole pipeline with the env var:

```bash
export RUNPROMPT_CACHE=1; echo "..." | ./runprompt a.prompt | ./runprompt b.prompt
```

Cached responses are stored in `~/.cache/runprompt/` (or `$XDG_CACHE_HOME/runprompt/`), based on the inputs applied to the template and frontmatter.

See `--help` for more information.

## Spec compliance

This is a minimal implementation of the [Dotprompt specification](https://google.github.io/dotprompt/). Not yet supported:

- Multi-message prompts (`{{role}}`, `{{history}}`)
- Conditionals (`{{#if}}`, `{{#unless}}`, `{{else}}`)
- Helpers (`{{json}}`, `{{media}}`, `{{section}}`)
- Model config (`temperature`, `maxOutputTokens`, etc.)
- Partials (`{{>partialName}}`)
- Nested Picoschema (objects, arrays of objects, enums)

See [TODO.md](TODO.md) for the full roadmap.
