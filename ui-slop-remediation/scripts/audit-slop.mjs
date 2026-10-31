#!/usr/bin/env node

/**
 * UI Slop Remediation - Automated Static Code Scanner
 * 
 * Audits HTML, JSX, TSX, Vue, Svelte, and CSS files for AI slop anti-patterns
 * and calculates a quantitative Slop Index (0-100).
 *
 * Usage:
 *   node audit-slop.mjs <file-or-directory> [--json]
 */

import { readFileSync, statSync, readdirSync } from "node:fs";
import { resolve, extname, join } from "node:path";

const ARGS = process.argv.slice(2);
const TARGET = ARGS.find(arg => !arg.startsWith("--"));
const IS_JSON = ARGS.includes("--json");

if (!TARGET) {
  console.log(`
UI Slop Remediation - Static Code Scanner
Usage: node audit-slop.mjs <path-to-file-or-directory> [--json]

Audits source files for AI slop tells:
  - Purple/violet gradients & text clips
  - Glowing colored shadows & neon borders
  - Emojis in interface copy & labels
  - Arbitrary pixel nudge classes (mt-[13px])
  - Hype copy keywords (supercharge, seamless, AI-powered)
  - Missing tabular numbers on financial data
`);
  process.exit(1);
}

// Slop rules definitions
const RULES = [
  {
    id: "SURF-01",
    category: "Surface & Effects",
    weight: 12,
    name: "Hue Gradients on Surfaces",
    description: "Vivid multi-hue gradients on backgrounds or cards (e.g. purple to blue).",
    regex: /(?:bg-gradient-to-[a-z]+|linear-gradient\([^)]*(?:#8b5cf6|#a855f7|#6366f1|purple|violet|indigo))/i,
    recommendation: "Use a single neutral surface ramp tinted toward your product's world."
  },
  {
    id: "SURF-02",
    category: "Surface & Effects",
    weight: 10,
    name: "Gradient Text Clip",
    description: "Text with gradient clipping (bg-clip-text text-transparent).",
    regex: /(?:bg-clip-text\s+text-transparent|text-transparent\s+bg-clip-text|-webkit-background-clip:\s*text)/i,
    recommendation: "Use solid high-contrast primary text color."
  },
  {
    id: "SURF-03",
    category: "Surface & Effects",
    weight: 12,
    name: "Colored Glow Shadows",
    description: "Neon or colored drop shadows radiating from buttons or containers.",
    regex: /(?:shadow-\[(?:0_0_|0px_0px_)[^\]]*(?:rgba\([^)]*246|rgba\([^)]*99|purple|violet)\]|shadow-purple|shadow-violet|shadow-indigo-[0-9]{3}\/[0-9]{2})/i,
    recommendation: "Replace glows with quiet hairline borders (border-white/[0.08]) or subtle neutral surface steps."
  },
  {
    id: "ICON-01",
    category: "Iconography & Badges",
    weight: 8,
    name: "Emoji in Interface Labels",
    description: "Emojis used as buttons, nav icons, or card decorations.",
    regex: /(?:[✨🚀🔥💡👋💰⚠️📈😬🎉🤖])/u,
    recommendation: "Replace emojis with uniform 16px/18px stroke line icons from Lucide or Heroicons."
  },
  {
    id: "ICON-02",
    category: "Iconography & Badges",
    weight: 6,
    name: "Hype / Sparkle Badge",
    description: "Badges featuring AI sparkles or rocket hype tags.",
    regex: /(?:New\s*✨|PRO\s*✨|Beta\s*🚀|AI-Powered\s*✨)/i,
    recommendation: "Use calm, quiet text labels with an optional 6px solid neutral status dot."
  },
  {
    id: "COPY-01",
    category: "Copywriting",
    weight: 10,
    name: "Hype & Buzzword Copy",
    description: "Generic AI marketing hype verbs and empty superlatives.",
    regex: /\b(supercharge|seamlessly|game-changing|revolutionize|unlock\s+the\s+power|magic\s+of|unleash|hyper-scale)\b/i,
    recommendation: "Replace with plain, factual verbs stating exactly what the tool accomplishes."
  },
  {
    id: "COPY-02",
    category: "Copywriting",
    weight: 5,
    name: "Greeting Headline Cliché",
    description: "Personalized greeting headline with waving hand or exclamation.",
    regex: /(?:Welcome\s+back,\s*[^!\n]+(?:!|👋)|Good\s+morning,\s*[^!\n]+!)/i,
    recommendation: "Name the current page or working context directly (e.g. 'Telemetry Overview', 'October 2026')."
  },
  {
    id: "COPY-03",
    category: "Copywriting",
    weight: 5,
    name: "Exclamation in Interface Text",
    description: "Double exclamation marks or shouting interface copy.",
    regex: /(?:!!|[A-Z][a-z]+!\s*<\/)/,
    recommendation: "Strip exclamation marks from interface buttons, headers, and toasts."
  },
  {
    id: "SPAC-01",
    category: "Spacing & Alignment",
    weight: 8,
    name: "Arbitrary Pixel Spacing",
    description: "Non-standard arbitrary Tailwind spacing classes breaking 4px grid.",
    regex: /(?:m[trblxy]?|p[trblxy]?|gap(?:-[xy])?|h|w)-\[(?:[13579]|11|13|15|17|19|21|23|27|29|31|33|35|37)px\]/i,
    recommendation: "Align all spacing to the standard 4px rhythm (4, 8, 12, 16, 20, 24, 32px)."
  },
  {
    id: "TYPE-01",
    category: "Typography",
    weight: 6,
    name: "Overly Heavy Heading Weight",
    description: "Font weights 800 or 900 used on display headings.",
    regex: /(?:font-extrabold|font-black|font-weight:\s*(?:800|900))/i,
    recommendation: "Use weight 400 or 500 for headings, relying on size and contrast for hierarchy."
  },
  {
    id: "TYPE-02",
    category: "Typography",
    weight: 6,
    name: "Uppercase Tracked Labels",
    description: "All-caps labels with wide tracking applied indiscriminately.",
    regex: /(?:uppercase\s+tracking-(?:wider|widest)|tracking-(?:wider|widest)\s+uppercase)/i,
    recommendation: "Convert to sentence case with standard letter spacing."
  },
  {
    id: "TYPE-03",
    category: "Typography",
    weight: 6,
    name: "Numeric Metric Missing Tabular Figures",
    description: "Monetary or metric data without tabular-nums specification.",
    check: (line) => {
      if (line.includes("tabular-nums") || line.includes("font-mono") || line.includes("\\text")) return null;
      return /(?:(?<!\\)\$[0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})|\b[+-][0-9]+(?:\.[0-9]+)?%)/.exec(line);
    },
    recommendation: "Add 'tabular-nums' (font-variant-numeric: tabular-nums) or 'font-mono' to prevent jitter."
  }
];

const VALID_EXTENSIONS = new Set([".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".css"]);

function collectFiles(targetPath) {
  const stat = statSync(targetPath);
  if (stat.isFile()) {
    return [targetPath];
  }
  if (stat.isDirectory()) {
    const results = [];
    const entries = readdirSync(targetPath, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name.startsWith(".") || entry.name === "node_modules" || entry.name === "dist") continue;
      const fullPath = join(targetPath, entry.name);
      if (entry.isDirectory()) {
        results.push(...collectFiles(fullPath));
      } else if (entry.isFile() && VALID_EXTENSIONS.has(extname(entry.name).toLowerCase())) {
        results.push(fullPath);
      }
    }
    return results;
  }
  return [];
}

function scanFile(filePath) {
  const content = readFileSync(filePath, "utf-8");
  const lines = content.split(/\r?\n/);
  const violations = [];

  lines.forEach((line, index) => {
    const lineNum = index + 1;
    for (const rule of RULES) {
      const match = typeof rule.check === "function" ? rule.check(line) : rule.regex.exec(line);
      if (match) {
        violations.push({
          ruleId: rule.id,
          name: rule.name,
          category: rule.category,
          weight: rule.weight,
          recommendation: rule.recommendation,
          line: lineNum,
          snippet: line.trim().slice(0, 100),
          match: match[0]
        });
      }
    }
  });

  return violations;
}

function computeScore(violations, lineCount) {
  if (violations.length === 0) return 0;
  let totalWeightedViolations = 0;
  for (const v of violations) {
    totalWeightedViolations += v.weight;
  }
  // Normalize based on scale
  const rawScore = Math.min(100, Math.round(totalWeightedViolations * 1.5));
  return rawScore;
}

const files = collectFiles(resolve(TARGET));
if (files.length === 0) {
  console.error(`No supported files (.html, .jsx, .tsx, .vue, .svelte, .css) found in: ${TARGET}`);
  process.exit(1);
}

let allViolations = [];
let totalLines = 0;
const fileResults = [];

for (const file of files) {
  const content = readFileSync(file, "utf-8");
  const lines = content.split(/\r?\n/).length;
  totalLines += lines;
  const violations = scanFile(file);
  allViolations.push(...violations);
  fileResults.push({
    file,
    lines,
    violationCount: violations.length,
    violations
  });
}

const slopIndex = computeScore(allViolations, totalLines);

let triage = "Clean UI (<10)";
if (slopIndex >= 40) triage = "Heavy Slop (>=40) - Full 10-Layer Remediation Required";
else if (slopIndex >= 10) triage = "Light Slop (10-39) - Surgical Redline Polish Required";

if (IS_JSON) {
  console.log(JSON.stringify({
    target: TARGET,
    filesScanned: files.length,
    totalLines,
    slopIndex,
    triage,
    totalViolations: allViolations.length,
    violations: allViolations
  }, null, 2));
  process.exit(0);
}

// Pretty print CLI report
console.log("================================================================================");
console.log(`UI SLOP REMEDIATION AUDIT REPORT`);
console.log("================================================================================");
console.log(`Target:         ${TARGET}`);
console.log(`Files Scanned:  ${files.length} (${totalLines} lines)`);
console.log(`Total Violations: ${allViolations.length}`);
console.log(`SLOP INDEX:     ${slopIndex} / 100`);
console.log(`Triage Status:  ${triage}`);
console.log("--------------------------------------------------------------------------------\n");

if (allViolations.length === 0) {
  console.log("✨ No AI slop anti-patterns detected. This interface exhibits clean digital craft!");
  console.log("================================================================================");
  process.exit(0);
}

// Group violations by category
const byCategory = {};
for (const v of allViolations) {
  if (!byCategory[v.category]) byCategory[v.category] = [];
  byCategory[v.category].push(v);
}

for (const [category, list] of Object.entries(byCategory)) {
  console.log(`[CATEGORY: ${category.toUpperCase()}] (${list.length} violations)`);
  for (const item of list) {
    console.log(`  • [Line ${item.line}] ${item.name} (${item.ruleId})`);
    console.log(`    Matched: "${item.match}"`);
    console.log(`    Snippet: ${item.snippet}`);
    console.log(`    Fix:     ${item.recommendation}\n`);
  }
}

console.log("================================================================================");
console.log("REMEDIATION NEXT STEPS:");
if (slopIndex >= 40) {
  console.log("1. Define the 5-point direction (Product, Character, World, Moments, Signature).");
  console.log("2. Execute all 10 Layers in order (Spacing -> Surface -> Icons -> Copy -> Type).");
  console.log("3. Re-run this audit to verify Slop Index drops under 10.");
} else if (slopIndex >= 10) {
  console.log("1. Perform targeted redline remediation on the specific flagged line numbers above.");
  console.log("2. Preserve existing brand palette and font family.");
} else {
  console.log("1. Slop Index is under 10. Implement minor micro-refinements if requested.");
}
console.log("================================================================================");
