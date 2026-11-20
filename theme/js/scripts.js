// Render Mermaid diagrams, including after instant navigation
document$.subscribe(function () {
  if (typeof mermaid === "undefined") return;

  // superfences wraps the source in <code>; Mermaid needs plain text
  document.querySelectorAll("pre.mermaid").forEach(function (pre) {
    var code = pre.querySelector("code");
    if (code) pre.textContent = code.textContent;
  });

  var dark = document.body.getAttribute("data-md-color-scheme") === "slate";
  mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "default" });
  mermaid.run({ querySelector: "pre.mermaid" });
});