const ratingDescriptions = {
  frustration_tolerance: ["Give up quickly", "Lose patience", "It depends", "Stay with it", "Keep trying calmly"],
  immersion: ["Very hard", "A little", "Sometimes", "Often", "Lose track of time"],
  failure_resilience: ["Very discouraged", "Need a reset", "Recover with time", "Learn and retry", "Learn quickly"],
  energy_level: ["Low", "Steady-low", "Balanced", "Energetic", "High energy"],
  social_energy: ["Prefer solo", "Mostly solo", "A mix", "Enjoy teamwork", "Very collaborative"],
  preference_for_structure: ["Very free", "Mostly flexible", "A mix", "Clear plans", "Strong structure"],
  creative_drive: ["Not much", "Occasionally", "Somewhat", "Quite a lot", "Very creative"],
  problem_solving_drive: ["Not really", "A little", "Sometimes", "Enjoy it", "Strongly enjoy it"]
};

const form = document.querySelector("#assessment-form");
const resultPanel = document.querySelector("#assessment-result");
const roadmapForm = document.querySelector("#roadmap-form");
const roadmapResult = document.querySelector("#roadmap-result");

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

for (const question of document.querySelectorAll(".question")) {
  const name = question.dataset.question;
  const options = question.querySelector(".rating-options");
  ratingDescriptions[name].forEach((description, index) => {
    const value = index + 1;
    const label = element("label", "rating-option");
    const input = document.createElement("input");
    input.type = "radio";
    input.name = name;
    input.value = String(value);
    input.required = value === 1;
    label.title = `${value}: ${description}`;
    label.append(input, element("span", "", String(value)));
    options.append(label);
  });
}

function addSectionTitle(parent, title, detail) {
  const heading = element("div", "result-section-title");
  heading.append(element("span", "", title), element("span", "", detail));
  parent.append(heading);
}

document.querySelectorAll(".mode-button").forEach((button) => {
  button.addEventListener("click", () => {
    const selectedMode = button.dataset.mode;
    document.querySelectorAll(".mode-button").forEach((tab) => {
      const selected = tab === button;
      tab.classList.toggle("is-active", selected);
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    document.querySelectorAll(".mode-panel").forEach((panel) => {
      panel.hidden = panel.id !== `${selectedMode}-panel`;
    });
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const submitButton = form.querySelector("button[type='submit']");
  const payload = Object.fromEntries(new FormData(form));
  for (const key of Object.keys(ratingDescriptions)) payload[key] = Number(payload[key]);
  submitButton.disabled = true;
  submitButton.querySelector("span").textContent = "Reading your answers...";

  try {
    const response = await fetch("/api/assess", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("The assessment could not be completed. Check your answers and try again.");
    renderAssessment(await response.json());
  } catch (error) {
    resultPanel.replaceChildren(element("p", "result-error", error.message || "Could not connect to MargHQ. Check that the server is running and try again."));
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector("span").textContent = "Get my direction";
  }
});

function renderAssessment(data) {
  const content = element("div", "result-content");
  content.append(element("p", "eyebrow", "YOUR CAREER READOUT"));
  content.append(element("h4", "", data.best_path));
  content.append(element("p", "result-summary", `${data.name}, this is a promising direction to explore. Treat it as a starting point and test it with a small project.`));
  addSectionTitle(content, "OTHER DIRECTIONS", "ALSO EXPLORE");
  content.append(element("p", "alternative-paths", data.alternative_paths.join("  /  ")));
  addSectionTitle(content, "WORK STYLE SNAPSHOT", "OUT OF 5");

  const behaviorLabels = {
    frustration_tolerance: "Frustration tolerance",
    immersion: "Deep focus",
    failure_resilience: "Resilience",
    energy_level: "Work energy",
    social_energy: "Social energy"
  };
  for (const [key, label] of Object.entries(behaviorLabels)) {
    const row = element("div", "behavior-row");
    row.append(element("span", "", label), element("span", "behavior-value", `${data.summary[key]}/5`));
    const track = element("div", "behavior-track");
    const fill = element("div", "behavior-fill");
    fill.style.width = `${data.summary[key] * 20}%`;
    track.append(fill);
    row.append(track);
    content.append(row);
  }

  addSectionTitle(content, "TRY IT OUT", "STARTER PROJECTS");
  const projects = element("ul", "project-list");
  for (const project of data.projects) {
    const item = element("li");
    item.append(element("span", "", project.title), element("span", "", project.duration));
    projects.append(item);
  }
  content.append(projects);
  resultPanel.replaceChildren(content);
}

roadmapForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const submitButton = roadmapForm.querySelector("button[type='submit']");
  const targetJob = new FormData(roadmapForm).get("targetJob").trim();
  submitButton.disabled = true;
  submitButton.querySelector("span").textContent = "Mapping your steps...";

  try {
    const response = await fetch("http://127.0.0.1:8000/generate-roadmap ", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ targetJob })
    });
    if (!response.ok) throw new Error("The workflow could not be generated. Check the career title and try again.");
    renderRoadmap(targetJob, await response.json());
  } catch (error) {
    roadmapResult.replaceChildren(element("p", "roadmap-error", error.message || "Could not connect to MargHQ. Check that the server is running and try again."));
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector("span").textContent = "Build my workflow";
  }
});

function renderRoadmap(targetJob, roadmap) {
  const wrapper = document.createDocumentFragment();
  const heading = element("div", "roadmap-heading");
  const titleGroup = document.createElement("div");
  titleGroup.append(element("p", "eyebrow", "YOUR 12-WEEK CAREER WORKFLOW"), element("h4", "", targetJob));
  heading.append(titleGroup, element("span", "roadmap-total", `${roadmap.nodes.length} PHASES · 12 WEEKS`));
  wrapper.append(heading);
  const steps = element("div", "roadmap-steps");
  const orderedNodes = [...roadmap.nodes].sort((a, b) => a.position.y - b.position.y);
  orderedNodes.forEach((node, index) => {
    const step = element("article", "roadmap-step");
    step.append(element("span", "step-marker", String(index + 1).padStart(2, "0")));
    step.append(element("span", "step-duration", node.data.duration || `PHASE ${index + 1}`));
    step.append(element("h5", "", node.data.label.replace(/^\d+\.\s*/, "")));
    step.append(element("p", "", node.data.description || "Follow this step and record what you learn."));
    steps.append(step);
  });
  wrapper.append(steps);
  roadmapResult.replaceChildren(wrapper);
}