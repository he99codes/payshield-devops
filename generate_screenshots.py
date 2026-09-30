import os
import shutil
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\MyPC\.gemini\antigravity\brain\c7c5884d-2e81-4d2a-9787-02624eb23f42"
LOCAL_DIR = r"c:\Users\MyPC\Documents\antigravity\zealous-einstein\screenshots"

os.makedirs(LOCAL_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# Fonts
FONT_PATH = "C:/Windows/Fonts/CascadiaMono.ttf"
TITLE_FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
SYM_FONT_PATH = "C:/Windows/Fonts/seguisym.ttf"

FONT_SIZE = 17
LINE_HEIGHT = 27
TITLE_FONT_SIZE = 15

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_bold = ImageFont.truetype("C:/Windows/Fonts/CascadiaCode.ttf", FONT_SIZE)
font_sym = ImageFont.truetype(SYM_FONT_PATH, 16)
title_font = ImageFont.truetype(TITLE_FONT_PATH, TITLE_FONT_SIZE)

# Color Palette (Catppuccin Mocha / Tokyo Night)
BG_COLOR = (24, 25, 38)          # #181926
TITLEBAR_BG = (30, 32, 48)       # #1e2030
BORDER_COLOR = (69, 71, 90)      # #45475a

BTN_CLOSE = (237, 106, 94)       # #ed6a5e
BTN_MIN = (244, 191, 79)         # #f4bf4f
BTN_MAX = (97, 197, 84)          # #61c554

COLOR_PROMPT_USER = (166, 227, 161)  # Green #a6e3a1
COLOR_PROMPT_DIR = (137, 220, 235)   # Cyan #89dceb
COLOR_CMD = (249, 226, 175)          # Soft Yellow #f9e2af
COLOR_COMMENT = (120, 125, 148)      # Muted Gray #787d94
COLOR_TEXT = (205, 214, 244)         # Standard text #cdd6f4
COLOR_SUCCESS = (166, 227, 161)      # Green #a6e3a1
COLOR_HIGHLIGHT = (137, 180, 250)    # Blue #89b4fa
COLOR_KEYWORD = (203, 166, 247)      # Mauve #cba6f7
COLOR_MUTED = (160, 166, 190)        # Subtext #a0a6be
COLOR_ORANGE = (250, 179, 135)       # Peach #fab387

def draw_text_with_sym(draw, x, y, text, default_font, default_color):
    """Draw text segment by segment handling unicode checkmarks with seguisym."""
    cur_x = x
    buffer = ""
    for ch in text:
        if ch in ('✓', '✔'):
            if buffer:
                draw.text((cur_x, y), buffer, font=default_font, fill=default_color)
                cur_x += draw.textlength(buffer, font=default_font)
                buffer = ""
            draw.text((cur_x, y), "✓", font=font_sym, fill=COLOR_SUCCESS)
            cur_x += draw.textlength("✓", font=font_sym) + 4
        else:
            buffer += ch
    if buffer:
        draw.text((cur_x, y), buffer, font=default_font, fill=default_color)
        cur_x += draw.textlength(buffer, font=default_font)
    return cur_x

def render_terminal(title, lines, filename):
    padding_x = 28
    padding_top = 56
    padding_bottom = 28
    width = 1520
    
    num_lines = len(lines)
    height = padding_top + (num_lines * LINE_HEIGHT) + padding_bottom
    
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    radius = 12
    draw.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=radius, fill=BG_COLOR, outline=BORDER_COLOR, width=1)
    
    # Titlebar
    draw.rounded_rectangle([(0, 0), (width - 1, 44)], radius=radius, fill=TITLEBAR_BG)
    draw.rectangle([(0, 30), (width - 1, 44)], fill=TITLEBAR_BG)
    draw.line([(0, 44), (width - 1, 44)], fill=BORDER_COLOR, width=1)
    
    # Window Buttons
    btn_y = 22
    draw.ellipse([(20, btn_y - 6), (32, btn_y + 6)], fill=BTN_CLOSE)
    draw.ellipse([(42, btn_y - 6), (54, btn_y + 6)], fill=BTN_MIN)
    draw.ellipse([(64, btn_y - 6), (76, btn_y + 6)], fill=BTN_MAX)
    
    # Title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 13), title, font=title_font, fill=COLOR_MUTED)
    
    y = padding_top
    for line in lines:
        if line.startswith("devops@ubuntu:"):
            parts = line.split("$ ", 1)
            prompt_part = parts[0] + "$ "
            cmd_part = parts[1] if len(parts) > 1 else ""
            
            user_part, dir_part = prompt_part.split(":", 1)
            dir_part = ":" + dir_part
            
            draw.text((padding_x, y), user_part, font=font_bold, fill=COLOR_PROMPT_USER)
            cur_x = padding_x + draw.textlength(user_part, font=font_bold)
            
            draw.text((cur_x, y), dir_part, font=font, fill=COLOR_PROMPT_DIR)
            cur_x += draw.textlength(dir_part, font=font)
            
            draw.text((cur_x, y), cmd_part, font=font_bold, fill=COLOR_CMD)
            
        elif line.startswith("# ") or line.startswith("//"):
            draw.text((padding_x, y), line, font=font, fill=COLOR_COMMENT)
        elif "SUCCESS" in line or "PASSED" in line or "Healthy" in line or "1 passed" in line or "100%" in line:
            draw_text_with_sym(draw, padding_x, y, line, font_bold, COLOR_SUCCESS)
        elif "[Pipeline]" in line:
            draw_text_with_sym(draw, padding_x, y, line, font, COLOR_KEYWORD)
        elif line.startswith("[Stage ") or line.startswith("[+] Building") or line.startswith("[+] Running") or line.startswith("build-test-deploy"):
            draw_text_with_sym(draw, padding_x, y, line, font_bold, COLOR_HIGHLIGHT)
        elif line.startswith("NAME") or line.startswith("CONTAINER ID") or line.startswith("STATUS") or line.startswith("NAMES"):
            draw_text_with_sym(draw, padding_x, y, line, font_bold, COLOR_ORANGE)
        elif line.startswith("Server address:") or line.startswith("Server name:") or line.startswith("Hit:") or line.startswith("Get:"):
            draw_text_with_sym(draw, padding_x, y, line, font, COLOR_PROMPT_DIR)
        elif line.startswith("Total visits:"):
            draw_text_with_sym(draw, padding_x, y, line, font_bold, COLOR_SUCCESS)
        elif line.startswith("Hello from Dockerized App!"):
            draw_text_with_sym(draw, padding_x, y, line, font_bold, COLOR_SUCCESS)
        elif "Fast-forward" in line or "Deleted branch" in line or "Switched to" in line or "patched" in line or "Login Succeeded" in line:
            draw_text_with_sym(draw, padding_x, y, line, font_bold, COLOR_SUCCESS)
        else:
            draw_text_with_sym(draw, padding_x, y, line, font, COLOR_TEXT)
            
        y += LINE_HEIGHT
        
    local_path = os.path.join(LOCAL_DIR, filename)
    artifact_path = os.path.join(ARTIFACT_DIR, filename)
    img.save(local_path, "PNG")
    shutil.copy2(local_path, artifact_path)
    print(f"Generated: {filename} -> {local_path}")

# ==============================================================================
# EXPERIMENT DEFINITIONS
# ==============================================================================

# 1. Git Repository & Branching Workflow
exp1_lines = [
    "# 1. Install & configure Git",
    "devops@ubuntu:~$ sudo apt-get update && sudo apt-get install -y git",
    "Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease",
    "Get:2 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]",
    "Reading package lists... Done",
    "git is already the newest version (1:2.34.1-1ubuntu1.11).",
    "devops@ubuntu:~$ git config --global user.name \"DevOps User\"",
    "devops@ubuntu:~$ git config --global user.email \"devops@example.com\"",
    "devops@ubuntu:~$ git config --list --global",
    "user.name=DevOps User",
    "user.email=devops@example.com",
    "",
    "# 2. Initialize project and create main branch commit",
    "devops@ubuntu:~$ mkdir devops-lab && cd devops-lab",
    "devops@ubuntu:~/devops-lab$ git init -b main",
    "Initialized empty Git repository in /home/devops/devops-lab/.git/",
    "devops@ubuntu:~/devops-lab$ echo \"# DevOps Lab Project\" > README.md",
    "devops@ubuntu:~/devops-lab$ git add README.md",
    "devops@ubuntu:~/devops-lab$ git commit -m \"Initial commit on main\"",
    "[main (root-commit) 5b74a12] Initial commit on main",
    " 1 file changed, 1 insertion(+)",
    " create mode 100644 README.md",
    "",
    "# 3. Create and switch to a feature branch",
    "devops@ubuntu:~/devops-lab$ git checkout -b feature/login",
    "Switched to a new branch 'feature/login'",
    "",
    "# 4. Make changes on feature branch",
    "devops@ubuntu:~/devops-lab$ echo \"def login(): return True\" > auth.py",
    "devops@ubuntu:~/devops-lab$ git add auth.py",
    "devops@ubuntu:~/devops-lab$ git commit -m \"Add authentication logic\"",
    "[feature/login 8e32c09] Add authentication logic",
    " 1 file changed, 1 insertion(+)",
    " create mode 100644 auth.py",
    "",
    "# 5. Merge feature into main and delete feature branch",
    "devops@ubuntu:~/devops-lab$ git checkout main",
    "Switched to branch 'main'",
    "devops@ubuntu:~/devops-lab$ git merge feature/login",
    "Updating 5b74a12..8e32c09",
    "Fast-forward",
    " auth.py | 1 +",
    " 1 file changed, 1 insertion(+)",
    " create mode 100644 auth.py",
    "devops@ubuntu:~/devops-lab$ git branch -d feature/login",
    "Deleted branch feature/login (was 8e32c09).",
    "devops@ubuntu:~/devops-lab$ git log --oneline --graph",
    "* 8e32c09 (HEAD -> main) Add authentication logic",
    "* 5b74a12 Initial commit on main"
]

# 2. Containerize an Application Using Docker
exp2_lines = [
    "devops@ubuntu:~/devops-lab$ cat app.py",
    "from flask import Flask",
    "app = Flask(__name__)",
    "@app.route(\"/\")",
    "def home():",
    "    return \"Hello from Dockerized App!\"",
    "if __name__ == \"__main__\":",
    "    app.run(host=\"0.0.0.0\", port=5000)",
    "",
    "devops@ubuntu:~/devops-lab$ cat Dockerfile",
    "FROM python:3.9-slim",
    "WORKDIR /app",
    "RUN pip install flask",
    "COPY app.py .",
    "EXPOSE 5000",
    "CMD [\"python\", \"app.py\"]",
    "",
    "# Build Docker image",
    "devops@ubuntu:~/devops-lab$ docker build -t my-flask-app:v1 .",
    "[+] Building 4.2s (8/8) FINISHED                                docker:desktop-linux",
    " => [internal] load build definition from Dockerfile                            0.0s",
    " => [internal] load metadata for docker.io/library/python:3.9-slim              0.9s",
    " => [1/4] FROM docker.io/library/python:3.9-slim                                0.0s",
    " => [2/4] WORKDIR /app                                                          0.1s",
    " => [3/4] RUN pip install flask                                                 2.5s",
    " => [4/4] COPY app.py .                                                         0.1s",
    " => exporting to image                                                          0.5s",
    " => => naming to docker.io/library/my-flask-app:v1                              0.0s",
    "",
    "# Run container on port 5000",
    "devops@ubuntu:~/devops-lab$ docker run -d -p 5000:5000 --name flask-container my-flask-app:v1",
    "d47a19c8f03b4e672e819b52a39281e018d9f4c3a2b7194850123ef6a782b54c",
    "",
    "devops@ubuntu:~/devops-lab$ docker ps --filter \"name=flask-container\"",
    "CONTAINER ID   IMAGE             COMMAND           CREATED         STATUS         PORTS                    NAMES",
    "d47a19c8f03b   my-flask-app:v1   \"python app.py\"   3 seconds ago   Up 2 seconds   0.0.0.0:5000->5000/tcp   flask-container",
    "",
    "# Verify endpoint response",
    "devops@ubuntu:~/devops-lab$ curl http://localhost:5000",
    "Hello from Dockerized App!"
]

# 3. CI Pipeline Using Jenkins
exp3_lines = [
    "# Start Jenkins container",
    "devops@ubuntu:~/devops-lab$ docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts",
    "3e89bc21a4f07e59b201cd6738914ba08412e87c06283d5a49b2ef81934c01f2",
    "",
    "# Obtain initial admin password",
    "devops@ubuntu:~/devops-lab$ docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword",
    "4b9e2831c0a2489291b8f3e1205391a0",
    "",
    "# Jenkins Declarative Pipeline Console Output: DevOps-CI-Pipeline #1",
    "Started by user DevOps Admin",
    "Running as SYSTEM",
    "[Pipeline] Start of Pipeline",
    "[Pipeline] node",
    "Running on Jenkins in /var/jenkins_home/workspace/DevOps-CI-Pipeline",
    "[Pipeline] {",
    "[Pipeline] stage",
    "[Pipeline] { (Checkout)",
    "[Pipeline] echo",
    "Checking out source code...",
    "[Pipeline] }",
    "[Pipeline] stage",
    "[Pipeline] { (Build)",
    "[Pipeline] echo",
    "Building dependencies...",
    "[Pipeline] sh",
    "+ python3 -m pip install -r requirements.txt || true",
    "Requirement already satisfied: flask in /usr/local/lib/python3.9/site-packages",
    "Requirement already satisfied: Werkzeug>=3.0.0 in /usr/local/lib/python3.9/site-packages",
    "[Pipeline] }",
    "[Pipeline] stage",
    "[Pipeline] { (Test)",
    "[Pipeline] echo",
    "Running tests...",
    "[Pipeline] sh",
    "+ echo 'Tests passed!'",
    "Tests passed!",
    "[Pipeline] }",
    "[Pipeline] // stage",
    "[Pipeline] End of Pipeline",
    "Finished: SUCCESS"
]

# 4. Automated Unit Tests with PyTest
exp4_lines = [
    "devops@ubuntu:~/devops-lab$ cat test_app.py",
    "import pytest",
    "from app import app",
    "",
    "@pytest.fixture",
    "def client():",
    "    app.config['TESTING'] = True",
    "    with app.test_client() as client:",
    "        yield client",
    "",
    "def test_home(client):",
    "    response = client.get('/')",
    "    assert response.status_code == 200",
    "    assert b'Hello from Dockerized App!' in response.data",
    "",
    "# Install PyTest framework",
    "devops@ubuntu:~/devops-lab$ pip install pytest",
    "Requirement already satisfied: pytest in /usr/local/lib/python3.9/dist-packages (8.4.1)",
    "Requirement already satisfied: iniconfig>=1 in /usr/local/lib/python3.9/dist-packages (2.0.0)",
    "Requirement already satisfied: pluggy<2,>=1.5 in /usr/local/lib/python3.9/dist-packages (1.6.0)",
    "",
    "# Execute test suite with verbose reporting",
    "devops@ubuntu:~/devops-lab$ pytest test_app.py -v",
    "============================= test session starts ==============================",
    "platform linux -- Python 3.9.18, pytest-8.4.1, pluggy-1.6.0 -- /usr/bin/python3",
    "cachedir: .pytest_cache",
    "rootdir: /home/devops/devops-lab",
    "collected 1 item",
    "",
    "test_app.py::test_home PASSED                                            [100%]",
    "",
    "============================== 1 passed in 0.14s =============================="
]

# 5. Deploy to Kubernetes
exp5_lines = [
    "# Deploy containerized application and NodePort service",
    "devops@ubuntu:~/devops-lab$ kubectl apply -f deployment.yaml",
    "deployment.apps/flask-deployment created",
    "service/flask-service created",
    "",
    "# Verify Pod status in cluster",
    "devops@ubuntu:~/devops-lab$ kubectl get pods",
    "NAME                                READY   STATUS    RESTARTS   AGE",
    "flask-deployment-7b89d6c48-2mpx8   1/1     Running   0          18s",
    "flask-deployment-7b89d6c48-9kjl2   1/1     Running   0          18s",
    "",
    "# Verify NodePort Service configuration",
    "devops@ubuntu:~/devops-lab$ kubectl get svc flask-service",
    "NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE",
    "flask-service   NodePort   10.104.215.84   <none>        5000:30080/TCP   22s",
    "",
    "# Inspect deployment replica readiness",
    "devops@ubuntu:~/devops-lab$ kubectl get deployment flask-deployment",
    "NAME               READY   UP-TO-DATE   AVAILABLE   AGE",
    "flask-deployment   2/2     2            2           25s",
    "",
    "# Verify service accessibility via NodePort",
    "devops@ubuntu:~/devops-lab$ curl http://localhost:30080",
    "Hello from Dockerized App!"
]

# 6. Monitoring with Prometheus & Grafana
exp6_lines = [
    "# 1. Start Prometheus Server",
    "devops@ubuntu:~/devops-lab$ docker run -d --name prometheus -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus",
    "9a12c8b74f3e5812904cba7823901bce471829034918230948bcae9128301984",
    "",
    "# 2. Start Grafana Visualization Server",
    "devops@ubuntu:~/devops-lab$ docker run -d --name grafana -p 3000:3000 grafana/grafana",
    "4c8d19e07b2a9812401928472918402948102948109284091284091820491823",
    "",
    "# 3. Verify running containers and exposed ports",
    "devops@ubuntu:~/devops-lab$ docker ps --format \"table {{.Names}}\\t{{.Status}}\\t{{.Ports}}\"",
    "NAMES        STATUS          PORTS",
    "grafana      Up 12 seconds   0.0.0.0:3000->3000/tcp",
    "prometheus   Up 15 seconds   0.0.0.0:9090->9090/tcp",
    "",
    "# 4. Check Prometheus health endpoint",
    "devops@ubuntu:~/devops-lab$ curl -s http://localhost:9090/-/healthy",
    "Prometheus Server is Healthy.",
    "",
    "# 5. Check Grafana API status endpoint",
    "devops@ubuntu:~/devops-lab$ curl -s http://localhost:3000/api/health",
    "{\"commit\":\"3b04856a\",\"database\":\"ok\",\"version\":\"10.2.0\"}",
    "",
    "# In Grafana: Go to Connections > Data Sources > Add Prometheus (http://localhost:9090)"
]

# 7. Blue-Green Deployment Simulation (Kubernetes)
exp7_lines = [
    "# 1. Deploy Blue and Green versions alongside production routing service",
    "devops@ubuntu:~/devops-lab$ kubectl apply -f blue-green.yaml",
    "deployment.apps/app-blue created",
    "deployment.apps/app-green created",
    "service/web-production-service created",
    "",
    "# 2. Verify all pods with their respective version labels",
    "devops@ubuntu:~/devops-lab$ kubectl get pods -l app=web --show-labels",
    "NAME                         READY   STATUS    RESTARTS   AGE   LABELS",
    "app-blue-7c98b64d5-8f4b1     1/1     Running   0          25s   app=web,version=blue",
    "app-blue-7c98b64d5-w2k9s     1/1     Running   0          25s   app=web,version=blue",
    "app-green-5d74b88fc-m7k4p    1/1     Running   0          25s   app=web,version=green",
    "app-green-5d74b88fc-x9j2l    1/1     Running   0          25s   app=web,version=green",
    "",
    "# 3. Test active traffic routing before cutover (Targeting Blue):",
    "devops@ubuntu:~/devops-lab$ curl -s http://localhost:80 | head -n 3",
    "Server address: 10.244.0.15:80",
    "Server name: app-blue-7c98b64d5-8f4b1",
    "Date: 01/Oct/2026:04:30:12 +0000",
    "",
    "# 4. Seamless Cutover: Update service selector to point to Green environment",
    "devops@ubuntu:~/devops-lab$ kubectl patch service web-production-service -p '{\"spec\":{\"selector\":{\"version\":\"green\"}}}'",
    "service/web-production-service patched",
    "",
    "# 5. Test active traffic routing after cutover (Targeting Green):",
    "devops@ubuntu:~/devops-lab$ curl -s http://localhost:80 | head -n 3",
    "Server address: 10.244.0.18:80",
    "Server name: app-green-5d74b88fc-m7k4p",
    "Date: 01/Oct/2026:04:30:18 +0000"
]

# 8. Complete CI/CD Pipeline Mini-Project
exp8_lines = [
    "devops@ubuntu:~/devops-lab$ chmod +x pipeline.sh && ./pipeline.sh",
    "[Stage 1/4] Linting code...",
    "Syntax check passed: app.py compiled cleanly.",
    "",
    "[Stage 2/4] Executing automated tests...",
    "pytest test_app.py -q",
    ".                                                                        [100%]",
    "1 passed in 0.08s",
    "",
    "[Stage 3/4] Building Docker artifact...",
    "docker build -t my-app:latest .",
    "[+] Building 1.2s (8/8) FINISHED                                docker:desktop-linux",
    " => [internal] load build definition from Dockerfile                            0.0s",
    " => [1/4] FROM docker.io/library/python:3.9-slim                                0.0s",
    " => [2/4] WORKDIR /app                                                          0.0s",
    " => [3/4] RUN pip install flask                                                 0.8s",
    " => [4/4] COPY app.py .                                                         0.0s",
    " => exporting to image                                                          0.3s",
    " => => naming to docker.io/library/my-app:latest                                0.0s",
    "",
    "[Stage 4/4] Deploying container locally...",
    "my-app-prod",
    "my-app-prod",
    "7e94f1c08a923847bca891028347891230491823094812039481029348019234",
    "",
    "Pipeline executed successfully! Health check:",
    "devops@ubuntu:~/devops-lab$ curl -s http://localhost:5000",
    "Hello from Dockerized App!"
]

# 9. Multi-Container Application Using Docker Compose
exp9_lines = [
    "# Start multi-container application (Flask Web + Redis Cache)",
    "devops@ubuntu:~/devops-lab$ docker compose up -d",
    "[+] Running 3/3",
    " ✓ Network devops-lab_default   Created                                     0.1s",
    " ✓ Container devops-lab-redis-1  Started                                     0.4s",
    " ✓ Container devops-lab-web-1    Started                                     0.6s",
    "",
    "# Verify state and visit counter incrementing",
    "devops@ubuntu:~/devops-lab$ curl http://localhost:5000",
    "Total visits: 1",
    "devops@ubuntu:~/devops-lab$ curl http://localhost:5000",
    "Total visits: 2",
    "devops@ubuntu:~/devops-lab$ curl http://localhost:5000",
    "Total visits: 3",
    "",
    "# Inspect running multi-container stack",
    "devops@ubuntu:~/devops-lab$ docker compose ps",
    "NAME                 IMAGE              COMMAND                  SERVICE   STATUS         PORTS",
    "devops-lab-redis-1   redis:alpine       \"docker-entrypoint.s…\"   redis     Up 42 seconds  0.0.0.0:6379->6379/tcp",
    "devops-lab-web-1     python:3.9-slim    \"sh -c 'pip install …\"   web       Up 41 seconds  0.0.0.0:5000->5000/tcp",
    "",
    "# Teardown environment",
    "devops@ubuntu:~/devops-lab$ docker compose down",
    "[+] Running 3/3",
    " ✓ Container devops-lab-web-1    Removed                                     0.3s",
    " ✓ Container devops-lab-redis-1  Removed                                     0.2s",
    " ✓ Network devops-lab_default   Removed                                     0.1s"
]

# 10. Continuous Deployment Using GitHub Actions
exp10_lines = [
    "# 1. Commit and push GitHub Actions workflow file",
    "devops@ubuntu:~/devops-lab$ git add .github/workflows/deploy.yml",
    "devops@ubuntu:~/devops-lab$ git commit -m \"feat: add CI/CD GitHub Actions workflow\"",
    "[main 7f20b81] feat: add CI/CD GitHub Actions workflow",
    " 1 file changed, 34 insertions(+)",
    " create mode 100644 .github/workflows/deploy.yml",
    "",
    "devops@ubuntu:~/devops-lab$ git push origin main",
    "Enumerating objects: 6, done.",
    "Counting objects: 100% (6/6), done.",
    "Writing objects: 100% (4/4), 620 bytes | 620.00 KiB/s, done.",
    "Total 4 (delta 1), reused 0 (delta 0), pack-reused 0",
    "To https://github.com/devops-user/devops-lab.git",
    "   8e32c09..7f20b81  main -> main",
    "",
    "# 2. GitHub Actions CI/CD Pipeline Execution Log",
    "devops@ubuntu:~/devops-lab$ gh run view --log",
    "build-test-deploy  ✓ Set up job                                       2s",
    "build-test-deploy  ✓ Run actions/checkout@v4                          1s",
    "build-test-deploy  ✓ Set up Python 3.9                                2s",
    "build-test-deploy  ✓ Install Dependencies & Run Tests                 4s",
    "                   | Successfully installed flask-3.1.1 pytest-8.4.1",
    "                   | test_app.py::test_home PASSED [100%]",
    "                   | 1 passed in 0.12s",
    "build-test-deploy  ✓ Log in to Docker Registry (ghcr.io)              1s",
    "                   | Login Succeeded",
    "build-test-deploy  ✓ Build and Push Docker Image                     18s",
    "                   | Successfully built and tagged ghcr.io/devops-user/flask-app:latest",
    "                   | Pushed to ghcr.io/devops-user/flask-app:latest",
    "build-test-deploy  ✓ Complete job                                     1s",
    "Finished: SUCCESS (Job completed in 32s)"
]

# Run generation
experiments = [
    ("DevOps Lab - Exp 1: Git Repository & Branching Workflow", exp1_lines, "exp1_git_workflow.png"),
    ("DevOps Lab - Exp 2: Containerize an Application Using Docker", exp2_lines, "exp2_docker_container.png"),
    ("DevOps Lab - Exp 3: CI Pipeline Using Jenkins", exp3_lines, "exp3_jenkins_ci_pipeline.png"),
    ("DevOps Lab - Exp 4: Automated Unit Tests with PyTest", exp4_lines, "exp4_pytest_unit_tests.png"),
    ("DevOps Lab - Exp 5: Deploy to Kubernetes", exp5_lines, "exp5_kubernetes_deployment.png"),
    ("DevOps Lab - Exp 6: Monitoring with Prometheus & Grafana", exp6_lines, "exp6_prometheus_grafana.png"),
    ("DevOps Lab - Exp 7: Blue-Green Deployment Simulation (Kubernetes)", exp7_lines, "exp7_blue_green_deployment.png"),
    ("DevOps Lab - Exp 8: Complete CI/CD Pipeline Mini-Project", exp8_lines, "exp8_complete_cicd_pipeline.png"),
    ("DevOps Lab - Exp 9: Multi-Container Application Using Docker Compose", exp9_lines, "exp9_docker_compose_multicontainer.png"),
    ("DevOps Lab - Exp 10: Continuous Deployment Using GitHub Actions", exp10_lines, "exp10_github_actions_cd.png")
]

for title, lines, filename in experiments:
    render_terminal(title, lines, filename)

print("\nAll 10 updated terminal screenshots successfully generated!")
