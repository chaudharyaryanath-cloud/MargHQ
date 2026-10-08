from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>MargHQ</title>
        <style>
            :root {
                --bg-dark: #06151f;
                --panel: rgba(10, 22, 34, 0.8);
                --green: #70f7b0;
                --blue: #6cc9ff;
                --text: #eaf9ff;
                --muted: #9cc4d8;
                --line: rgba(125, 199, 255, 0.25);
            }

            * { box-sizing: border-box; }
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background:
                    radial-gradient(circle at 20% 20%, rgba(109, 201, 255, 0.14), transparent 25%),
                    radial-gradient(circle at 80% 15%, rgba(112, 247, 176, 0.10), transparent 20%),
                    linear-gradient(135deg, #040d17 0%, #081a2b 45%, #0b1e2d 100%);
                color: var(--text);
                min-height: 100vh;
            }

            body::before {
                content: "";
                position: fixed;
                inset: 0;
                background-image: radial-gradient(rgba(108, 201, 255, 0.5) 1px, transparent 1px);
                background-size: 18px 18px;
                opacity: 0.35;
                pointer-events: none;
            }

            .container {
                position: relative;
                z-index: 1;
                width: min(1100px, calc(100% - 32px));
                margin: 0 auto;
                padding: 28px 0 70px;
            }

            .nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 50px;
            }

            .logo {
                color: var(--green);
                font-size: 1.5rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }

            .links {
                display: flex;
                gap: 24px;
            }

            .links a {
                color: var(--muted);
                text-decoration: none;
                font-size: 0.9rem;
            }

            .hero {
                display: grid;
                grid-template-columns: 1.2fr 0.8fr;
                gap: 30px;
                align-items: center;
                min-height: 60vh;
            }

            .eyebrow {
                display: inline-block;
                padding: 8px 14px;
                border-radius: 999px;
                background: rgba(112, 247, 176, 0.08);
                border: 1px solid rgba(112, 247, 176, 0.18);
                color: var(--green);
                font-size: 0.72rem;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }

            h1 {
                margin: 20px 0 14px;
                font-size: clamp(3.2rem, 7vw, 6.6rem);
                line-height: 0.92;
                letter-spacing: -0.08em;
                color: var(--green);
            }

            p {
                font-size: 1.08rem;
                line-height: 1.7;
                color: var(--muted);
                max-width: 560px;
            }

            .buttons {
                display: flex;
                gap: 16px;
                margin-top: 26px;
            }

            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 14px 20px;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                transition: 0.2s ease;
            }

            .primary {
                background: linear-gradient(135deg, var(--green), #38d995);
                color: #04150e;
            }

            .secondary {
                border: 1px solid var(--line);
                color: var(--text);
                background: rgba(255,255,255,0.02);
            }

            .card {
                position: relative;
                background: rgba(12, 23, 36, 0.8);
                border: 1px solid var(--line);
                border-radius: 24px;
                padding: 26px;
                box-shadow: 0 22px 40px rgba(0, 0, 0, 0.25);
                min-height: 260px;
            }

            .orb {
                position: absolute;
                border-radius: 50%;
                filter: blur(6px);
            }

            .orb1 {
                width: 210px;
                height: 210px;
                background: radial-gradient(circle, rgba(108, 201, 255, 0.72), rgba(108, 201, 255, 0.08) 60%, transparent 68%);
                right: 30px;
                top: 30px;
            }

            .orb2 {
                width: 170px;
                height: 170px;
                background: radial-gradient(circle, rgba(112, 247, 176, 0.72), rgba(112, 247, 176, 0.08) 60%, transparent 68%);
                left: 30px;
                bottom: 20px;
            }

            .card-inner {
                position: relative;
                z-index: 1;
            }

            .label {
                font-size: 0.72rem;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: var(--green);
            }

            .fit {
                margin-top: 14px;
                font-size: 2rem;
                font-weight: 700;
            }

            .meta {
                margin-top: 8px;
                color: var(--muted);
            }

            .bars {
                display: flex;
                gap: 8px;
                margin-top: 24px;
            }

            .bars span {
                height: 9px;
                flex: 1;
                border-radius: 999px;
                background: linear-gradient(90deg, var(--green), var(--blue));
            }

            .quiz-box {
                margin-top: 50px;
                background: rgba(12, 23, 36, 0.72);
                border: 1px solid var(--line);
                border-radius: 20px;
                padding: 24px;
            }

            form {
                display: grid;
                gap: 18px;
            }

            .row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 18px;
            }

            label {
                display: block;
                font-weight: 600;
                margin-bottom: 8px;
            }

            select, input[type="text"] {
                width: 100%;
                padding: 12px 14px;
                border-radius: 10px;
                border: 1px solid var(--line);
                background: rgba(8, 19, 30, 0.9);
                color: var(--text);
            }

            button {
                width: 100%;
                border: none;
                background: linear-gradient(135deg, var(--green), #38d995);
                color: #061710;
                font-weight: 700;
                padding: 15px;
                border-radius: 12px;
                cursor: pointer;
                font-size: 1rem;
            }

            @media (max-width: 800px) {
                .hero, .row {
                    grid-template-columns: 1fr;
                }
                .nav {
                    flex-direction: column;
                    gap: 12px;
                    align-items: flex-start;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <nav class="nav">
                <div class="logo">MargHQ</div>
                <div class="links">
                    <a href="#about">About</a>
                    <a href="#quiz">Quiz</a>
                    <a href="#result">Results</a>
                </div>
            </nav>

            <section class="hero">
                <div>
                    <span class="eyebrow">Career clarity for your next chapter</span>
                    <h1>MargHQ</h1>
                    <p>Discover the kind of work that fits your strengths, interests, and natural energy.</p>

                    <div class="buttons">
                        <a class="btn primary" href="#quiz">Start quiz</a>
                        <a class="btn secondary" href="#about">Learn more</a>
                    </div>
                </div>

                <div class="card">
                    <div class="orb orb1"></div>
                    <div class="orb orb2"></div>
                    <div class="card-inner">
                        <div class="label">Potential fit</div>
                        <div class="fit">Product Strategy</div>
                        <div class="meta">High alignment • 88%</div>
                        <div class="bars">
                            <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            </section>

            <section class="quiz-box" id="quiz">
                <form action="/result" method="post">
                    <div class="row">
                        <div>
                            <label for="interests">What do you enjoy most?</label>
                            <input type="text" id="interests" name="interests" placeholder="coding, design, business..." />
                        </div>

                        <div>
                            <label for="strengths">Your strongest skill</label>
                            <input type="text" id="strengths" name="strengths" placeholder="problem solving, communication..." />
                        </div>
                    </div>

                    <div class="row">
                        <div>
                            <label for="personality">Personality</label>
                            <select id="personality" name="personality">
                                <option value="analytical">Analytical</option>
                                <option value="creative">Creative</option>
                                <option value="social">Social</option>
                                <option value="leadership">Leadership</option>
                            </select>
                        </div>

                        <div>
                            <label for="work_style">Work style</label>
                            <select id="work_style" name="work_style">
                                <option value="independent">Independent</option>
                                <option value="team">Team-based</option>
                                <option value="flexible">Flexible</option>
                            </select>
                        </div>
                    </div>

                    <div class="row">
                        <div>
                            <label for="risk_tolerance">Risk tolerance</label>
                            <select id="risk_tolerance" name="risk_tolerance">
                                <option value="low">Low</option>
                                <option value="medium" selected>Medium</option>
                                <option value="high">High</option>
                            </select>
                        </div>

                        <div>
                            <label for="name">Your name</label>
                            <input type="text" id="name" name="name" placeholder="Your name" />
                        </div>
                    </div>

                    <button type="submit">See my direction</button>
                </form>
            </section>
        </div>
    </body>
    </html>
    """

@app.post("/result")
async def result_page(
    interests: str = Form(...),
    strengths: str = Form(...),
    personality: str = Form(...),
    work_style: str = Form(...),
    risk_tolerance: str = Form(...),
    name: str = Form("User")
):
    return HTMLResponse(
        f"""
        <html>
        <head>
            <title>MargHQ Result</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #07131f;
                    color: white;
                    padding: 40px;
                }}
                .box {{
                    max-width: 700px;
                    margin: auto;
                    background: rgba(12, 23, 36, 0.75);
                    border: 1px solid rgba(125, 199, 255, 0.25);
                    border-radius: 20px;
                    padding: 30px;
                }}
                h1 {{ color: #70f7b0; }}
            </style>
        </head>
        <body>
            <div class="box">
                <h1>MargHQ Result</h1>
                <p>Hello {name}, your path looks strongest around <strong>Product Strategy</strong>.</p>
                <p><strong>Interests:</strong> {interests}</p>
                <p><strong>Strengths:</strong> {strengths}</p>
                <p><strong>Personality:</strong> {personality}</p>
                <p><strong>Work style:</strong> {work_style}</p>
                <p><strong>Risk tolerance:</strong> {risk_tolerance}</p>
            </div>
        </body>
        </html>
        """
    )