import os
import base64

ARTIFACT_DIR = r"C:\Users\MyPC\.gemini\antigravity\brain\c7c5884d-2e81-4d2a-9787-02624eb23f42"
LOCAL_DIR = r"c:\Users\MyPC\Documents\antigravity\zealous-einstein\screenshots"

experiments = [
    {
        "id": "1",
        "title": "Exp 1: Git Repository & Branching Workflow",
        "badge": "Version Control",
        "filename": "exp1_git_workflow.png",
        "desc": "Initialize repository, configure git identity, create feature branch, commit changes, merge back to main, and delete branch."
    },
    {
        "id": "2",
        "title": "Exp 2: Containerize an Application Using Docker",
        "badge": "Docker",
        "filename": "exp2_docker_container.png",
        "desc": "Build an optimized Python 3.9 Flask container, expose port 5000, run container daemon, and verify HTTP curl response."
    },
    {
        "id": "3",
        "title": "Exp 3: CI Pipeline Using Jenkins",
        "badge": "CI Automation",
        "filename": "exp3_jenkins_ci_pipeline.png",
        "desc": "Launch Jenkins LTS container, extract admin token, and execute declarative Jenkinsfile pipeline through Checkout, Build, and Test."
    },
    {
        "id": "4",
        "title": "Exp 4: Automated Unit Tests with PyTest",
        "badge": "Testing",
        "filename": "exp4_pytest_unit_tests.png",
        "desc": "Write automated unit test fixture for Flask app and execute PyTest suite with verbose test pass reporting."
    },
    {
        "id": "5",
        "title": "Exp 5: Deploy to Kubernetes",
        "badge": "Kubernetes",
        "filename": "exp5_kubernetes_deployment.png",
        "desc": "Deploy 2-replica pod deployment with NodePort service on port 30080 and verify pod health."
    },
    {
        "id": "6",
        "title": "Exp 6: Monitoring with Prometheus & Grafana",
        "badge": "Observability",
        "filename": "exp6_prometheus_grafana.png",
        "desc": "Deploy Prometheus metrics scraper on port 9090 and Grafana dashboard visualization on port 3000."
    },
    {
        "id": "7",
        "title": "Exp 7: Blue-Green Deployment Simulation",
        "badge": "Zero Downtime",
        "filename": "exp7_blue_green_deployment.png",
        "desc": "Zero-downtime traffic switching between Blue and Green deployments using live Kubernetes service selector patching."
    },
    {
        "id": "8",
        "title": "Exp 8: Complete CI/CD Pipeline Mini-Project",
        "badge": "Full Pipeline",
        "filename": "exp8_complete_cicd_pipeline.png",
        "desc": "End-to-end automated script performing linting (py_compile), test execution (pytest), docker build, and deployment."
    },
    {
        "id": "9",
        "title": "Exp 9: Multi-Container Stack (Docker Compose)",
        "badge": "Docker Compose",
        "filename": "exp9_docker_compose_multicontainer.png",
        "desc": "Spin up multi-container microservice with Flask web server and Redis in-memory database with visit counter."
    },
    {
        "id": "10",
        "title": "Exp 10: Continuous Deployment (GitHub Actions)",
        "badge": "Cloud CD",
        "filename": "exp10_github_actions_cd.png",
        "desc": "Automated workflow on git push to main: automated testing, login to ghcr.io, and publishing container image."
    }
]

# Build base64 dict
b64_images = {}
for exp in experiments:
    img_path = os.path.join(LOCAL_DIR, exp["filename"])
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
        b64_images[exp["id"]] = f"data:image/png;base64,{b64}"

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DevOps Lab Output Screenshots Gallery</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      background: #0f111a;
      color: #e2e8f0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}
    .tab-btn.active {{
      background-color: #3b82f6;
      color: #ffffff;
      border-color: #3b82f6;
    }}
  </style>
</head>
<body class="p-6">
  <div class="max-w-7xl mx-auto space-y-6">
    
    <!-- Header -->
    <header class="bg-[#181a27] border border-slate-700/60 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full text-xs font-semibold tracking-wider uppercase">
            10 / 10 Experiments Executed
          </span>
          <span class="text-xs text-slate-400">High-DPI Screenshots Ready</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-bold text-white mt-2">DevOps Lab Experiments: Terminal Output Gallery</h1>
        <p class="text-slate-400 text-sm mt-1">Complete verification records with verified outputs and terminal screenshots.</p>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="showAllMode()" id="viewAllBtn" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-sm font-medium transition">
          View All Grid
        </button>
      </div>
    </header>

    <!-- Navigation Pills -->
    <div class="flex flex-wrap gap-2 pb-1" id="tabContainer">
"""

for exp in experiments:
    active_class = "active" if exp["id"] == "1" else ""
    html += f"""      <button onclick="selectExp('{exp['id']}')" id="btn-{exp['id']}" class="tab-btn {active_class} px-3.5 py-1.5 rounded-lg text-xs font-medium bg-[#1e2030] hover:bg-slate-800 text-slate-300 border border-slate-700/60 transition">
        {exp['id']}. {exp['badge']}
      </button>\n"""

html += """    </div>

    <!-- Single View Container -->
    <div id="singleView" class="space-y-4">
"""

for exp in experiments:
    hidden_class = "" if exp["id"] == "1" else "hidden"
    data_uri = b64_images[exp["id"]]
    html += f"""      <div id="card-{exp['id']}" class="exp-card {hidden_class} bg-[#181a27] border border-slate-700/60 rounded-2xl p-6 shadow-xl space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-slate-800">
          <div>
            <span class="text-xs font-semibold text-blue-400 uppercase tracking-wider">{exp['badge']}</span>
            <h2 class="text-xl font-bold text-white mt-0.5">{exp['title']}</h2>
            <p class="text-slate-400 text-sm mt-1">{exp['desc']}</p>
          </div>
          <div class="flex items-center gap-2">
            <a href="{data_uri}" download="{exp['filename']}" class="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-medium transition shadow flex items-center gap-1.5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
              Download PNG
            </a>
          </div>
        </div>
        <div class="bg-[#0b0c14] p-3 rounded-xl border border-slate-800/80 overflow-x-auto flex justify-center">
          <img src="{data_uri}" alt="{exp['title']}" class="rounded-lg shadow-2xl max-w-full h-auto border border-slate-800" />
        </div>
      </div>\n"""

html += """    </div>

    <!-- All in One Grid View (Hidden by default) -->
    <div id="allView" class="hidden space-y-8">
"""

for exp in experiments:
    data_uri = b64_images[exp["id"]]
    html += f"""      <div class="bg-[#181a27] border border-slate-700/60 rounded-2xl p-6 shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <div>
            <span class="text-xs font-semibold text-blue-400 uppercase tracking-wider">{exp['badge']}</span>
            <h3 class="text-lg font-bold text-white">{exp['title']}</h3>
          </div>
          <a href="{data_uri}" download="{exp['filename']}" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition">
            Save Image
          </a>
        </div>
        <div class="bg-[#0b0c14] p-2 rounded-xl border border-slate-800/80 overflow-x-auto flex justify-center">
          <img src="{data_uri}" alt="{exp['title']}" class="rounded-lg shadow-xl max-w-full h-auto" />
        </div>
      </div>\n"""

html += """    </div>

  </div>

  <script>
    let isAllView = false;

    function selectExp(id) {
      if (isAllView) toggleViewMode();
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('btn-' + id);
      if (activeBtn) activeBtn.classList.add('active');

      document.querySelectorAll('.exp-card').forEach(c => c.classList.add('hidden'));
      const activeCard = document.getElementById('card-' + id);
      if (activeCard) activeCard.classList.remove('hidden');
    }

    function showAllMode() {
      toggleViewMode();
    }

    function toggleViewMode() {
      isAllView = !isAllView;
      const single = document.getElementById('singleView');
      const all = document.getElementById('allView');
      const tabContainer = document.getElementById('tabContainer');
      const btn = document.getElementById('viewAllBtn');

      if (isAllView) {
        single.classList.add('hidden');
        all.classList.remove('hidden');
        tabContainer.classList.add('opacity-50', 'pointer-events-none');
        btn.innerText = "Single Tab Mode";
        btn.classList.add('bg-blue-600', 'text-white');
      } else {
        all.classList.add('hidden');
        single.classList.remove('hidden');
        tabContainer.classList.remove('opacity-50', 'pointer-events-none');
        btn.innerText = "View All Grid";
        btn.classList.remove('bg-blue-600', 'text-white');
      }
    }
  </script>
</body>
</html>
"""

html_artifact_path = os.path.join(ARTIFACT_DIR, "devops_gallery.html")
with open(html_artifact_path, "w", encoding="utf-8") as f:
    f.write(html)

local_html_path = os.path.join(r"c:\Users\MyPC\Documents\antigravity\zealous-einstein", "devops_gallery.html")
with open(local_html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Generated interactive HTML gallery at:", html_artifact_path)
