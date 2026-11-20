// Test fixture containing intentional vulnerable Node/Next/Nest/Express patterns

import { exec } from 'node:child_process';

// 1. Command Injection
function runPing(host: string) {
  exec('ping -c 1 ' + host);
}

// 2. Code Injection via eval
function runCalc(expr: string) {
  return eval(expr);
}

// 3. Dangerous innerHTML in React
export function UnsafeView({ content }: { content: string }) {
  return <div dangerouslySetInnerHTML={{ __html: content }} />;
}

// 4. Missing whitelist in NestJS ValidationPipe
const pipe = new ValidationPipe({ transform: true });

// 5. Express Open Redirect
app.get('/redirect', (req, res) => {
  res.redirect(req.query.target);
});

// 6. Express Path Traversal in sendFile
app.get('/download', (req, res) => {
  res.sendFile(req.query.doc);
});
