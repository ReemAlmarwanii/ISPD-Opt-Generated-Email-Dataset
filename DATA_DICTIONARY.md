
# Data Dictionary

| Field | Meaning |
|---|---|
| `record_id` | Stable benchmark record identifier. |
| `text` | Exact classifier input retained from the verified benchmark. |
| `subject`, `body` | Structured subject and body fields where available. |
| `authorship` | Authorship axis; `ai` for every released row. |
| `intent` | Legitimate or phishing intent. |
| `class_label` | `GL` for generated legitimate or `GP` for generated phishing. |
| `generator`, `generator_family`, `model_name` | Generator provenance recorded during construction. |
| `source` | Controlled-generation source category. |
| `scenario`, `difficulty` | Scenario and verified difficulty metadata; unverified Gemini difficulty remains `not_verified`. |
| `pair_id`, `cue_plan_id`, `prompt_id` | Construction-family identifiers used in paired and prompt-family diagnostics. |
| `batch_id`, `run_id`, `generation_date` | Controlled-generation batch/run provenance. |
| `generation_method`, `prompt_version` | Generation workflow metadata. |
| `link_presence`, `urgency_level`, `authority_tone`, `attachment_reference`, `length_band` | Construction controls and descriptive metadata; not operational classifier inputs. |
| `text_sha256` | SHA-256 of the exact UTF-8 `text` value. |
| `post_edit_applied`, `post_editor`, `post_edit_date`, `post_edit_reason`, `original_text_sha256` | Quality-control provenance for the limited post-edited subset. |

The internal `_source_file` field is deliberately excluded because it is unnecessary for reproducibility and may reveal local construction paths. No column contains third-party human-email text.
