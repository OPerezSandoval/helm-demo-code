from flask import Flask, jsonify, render_template_string
import os
import socket

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Helm Demo - {{ env }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: {{ bg_gradient }};
            min-height: 100vh;
            padding: 40px 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Animated background circles */
        body::before {
            content: '';
            position: fixed;
            width: 500px;
            height: 500px;
            background: {{ accent }};
            border-radius: 50%;
            top: -250px;
            right: -250px;
            opacity: 0.1;
            z-index: 0;
        }
        
        body::after {
            content: '';
            position: fixed;
            width: 400px;
            height: 400px;
            background: {{ accent }};
            border-radius: 50%;
            bottom: -200px;
            left: -200px;
            opacity: 0.1;
            z-index: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .logo {
            font-size: 64px;
            margin-bottom: 10px;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        h1 {
            font-size: 42px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }
        
        .env-badge {
            display: inline-block;
            background: {{ accent }};
            color: {{ badge_text }};
            padding: 12px 32px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 18px;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        }
        
        .card-icon {
            font-size: 36px;
            margin-bottom: 15px;
        }
        
        .card-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .card-value {
            color: white;
            font-size: 24px;
            font-weight: 700;
            font-family: 'Monaco', 'Courier New', monospace;
            word-break: break-all;
        }
        
        .labels-card {
            grid-column: 1 / -1;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .labels-title {
            color: white;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        
        .tag {
            background: linear-gradient(135deg, {{ accent }} 0%, {{ accent_dark }} 100%);
            color: {{ badge_text }};
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease;
        }
        
        .tag:hover {
            transform: scale(1.05);
        }
        
        .config-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .config-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .config-key {
            color: rgba(255, 255, 255, 0.6);
            font-size: 11px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .config-value {
            color: white;
            font-size: 14px;
            font-family: 'Monaco', monospace;
        }
        
        @media (max-width: 768px) {
            h1 { font-size: 32px; }
            .grid { grid-template-columns: 1fr; }
            .card-value { font-size: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⎈</div>
            <h1>Helm Demo Display</h1>
            <div class="env-badge">{{ env }}</div>
        </div>
        
        <div class="grid">
            <div class="card">
                <div class="card-icon">📦</div>
                <div class="card-label">Pod Name</div>
                <div class="card-value">{{ hostname }}</div>
            </div>
            
            <div class="card">
                <div class="card-icon">🛸</div>
                <div class="card-label">Deployment</div>
                <div class="card-value">{{ deployment }}</div>
            </div>
            
            <div class="card">
                <div class="card-icon">⚙️</div>
                <div class="card-label">Namespace</div>
                <div class="card-value">{{ namespace }}</div>
            </div>
            
            <div class="card">
                <div class="card-icon">🔖</div>
                <div class="card-label">Version</div>
                <div class="card-value">{{ version }}</div>
            </div>
            
            <div class="card">
                <div class="card-icon">👥</div>
                <div class="card-label">Replicas</div>
                <div class="card-value">{{ replicas }}</div>
            </div>
            
            <div class="card">
                <div class="card-icon">⚓️</div>
                <div class="card-label">Helm Release</div>
                <div class="card-value">{{ release }}</div>
            </div>
            
            <div class="card">
                <div class="card-icon">🎯</div>
                <div class="card-label">Production Mode</div>
                <div class="card-value">{{ production_mode }}</div>
            </div>
            
            <div class="card">
                <div class="card-icon">📝</div>
                <div class="card-label">Log Level</div>
                <div class="card-value">{{ log_level }}</div>
            </div>
        </div>
        
        <div class="labels-card">
            <div class="labels-title">
                <span>🏷️</span>
                <span>Custom Labels</span>
            </div>
            <div class="tags">
                {% for label in custom_labels %}
                <div class="tag">{{ label }}</div>
                {% endfor %}
            </div>
        </div>
        
        {% if config_data %}
        <div class="labels-card" style="margin-top: 30px;">
            <div class="labels-title">
                <span>🗂️</span>
                <span>ConfigMap Data</span>
            </div>
            <div class="config-grid">
                {% for key, value in config_data.items() %}
                <div class="config-item">
                    <div class="config-key">{{ key }}</div>
                    <div class="config-value">{{ value }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if extra_vars %}
        <div class="labels-card" style="margin-top: 30px;">
            <div class="labels-title">
                <span>⚡</span>
                <span>Extra Environment Variables (via Range)</span>
            </div>
            <div class="config-grid">
                {% for key, value in extra_vars.items() %}
                <div class="config-item">
                    <div class="config-key">{{ key }}</div>
                    <div class="config-value">{{ value }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    env = os.getenv('ENVIRONMENT', 'unknown')
    
    colors = {
        'development': {
            'bg': 'linear-gradient(135deg, #1e293b 0%, #334155 100%)', 
            'accent': '#f59e0b',
            'accent_dark': '#d97706',
            'badge_text': '#ffffff'
        },
        'production': {
            'bg': 'linear-gradient(135deg, #374151 0%, #4b5563 100%)',  
            'accent': '#10b981',
            'accent_dark': '#059669',
            'badge_text': '#ffffff'
        }
    }
    
    color_scheme = colors.get(env, {
        'bg': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'accent': '#a78bfa',
        'accent_dark': '#7c3aed',
        'badge_text': '#1f2937'
    })
    
    # Get custom labels from environment
    labels_str = os.getenv('CUSTOM_LABELS', '')
    custom_labels = [l.strip() for l in labels_str.split(',') if l.strip()]
    
    # Get production mode and log level (from IF statement in Helm)
    production_mode = os.getenv('PRODUCTION_MODE', 'unknown')
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # ConfigMap data if enabled
    config_data = {}
    if os.getenv('DATABASE_HOST'):
        config_data = {
            'database_host': os.getenv('DATABASE_HOST', 'not set'),
            'cache_ttl': os.getenv('CACHE_TTL', 'not set'),
            'api_endpoint': os.getenv('API_ENDPOINT', 'not set')
        }
    
    # Get extra env vars (from RANGE in Helm)
    extra_vars = {}
    for key, value in os.environ.items():
        if (key.startswith('DEBUG_') or 
            key.startswith('MONITORING') or 
            key.startswith('VERBOSE_') or 
            key.startswith('METRICS_') or 
            key.startswith('DEV_') or 
            key.startswith('ALERTING')):
            extra_vars[key] = value
    
    return render_template_string(
        HTML,
        env=env,
        hostname=socket.gethostname(),
        namespace=os.getenv('POD_NAMESPACE', 'unknown'),
        deployment=os.getenv('DEPLOYMENT_NAME', 'unknown'),
        version=os.getenv('APP_VERSION', '1.0'),
        replicas=os.getenv('REPLICA_COUNT', 'unknown'),
        release=os.getenv('HELM_RELEASE', 'unknown'),
        custom_labels=custom_labels if custom_labels else ['none'],
        production_mode=production_mode,
        log_level=log_level,
        config_data=config_data,
        extra_vars=extra_vars,
        bg_gradient=color_scheme['bg'],
        accent=color_scheme['accent'],
        accent_dark=color_scheme['accent_dark'],
        badge_text=color_scheme['badge_text']
    )

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
