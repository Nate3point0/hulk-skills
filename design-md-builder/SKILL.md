---
name: design-md-builder
description: >
  Extracts or generates a complete DESIGN.md design system document from any
  reference: screenshot, URL, Figma link, brand description, or existing
  style guide. Output is a reusable token file for consistent artifacts across
  all projects. Saves to BrainVault and can be promoted to a SKILL.md.
triggers:
  - DESIGN.md
  - design system
  - design tokens
  - extract design
  - brand tokens
  - color palette
  - typography scale
  - style guide
  - extract brand
  - design language
version: "1.0"
author: Ceepeezee
---

# design-md-builder

Generates a production-ready DESIGN.md from any input. Used at the start of
every project to lock tokens before building artifacts.

---

## Step 1 — Detect Input Mode

| Input provided | Mode |
|----------------|------|
| Screenshot / image | Extract from visual |
| URL | Fetch and extract |
| Figma link | Extract from Figma description |
| Brand description in text | Generate from brief |
| Existing CSS / style sheet | Parse tokens |
| "Start fresh" / no reference | Interview mode |

---

## Step 2 — Interview (if no reference)

Ask once, all together:

```
To build your DESIGN.md I need:
1. Brand colors — even rough: "dark navy, gold accent, white background"
2. Vibe / tone — pick one: minimal · bold · playful · corporate · techy · warm · luxury
3. Typography feel — pick one: clean sans · humanist sans · modern serif · monospace · mixed
4. One reference site or brand you like (or "derive from [niche/product]")
5. Primary use case — landing page · dashboard · calculator · quiz · all of the above
```

---

## Step 3 — Extraction Prompt (for reference inputs)

```
Analyze this [screenshot / URL / Figma / CSS] and extract a complete DESIGN.md.

1. COLOR TOKENS
   - Primary, Secondary, Accent, Background, Surface, Text, Muted, Error, Success
   - Provide HEX codes. If exact HEX is unavailable, estimate from visual.

2. TYPOGRAPHY SCALE
   - Font families (heading + body; note if system font)
   - Size scale: H1 · H2 · H3 · H4 · Body · Small · Caption
   - Weights and line heights for each

3. SPACING SCALE
   - Identify base unit (4px or 8px typical)
   - List full scale: base × 1 through × 16

4. COMPONENT INVENTORY
   - Buttons: variants (primary, secondary, ghost, destructive), sizes, border radius
   - Cards: background, border, shadow, radius, padding
   - Inputs: height, border, focus style, error style
   - Navigation: type (top bar / sidebar / mobile drawer), style
   - Hero variants: type-only · split · centered-screenshot · video-bg

5. LAYOUT RULES
   - Max content width
   - Column grid and gutter
   - Responsive breakpoints (mobile · tablet · desktop)
   - Section vertical padding (desktop + mobile)

6. ICON SYSTEM
   - Library if identifiable (Lucide preferred)
   - Style: filled vs outline
   - Sizes: inline · standalone · feature

7. DENSITY MODES
   - Compact · Comfortable · Spacious definitions (spacing multipliers)

8. ACCESSIBILITY BASELINE
   - Contrast ratios where calculable (WCAG AA = 4.5:1 text, 3:1 UI)
   - Keyboard navigation notes
   - Touch target minimums

Output as a clean markdown document starting with "# DESIGN.md — [Project Name]".
```

---

## Step 4 — DESIGN.md Output Template

```markdown
# DESIGN.md — [Project Name]
Generated: [date] | Niche: [niche] | Tone: [tone]

---

## Color Tokens
| Token | HEX | Usage |
|-------|-----|-------|
| --color-primary    | #XXXXXX | CTAs, headings, active links |
| --color-secondary  | #XXXXXX | Secondary actions, accents |
| --color-accent     | #XXXXXX | Highlights, badges, tags |
| --color-bg         | #XXXXXX | Page background |
| --color-surface    | #XXXXXX | Cards, panels, modals |
| --color-text       | #XXXXXX | Body copy, labels |
| --color-muted      | #XXXXXX | Captions, placeholders, dividers |
| --color-error      | #EF4444 | Error states |
| --color-success    | #22C55E | Success states |

## Typography Scale
| Role    | Family | Size       | Weight | Line Height |
|---------|--------|------------|--------|-------------|
| H1      |        | 48px/3rem  | 700    | 1.1         |
| H2      |        | 36px/2.25rem | 600  | 1.2         |
| H3      |        | 24px/1.5rem  | 600  | 1.3         |
| H4      |        | 20px/1.25rem | 500  | 1.4         |
| Body    |        | 16px/1rem  | 400    | 1.6         |
| Small   |        | 14px/.875rem | 400  | 1.5         |
| Caption |        | 12px/.75rem  | 400  | 1.4         |

## Spacing Scale (base: 4px)
| Step | Value |
|------|-------|
| 1    | 4px   |
| 2    | 8px   |
| 3    | 12px  |
| 4    | 16px  |
| 6    | 24px  |
| 8    | 32px  |
| 12   | 48px  |
| 16   | 64px  |
| 24   | 96px  |
| 32   | 128px |

## Component Rules

### Buttons
- Primary: --color-primary bg · white text · 8px radius · 16px/32px padding
- Secondary: transparent bg · --color-primary border + text
- Ghost: no border · --color-primary text · 10% opacity hover bg
- Sizes: sm(12px/28px) · md(16px/40px) · lg(18px/52px)

### Cards
- Background: --color-surface
- Border: 1px solid rgba(0,0,0,0.08)
- Radius: 12px
- Shadow: 0 2px 8px rgba(0,0,0,0.06)
- Padding: comfortable 24px · compact 16px · spacious 32px

### Inputs
- Height: 44px (mobile tap target minimum)
- Border: 1px solid --color-muted
- Focus: 2px solid --color-primary outline, offset 2px
- Error: 1px solid --color-error · inline message below field
- Label: above input · --color-text · 14px · 500 weight

### Hero Variants
- type-only: centered text + CTA, no image
- split-image: 50/50 text left · image right
- centered-screenshot: text + product screenshot centered below
- video-bg: full-bleed video · text overlay with scrim

## Density Modes
- compact:     spacing × 0.75
- comfortable: spacing × 1.0  ← default
- spacious:    spacing × 1.25

## Icon System
- Library: Lucide icons only (no external image URLs)
- Style: [outline / filled]
- Sizes: 20px inline · 24px standalone · 32px feature · 48px hero
- Fallback: emoji if Lucide lacks the icon

## Layout
- Max width: 1200px
- Grid: 12-column · 24px gutter
- Breakpoints: mobile <768px · tablet 768–1024px · desktop >1024px
- Section padding: 80px top/bottom desktop · 48px mobile

## Accessibility Baseline
- Text contrast: 4.5:1 minimum (WCAG AA)
- UI element contrast: 3:1 minimum
- Touch targets: 44×44px minimum
- Keyboard: all interactive elements focusable, visible focus ring
- Dynamic content: aria-live="polite" regions
- Forms: label + aria-describedby for error messages
- Images: descriptive alt text required
```

---

## Step 5 — Post-Generation Actions

After outputting the DESIGN.md, always:

1. **Save instruction** — tell the user:
   > "Save this to BrainVault at `/design-systems/[niche]/DESIGN.md`. Tag: `#design-system #[niche]`."

2. **Session reference** — tell the user:
   > "Start every artifact session with: *'Reference DESIGN.md — do not deviate from these tokens unless I ask.'*"

3. **Skillify offer** — ask:
   > "Want me to wrap this as a SKILL.md so it loads automatically for this niche?"

4. **Accessibility check offer** — ask:
   > "Want me to run a contrast audit on this palette against WCAG AA before we build?"

---

## Accessibility Audit (run on request)

```
Audit this palette for WCAG AA:
Primary: [HEX] · Secondary: [HEX] · BG: [HEX] · Text: [HEX] · Accent: [HEX]

For every realistic text-on-background pair:
1. Calculate contrast ratio
2. State WCAG requirement (4.5:1 text · 3:1 UI)
3. Mark pass / fail
4. For fails: suggest minimum HEX adjustment preserving brand feel
5. Output: fixed palette + before/after ratios + safe-combination matrix
```
