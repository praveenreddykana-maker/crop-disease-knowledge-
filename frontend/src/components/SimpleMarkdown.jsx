/**
 * Simple markdown renderer that handles the most common patterns
 * in chat responses (bold, lists, headers, code) without needing
 * external ESM-only packages.
 */
export default function SimpleMarkdown({ children }) {
  if (!children) return null;

  const lines = children.split('\n');
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // H1
    if (line.startsWith('# ')) {
      elements.push(
        <h1 key={i} className="text-lg font-bold text-primary-800 mt-3 mb-1">
          {renderInline(line.slice(2))}
        </h1>
      );
    }
    // H2
    else if (line.startsWith('## ')) {
      elements.push(
        <h2 key={i} className="text-base font-bold text-primary-800 mt-3 mb-1">
          {renderInline(line.slice(3))}
        </h2>
      );
    }
    // H3
    else if (line.startsWith('### ')) {
      elements.push(
        <h3 key={i} className="text-sm font-bold text-primary-800 mt-2 mb-0.5">
          {renderInline(line.slice(4))}
        </h3>
      );
    }
    // Horizontal rule
    else if (line.match(/^---+$/) || line.match(/^\*\*\*+$/)) {
      elements.push(<hr key={i} className="border-gray-200 my-3" />);
    }
    // Bullet list
    else if (line.startsWith('- ') || line.startsWith('* ')) {
      elements.push(
        <li key={i} className="ml-4 list-disc text-sm leading-relaxed">
          {renderInline(line.slice(2))}
        </li>
      );
    }
    // Numbered list
    else if (line.match(/^\d+\.\s/)) {
      elements.push(
        <li key={i} className="ml-4 list-decimal text-sm leading-relaxed">
          {renderInline(line.replace(/^\d+\.\s/, ''))}
        </li>
      );
    }
    // Blockquote
    else if (line.startsWith('> ')) {
      elements.push(
        <blockquote key={i} className="border-l-4 border-primary-300 pl-3 text-gray-600 italic text-sm my-2">
          {renderInline(line.slice(2))}
        </blockquote>
      );
    }
    // Empty line
    else if (line.trim() === '') {
      elements.push(<div key={i} className="h-2" />);
    }
    // Regular paragraph
    else {
      elements.push(
        <p key={i} className="text-sm leading-relaxed mb-1">
          {renderInline(line)}
        </p>
      );
    }
    i++;
  }

  return <>{elements}</>;
}

function renderInline(text) {
  // Handle **bold**, *italic*, `code`
  const parts = [];
  let remaining = text;
  let keyIdx = 0;

  while (remaining.length > 0) {
    // Bold
    const boldMatch = remaining.match(/^(.*?)\*\*(.+?)\*\*(.*)/s);
    // Italic
    const italicMatch = remaining.match(/^(.*?)\*(.+?)\*(.*)/s);
    // Code
    const codeMatch = remaining.match(/^(.*?)`(.+?)`(.*)/s);

    // Find which one comes first
    const candidates = [
      boldMatch ? { match: boldMatch, type: 'bold', start: boldMatch[1].length } : null,
      italicMatch ? { match: italicMatch, type: 'italic', start: italicMatch[1].length } : null,
      codeMatch ? { match: codeMatch, type: 'code', start: codeMatch[1].length } : null,
    ].filter(Boolean);

    if (candidates.length === 0) {
      parts.push(<span key={keyIdx++}>{remaining}</span>);
      break;
    }

    // Pick the earliest match
    candidates.sort((a, b) => a.start - b.start);
    const winner = candidates[0];
    const [, before, content, after] = winner.match;

    if (before) parts.push(<span key={keyIdx++}>{before}</span>);

    if (winner.type === 'bold') {
      parts.push(<strong key={keyIdx++} className="font-semibold">{content}</strong>);
    } else if (winner.type === 'italic') {
      parts.push(<em key={keyIdx++}>{content}</em>);
    } else {
      parts.push(
        <code key={keyIdx++} className="bg-gray-100 text-primary-700 rounded px-1 text-xs font-mono">
          {content}
        </code>
      );
    }

    remaining = after;
  }

  return parts;
}

