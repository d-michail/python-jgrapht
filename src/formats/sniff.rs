//! Finding out whether a document declares a directed graph, without parsing all of it.
//!
//! The importers of `jgrapht-io` add to a graph of the caller's choosing, so the direction has to
//! be known beforehand. Each format gets a small scanner that looks only at the place where the
//! format declares it, skipping comments and quoted text.

use super::Fmt;

pub fn directed(fmt: Fmt, text: &str) -> bool {
    match fmt {
        Fmt::Dot => dot(text),
        Fmt::Gml => gml(text),
        Fmt::GraphMl => {
            xml_attribute(text, "graph", "edgedefault").is_some_and(|v| v == "directed")
        }
        Fmt::Gexf => {
            xml_attribute(text, "graph", "defaultedgetype").is_some_and(|v| v == "directed")
        }
        Fmt::Dimacs => dimacs(text),
        Fmt::Graph6 => graph6(text),
        _ => false,
    }
}

/// `[strict] (graph|digraph) ...`, after comments.
fn dot(text: &str) -> bool {
    let mut rest = text;
    loop {
        rest = rest.trim_start();
        if let Some(r) = rest.strip_prefix("//").or_else(|| rest.strip_prefix('#')) {
            rest = r.split_once('\n').map_or("", |(_, after)| after);
        } else if let Some(r) = rest.strip_prefix("/*") {
            rest = r.split_once("*/").map_or("", |(_, after)| after);
        } else {
            let end = rest
                .find(|c: char| !c.is_ascii_alphanumeric() && c != '_')
                .unwrap_or(rest.len());
            let (word, after) = rest.split_at(end);
            match word.to_ascii_lowercase().as_str() {
                "strict" => rest = after,
                "digraph" => return true,
                _ => return false,
            }
        }
    }
}

#[derive(PartialEq)]
enum Token<'a> {
    Open,
    Close,
    Str,
    Word(&'a str),
}

fn gml_tokens(text: &str) -> Vec<Token<'_>> {
    let bytes = text.as_bytes();
    let mut tokens = Vec::new();
    let mut i = 0;
    while i < bytes.len() {
        match bytes[i] {
            b'#' => {
                while i < bytes.len() && bytes[i] != b'\n' {
                    i += 1;
                }
            }
            b'"' => {
                i += 1;
                while i < bytes.len() && bytes[i] != b'"' {
                    i += if bytes[i] == b'\\' { 2 } else { 1 };
                }
                i += 1;
                tokens.push(Token::Str);
            }
            b'[' => {
                tokens.push(Token::Open);
                i += 1;
            }
            b']' => {
                tokens.push(Token::Close);
                i += 1;
            }
            c if c.is_ascii_whitespace() => i += 1,
            _ => {
                let start = i;
                while i < bytes.len()
                    && !bytes[i].is_ascii_whitespace()
                    && !matches!(bytes[i], b'[' | b']' | b'"' | b'#')
                {
                    i += 1;
                }
                tokens.push(Token::Word(&text[start..i]));
            }
        }
    }
    tokens
}

/// `directed 1` among the keys of the outermost `graph [ ... ]`.
fn gml(text: &str) -> bool {
    let tokens = gml_tokens(text);
    let mut depth = 0usize;
    let mut i = 0;
    while i < tokens.len() {
        match &tokens[i] {
            Token::Open => depth += 1,
            Token::Close => depth = depth.saturating_sub(1),
            Token::Word(key) if depth == 1 && key.eq_ignore_ascii_case("directed") => {
                if let Some(Token::Word(value)) = tokens.get(i + 1) {
                    return value.parse::<f64>().is_ok_and(|v| v != 0.0);
                }
            }
            _ => {}
        }
        i += 1;
    }
    false
}

/// The value of attribute `attr` on the first element named `element` (ignoring namespace
/// prefixes), skipping comments, CDATA and processing instructions.
fn xml_attribute(text: &str, element: &str, attr: &str) -> Option<String> {
    let mut rest = text;
    while let Some(at) = rest.find('<') {
        rest = &rest[at + 1..];
        if let Some(r) = rest.strip_prefix("!--") {
            rest = r.split_once("-->")?.1;
        } else if let Some(r) = rest.strip_prefix("![CDATA[") {
            rest = r.split_once("]]>")?.1;
        } else if rest.starts_with('?') || rest.starts_with('!') || rest.starts_with('/') {
            rest = rest.split_once('>')?.1;
        } else {
            let name_end = rest.find(|c: char| c.is_ascii_whitespace() || c == '>' || c == '/')?;
            let name = &rest[..name_end];
            let local = name.rsplit(':').next().unwrap_or(name);
            let (tag, after) = tag_body(&rest[name_end..])?;
            if local == element {
                return attributes(tag)
                    .into_iter()
                    .find(|(k, _)| k.rsplit(':').next() == Some(attr))
                    .map(|(_, v)| v);
            }
            rest = after;
        }
    }
    None
}

/// The text of a start tag up to its closing `>` (quoted values may contain `>`), and what follows.
fn tag_body(text: &str) -> Option<(&str, &str)> {
    let mut quote = None;
    for (i, c) in text.char_indices() {
        match (quote, c) {
            (None, '"' | '\'') => quote = Some(c),
            (Some(q), c) if c == q => quote = None,
            (None, '>') => return Some((&text[..i], &text[i + 1..])),
            _ => {}
        }
    }
    None
}

fn attributes(tag: &str) -> Vec<(String, String)> {
    let mut out = Vec::new();
    let mut rest = tag.trim_start();
    while let Some(eq) = rest.find('=') {
        let name = rest[..eq].trim().trim_start_matches('/').trim().to_owned();
        let after = rest[eq + 1..].trim_start();
        let Some(q) = after.chars().next().filter(|c| matches!(c, '"' | '\'')) else {
            break;
        };
        let Some(end) = after[1..].find(q) else { break };
        out.push((name, after[1..1 + end].to_owned()));
        rest = after[end + 2..].trim_start();
    }
    out
}

/// The first `p` line names a directed problem (shortest path, max flow, min cost, assignment).
fn dimacs(text: &str) -> bool {
    for line in text.lines() {
        let mut tokens = line.split_whitespace();
        if tokens.next() == Some("p") {
            return matches!(tokens.next(), Some("sp" | "max" | "min" | "asn"));
        }
    }
    false
}

/// digraph6 data starts with `&`, after an optional `>>...<<` header.
fn graph6(text: &str) -> bool {
    let line = text
        .lines()
        .map(str::trim)
        .find(|l| !l.is_empty())
        .unwrap_or("");
    let line = match line.strip_prefix(">>") {
        Some(r) => r.split_once("<<").map_or(r, |(_, after)| after),
        None => line,
    };
    line.starts_with('&')
}
