async function ensureD3() {
  if (window.d3) {
    return window.d3;
  }

  await new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/d3@7";
    script.onload = resolve;
    script.onerror = () => reject(new Error("Failed to load D3."));
    document.head.appendChild(script);
  });

  return window.d3;
}

function colorForType(type) {
  switch (type) {
    case "note":
      return "#f16431";
    case "index":
      return "#cbb9aa";
    case "report":
      return "#7d8792";
    default:
      return "#5d666f";
  }
}

async function renderGraph() {
  const container = document.getElementById("graph");
  if (!container) {
    return;
  }

  container.innerHTML = '<div class="graph-empty">Loading graph…</div>';

  try {
    const [d3, response] = await Promise.all([ensureD3(), fetch("/api/graph")]);
    if (!response.ok) {
      throw new Error(`Graph request failed with ${response.status}`);
    }

    const data = await response.json();
    if (!data.nodes.length) {
      container.innerHTML =
        '<div class="graph-empty">No markdown files found.</div>';
      return;
    }

    container.innerHTML = "";
    const tooltip = document.createElement("div");
    tooltip.className = "graph-tooltip";
    document.body.appendChild(tooltip);

    const svg = d3.select(container).append("svg");
    const layer = svg.append("g");
    const linkLayer = layer
      .append("g")
      .attr("stroke", "rgba(255, 255, 255, 0.12)");
    const nodeLayer = layer.append("g");
    const labelLayer = layer.append("g");

    const zoom = d3
      .zoom()
      .scaleExtent([0.3, 3])
      .on("zoom", (event) => {
        layer.attr("transform", event.transform);
      });
    svg.call(zoom);

    const simulation = d3
      .forceSimulation(data.nodes)
      .force(
        "link",
        d3
          .forceLink(data.links)
          .id((node) => node.id)
          .distance(86)
          .strength(0.24),
      )
      .force("charge", d3.forceManyBody().strength(-230))
      .force("center", d3.forceCenter())
      .force("collision", d3.forceCollide().radius(20));

    const links = linkLayer
      .selectAll("line")
      .data(data.links)
      .join("line")
      .attr("stroke-width", 1.15);

    const nodes = nodeLayer
      .selectAll("circle")
      .data(data.nodes)
      .join("circle")
      .attr("r", 8.5)
      .attr("fill", (node) => colorForType(node.type))
      .attr("stroke", "rgba(255, 244, 235, 0.22)")
      .attr("stroke-width", 1.1)
      .attr("cursor", "pointer")
      .style("filter", (node) =>
        node.type === "note"
          ? "drop-shadow(0 0 8px rgba(241, 100, 49, 0.18))"
          : "drop-shadow(0 0 6px rgba(255, 255, 255, 0.06))",
      )
      .call(
        d3
          .drag()
          .on("start", (event, node) => {
            if (!event.active) {
              simulation.alphaTarget(0.2).restart();
            }
            node.fx = node.x;
            node.fy = node.y;
          })
          .on("drag", (event, node) => {
            node.fx = event.x;
            node.fy = event.y;
          })
          .on("end", (event, node) => {
            if (!event.active) {
              simulation.alphaTarget(0);
            }
            node.fx = null;
            node.fy = null;
          }),
      );

    nodes
      .on("click", (_, node) => {
        window.location.href = node.url;
      })
      .on("mouseenter", (event, node) => {
        tooltip.textContent = node.label;
        tooltip.style.opacity = "1";
        tooltip.style.left = `${event.clientX}px`;
        tooltip.style.top = `${event.clientY}px`;
      })
      .on("mousemove", (event) => {
        tooltip.style.left = `${event.clientX}px`;
        tooltip.style.top = `${event.clientY}px`;
      })
      .on("mouseleave", () => {
        tooltip.style.opacity = "0";
      });

    const labels = labelLayer
      .selectAll("text")
      .data(data.nodes)
      .join("text")
      .text((node) => node.label)
      .attr("font-size", 11)
      .attr("fill", "#e6ddd4")
      .attr("dx", 12)
      .attr("dy", 4)
      .style(
        "font-family",
        "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
      )
      .style("pointer-events", "none");

    function resize() {
      const rect = container.getBoundingClientRect();
      svg.attr("viewBox", [0, 0, rect.width, rect.height]);
      simulation.force(
        "center",
        d3.forceCenter(rect.width / 2, rect.height / 2),
      );
      simulation.alpha(0.3).restart();
    }

    simulation.on("tick", () => {
      links
        .attr("x1", (link) => link.source.x)
        .attr("y1", (link) => link.source.y)
        .attr("x2", (link) => link.target.x)
        .attr("y2", (link) => link.target.y);

      nodes.attr("cx", (node) => node.x).attr("cy", (node) => node.y);
      labels.attr("x", (node) => node.x).attr("y", (node) => node.y);
    });

    resize();
    window.addEventListener("resize", resize, { passive: true });
  } catch (error) {
    console.error(error);
    container.innerHTML = `<div class="graph-empty">${error.message}</div>`;
  }
}

document.addEventListener("DOMContentLoaded", renderGraph);
