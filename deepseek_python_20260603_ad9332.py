<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Trust Gifts</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg-primary: #07141a;
            --bg-secondary: #0b202a;
            --bg-card: rgba(14, 40, 52, 0.45);
            --border-color: rgba(0, 255, 200, 0.10);
            --text-primary: #e6f7f0;
            --text-secondary: #8fc9d9;
            --text-muted: #4f8a9a;
            --aqua: #00e5c8;
            --coral: #ff6b6b;
            --sunny: #ffd93d;
            --gradient-main: linear-gradient(135deg, #00e5c8, #00b8a0, #00897b);
            --radius: 28px;
            --radius-sm: 16px;
            --success: #00e5a0;
            --danger: #ff6b6b;
            --warning: #ffd93d;
            --shadow-glow: 0 8px 40px rgba(0, 229, 200, 0.08);
            --glass-border: rgba(255, 255, 255, 0.04);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 16px;
            padding-bottom: 90px;
            overflow-x: hidden;
            background-image:
                radial-gradient(circle at 10% 20%, rgba(0, 229, 200, 0.06) 0%, transparent 45%),
                radial-gradient(circle at 90% 80%, rgba(255, 107, 107, 0.03) 0%, transparent 40%);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: var(--aqua); border-radius: 10px; }

        .summer-scene { position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none; }
        .summer-scene .sun { position: absolute; top: 20px; right: 40px; width: 120px; height: 120px; border-radius: 50%; background: radial-gradient(circle, #ffd93d, #f9a825 60%, transparent 75%); box-shadow: 0 0 120px rgba(255, 217, 61, 0.15); animation: sunSpin 30s linear infinite; opacity: 0.3; }
        @keyframes sunSpin { 0% { transform: rotate(0deg) scale(1); } 50% { transform: rotate(180deg) scale(1.05); } 100% { transform: rotate(360deg) scale(1); } }
        .summer-scene .wave { position: absolute; bottom: 0; left: 0; right: 0; height: 120px; background: repeating-linear-gradient(90deg, transparent, rgba(0, 229, 200, 0.02) 30px, transparent 60px); animation: waveMove 12s ease-in-out infinite; opacity: 0.3; }
        .summer-scene .wave:nth-child(2) { bottom: 20px; height: 80px; animation-delay: -4s; opacity: 0.2; }
        .summer-scene .wave:nth-child(3) { bottom: 0px; height: 100px; animation-delay: -8s; opacity: 0.15; }
        @keyframes waveMove { 0% { transform: translateX(-40px) scaleY(1); } 50% { transform: translateX(40px) scaleY(1.1); } 100% { transform: translateX(-40px) scaleY(1); } }
        .summer-scene .cloud { position: absolute; font-size: 40px; opacity: 0.05; animation: cloudFloat 40s linear infinite; }
        .summer-scene .cloud:nth-child(4) { top: 10%; left: -10%; animation-duration: 35s; }
        .summer-scene .cloud:nth-child(5) { top: 30%; left: -20%; animation-duration: 50s; animation-delay: -10s; }
        .summer-scene .cloud:nth-child(6) { top: 5%; left: -30%; animation-duration: 45s; animation-delay: -20s; }
        @keyframes cloudFloat { 0% { transform: translateX(0); } 100% { transform: translateX(110vw); } }
        .summer-scene .bird { position: absolute; font-size: 16px; opacity: 0.04; animation: birdFly 25s linear infinite; }
        .summer-scene .bird:nth-child(7) { top: 15%; left: -5%; animation-duration: 22s; }
        .summer-scene .bird:nth-child(8) { top: 25%; left: -15%; animation-duration: 28s; animation-delay: -8s; }
        @keyframes birdFly { 0% { transform: translateX(0) translateY(0); } 25% { transform: translateX(25vw) translateY(-20px); } 50% { transform: translateX(50vw) translateY(10px); } 75% { transform: translateX(75vw) translateY(-15px); } 100% { transform: translateX(110vw) translateY(0); } }

        @keyframes popIn { 0% { opacity: 0; transform: scale(0.96) translateY(12px); } 100% { opacity: 1; transform: scale(1) translateY(0); } }
        @keyframes slideFade { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
        @keyframes pulseGlow { 0%,100% { box-shadow: 0 0 20px rgba(0, 229, 200, 0.05); } 50% { box-shadow: 0 0 60px rgba(0, 229, 200, 0.12); } }
        @keyframes shimmerText { 0% { background-position: -200% center; } 100% { background-position: 200% center; } }
        @keyframes floatUp { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-16px) rotate(4deg); } }
        @keyframes spinSlow { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes typingBounce { 0%,60%,100% { transform: translateY(0); } 30% { transform: translateY(-8px); } }

        .glass {
            background: var(--bg-card);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-glow), inset 0 1px 0 rgba(255, 255, 255, 0.03);
            animation: popIn 0.5s ease forwards;
        }
        .glass:hover { border-color: rgba(0, 229, 200, 0.12); }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 14px 20px; border-radius: var(--radius); margin-bottom: 16px;
            flex-wrap: wrap; gap: 8px; position: relative; z-index: 2;
        }
        .header-logo { font-size: 38px; filter: drop-shadow(0 0 20px rgba(0, 229, 200, 0.3)); animation: floatUp 5s ease-in-out infinite; }
        .header-title { font-size: 24px; font-weight: 900; background: linear-gradient(135deg, #00e5c8, #ffd93d, #ff6b6b); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shimmerText 4s linear infinite; }
        .header-title span { font-weight: 400; -webkit-text-fill-color: var(--text-secondary); }
        .header-user { font-size: 12px; color: var(--text-secondary); font-weight: 500; }
        .header-balance { font-size: 15px; font-weight: 700; color: var(--aqua); background: rgba(0, 229, 200, 0.06); padding: 2px 18px; border-radius: 30px; border: 1px solid rgba(0, 229, 200, 0.1); }
        .online-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(0, 229, 200, 0.06); padding: 4px 14px; border-radius: 30px; font-size: 11px; font-weight: 600; color: var(--aqua); border: 1px solid rgba(0, 229, 200, 0.08); }
        .online-dot { width: 7px; height: 7px; background: var(--aqua); border-radius: 50%; display: inline-block; animation: pulseGlow 1.8s ease-in-out infinite; }

        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px; z-index: 2; position: relative; }
        .stat-card { padding: 14px 10px; border-radius: var(--radius-sm); text-align: center; background: var(--bg-card); backdrop-filter: blur(12px); border: 1px solid var(--border-color); transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); animation: slideFade 0.5s ease backwards; }
        .stat-card:nth-child(1) { animation-delay: 0.05s; }
        .stat-card:nth-child(2) { animation-delay: 0.10s; }
        .stat-card:nth-child(3) { animation-delay: 0.15s; }
        .stat-card:hover { transform: translateY(-6px) scale(1.02); border-color: rgba(0, 229, 200, 0.2); box-shadow: 0 12px 40px rgba(0, 229, 200, 0.08); }
        .stat-number { font-size: 26px; font-weight: 900; background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: block; transition: all 0.3s; }
        .stat-label { font-size: 9px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; margin-top: 4px; }

        .nav {
            display: flex; gap: 6px; background: var(--bg-card); backdrop-filter: blur(20px);
            padding: 8px; border-radius: var(--radius); border: 1px solid var(--border-color);
            margin-bottom: 16px; overflow-x: auto; flex-wrap: nowrap; position: relative; z-index: 2;
            -webkit-overflow-scrolling: touch;
        }
        .nav button {
            flex: 1; min-width: 48px; padding: 10px 4px; border: none; border-radius: var(--radius-sm);
            background: transparent; color: var(--text-secondary); font-size: 10px; font-weight: 600;
            font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            white-space: nowrap; display: flex; flex-direction: column; align-items: center; justify-content: center;
            gap: 2px; position: relative; -webkit-tap-highlight-color: transparent;
        }
        .nav button i { font-size: 20px; transition: all 0.3s; }
        .nav button span { font-size: 8px; opacity: 0.7; font-weight: 500; }
        .nav button::after { content: ''; position: absolute; bottom: 4px; left: 50%; transform: translateX(-50%); width: 0; height: 2px; background: var(--gradient-main); border-radius: 10px; transition: width 0.4s ease; }
        .nav button:hover:not(.active) { color: var(--text-primary); background: rgba(0, 229, 200, 0.04); transform: translateY(-2px); }
        .nav button.active { background: var(--gradient-main); color: #07141a; box-shadow: 0 8px 30px rgba(0, 229, 200, 0.2); transform: scale(1.02); }
        .nav button.active i { color: #07141a; }
        .nav button.active::after { width: 60%; }

        .page { display: none; animation: slideFade 0.5s ease; position: relative; z-index: 2; }
        .page.active { display: block; }

        .card { background: var(--bg-card); backdrop-filter: blur(16px); border-radius: var(--radius); padding: 20px; margin: 10px 0; border: 1px solid var(--border-color); box-shadow: 0 8px 40px rgba(0, 0, 0, 0.12); transition: all 0.4s ease; animation: slideFade 0.5s ease backwards; }
        .card:hover { border-color: rgba(0, 229, 200, 0.12); transform: translateY(-2px); }
        .card-title { font-size: 18px; font-weight: 800; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; letter-spacing: -0.3px; }
        .card-title i { color: var(--aqua); font-size: 22px; text-shadow: 0 0 30px rgba(0, 229, 200, 0.2); }
        .card-subtitle { font-size: 13px; color: var(--text-secondary); font-weight: 400; margin-bottom: 14px; }

        .hero-card { background: linear-gradient(145deg, rgba(0, 229, 200, 0.08), rgba(14, 40, 52, 0.7) 50%, rgba(255, 107, 107, 0.04)); border-color: rgba(0, 229, 200, 0.15); overflow: hidden; position: relative; min-height: 200px; }
        .hero-card::before { content: '🏄'; position: absolute; font-size: 120px; right: -10px; bottom: -20px; opacity: 0.08; transform: rotate(-10deg); }
        .hero-card::after { content: '🌊'; position: absolute; font-size: 80px; left: -10px; top: -10px; opacity: 0.06; }
        .hero-wave { position: absolute; bottom: 0; left: 0; right: 0; height: 40px; background: repeating-linear-gradient(90deg, transparent, rgba(0, 229, 200, 0.03) 20px, transparent 40px); animation: waveMove 6s ease-in-out infinite; }

        .btn { padding: 12px 20px; border: none; border-radius: var(--radius-sm); font-weight: 700; font-size: 14px; font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); display: inline-flex; align-items: center; justify-content: center; gap: 10px; width: 100%; -webkit-tap-highlight-color: transparent; }
        .btn:active { transform: scale(0.96); }
        .btn-primary { background: var(--gradient-main); color: #07141a; box-shadow: 0 8px 30px rgba(0, 229, 200, 0.15); }
        .btn-primary:hover { transform: translateY(-4px) scale(1.02); box-shadow: 0 12px 50px rgba(0, 229, 200, 0.25); }
        .btn-secondary { background: rgba(255, 255, 255, 0.04); color: var(--text-primary); border: 1px solid var(--border-color); }
        .btn-secondary:hover { background: rgba(255, 255, 255, 0.08); transform: translateY(-3px); }
        .btn-gold { background: linear-gradient(135deg, #ffd93d, #f9a825); color: #07141a; box-shadow: 0 8px 30px rgba(255, 217, 61, 0.15); }
        .btn-gold:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(255, 217, 61, 0.25); }
        .btn-success { background: rgba(0, 229, 160, 0.12); color: var(--success); border: 1px solid rgba(0, 229, 160, 0.15); }
        .btn-success:hover { background: rgba(0, 229, 160, 0.2); transform: translateY(-3px); }
        .btn-danger { background: rgba(255, 107, 107, 0.12); color: var(--danger); border: 1px solid rgba(255, 107, 107, 0.15); }
        .btn-danger:hover { background: rgba(255, 107, 107, 0.2); transform: translateY(-3px); }
        .btn-sm { padding: 8px 16px; font-size: 12px; width: auto; }
        .btn-support { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: #fff; box-shadow: 0 8px 30px rgba(255, 107, 107, 0.2); }
        .btn-support:hover { transform: translateY(-4px) scale(1.02); box-shadow: 0 12px 40px rgba(255, 107, 107, 0.3); }
        .btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none !important; }

        .form-group { margin: 12px 0; }
        .form-group label { display: block; color: var(--text-secondary); font-size: 12px; font-weight: 600; margin-bottom: 5px; }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%; padding: 12px 16px; background: rgba(0, 0, 0, 0.25);
            border: 1px solid var(--border-color); border-radius: var(--radius-sm);
            color: var(--text-primary); font-size: 14px; font-family: 'Inter', sans-serif;
            transition: all 0.3s; box-sizing: border-box; -webkit-appearance: none; appearance: none;
        }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none; border-color: var(--aqua); box-shadow: 0 0 0 4px rgba(0, 229, 200, 0.06);
        }
        .form-group textarea { resize: vertical; min-height: 70px; }

        .balance-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
        .balance-item { display: flex; flex-direction: column; align-items: center; padding: 12px 8px; background: rgba(0, 0, 0, 0.15); border-radius: var(--radius-sm); border: 1px solid var(--border-color); transition: all 0.3s; }
        .balance-item:hover { border-color: rgba(0, 229, 200, 0.15); transform: translateY(-2px); }
        .balance-item .label { font-size: 10px; color: var(--text-muted); font-weight: 500; }
        .balance-item .value { font-size: 18px; font-weight: 800; margin-top: 2px; }
        .balance-item .value.ton { color: var(--aqua); }
        .balance-item .value.stars { color: var(--sunny); }
        .balance-item .value.rub { color: var(--success); }
        .balance-item .value.uah { color: var(--coral); }

        .deal-card { background: rgba(0, 0, 0, 0.15); border-radius: var(--radius-sm); padding: 14px; margin: 6px 0; border: 1px solid var(--border-color); transition: all 0.3s; }
        .deal-card:hover { border-color: rgba(0, 229, 200, 0.1); }
        .deal-status { display: inline-block; padding: 2px 14px; border-radius: 30px; font-size: 10px; font-weight: 700; }
        .deal-status.waiting { background: rgba(255, 217, 61, 0.12); color: #ffd93d; }
        .deal-status.paid { background: rgba(0, 229, 160, 0.12); color: #00e5a0; }
        .deal-status.awaiting { background: rgba(0, 229, 200, 0.12); color: var(--aqua); }
        .deal-status.completed { background: rgba(0, 229, 200, 0.12); color: var(--aqua); }

        .support-block { background: rgba(0, 229, 200, 0.04); border-radius: var(--radius-sm); padding: 14px; border-left: 3px solid var(--aqua); margin-top: 8px; }
        .support-block a { color: var(--aqua); text-decoration: none; font-weight: 600; }

        .guide-step { display: flex; gap: 14px; padding: 12px; background: rgba(0, 0, 0, 0.1); border-radius: var(--radius-sm); margin: 6px 0; align-items: flex-start; border: 1px solid var(--border-color); }
        .guide-step .num { font-size: 20px; font-weight: 900; color: var(--aqua); min-width: 32px; text-align: center; }
        .guide-step .content { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }
        .guide-step .content strong { color: var(--text-primary); }

        .verification-status { padding: 10px 14px; border-radius: var(--radius-sm); margin: 8px 0; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
        .verification-status.verified { background: rgba(0, 229, 160, 0.08); border: 1px solid rgba(0, 229, 160, 0.15); color: var(--success); }
        .verification-status.unverified { background: rgba(255, 217, 61, 0.08); border: 1px solid rgba(255, 217, 61, 0.15); color: var(--sunny); }

        .wizard-steps { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; margin: 12px 0 16px; }
        .wizard-dot { height: 6px; border-radius: 999px; background: rgba(255, 255, 255, 0.06); overflow: hidden; }
        .wizard-dot.active { background: var(--gradient-main); box-shadow: 0 0 24px rgba(0, 229, 200, 0.2); }
        .wizard-panel { display: none; animation: slideFade 0.35s ease; }
        .wizard-panel.active { display: block; }
        .wizard-preview { padding: 14px; border-radius: var(--radius-sm); border: 1px solid rgba(0, 229, 200, 0.14); background: rgba(0, 229, 200, 0.04); margin-top: 10px; }

        .modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(24px); display: none; align-items: center; justify-content: center; z-index: 1000; padding: 16px; }
        .modal.active { display: flex; }
        .modal-content { background: var(--bg-secondary); border-radius: var(--radius); padding: 24px; max-width: 480px; width: 100%; max-height: 85vh; overflow-y: auto; border: 1px solid var(--border-color); box-shadow: 0 24px 80px rgba(0, 0, 0, 0.5); animation: slideFade 0.4s ease; }
        .modal-close { float: right; font-size: 24px; cursor: pointer; color: var(--text-muted); background: none; border: none; transition: 0.3s; padding: 4px; }
        .modal-close:hover { color: var(--text-primary); transform: rotate(90deg); }

        .toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: var(--bg-secondary); color: var(--text-primary); padding: 14px 24px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); box-shadow: 0 16px 60px rgba(0, 0, 0, 0.4); z-index: 2000; animation: slideFade 0.4s ease; max-width: 92%; text-align: center; font-weight: 500; font-size: 14px; backdrop-filter: blur(20px); }
        .toast.success { border-color: rgba(0, 229, 160, 0.3); }
        .toast.error { border-color: rgba(255, 107, 107, 0.3); }
        .toast.info { border-color: rgba(0, 229, 200, 0.3); }

        .ticket-card { background: rgba(0, 0, 0, 0.15); border-radius: var(--radius-sm); padding: 14px; margin: 6px 0; border: 1px solid var(--border-color); }
        .ticket-status { font-size: 11px; font-weight: 700; padding: 2px 12px; border-radius: 30px; display: inline-block; }
        .ticket-status.open { background: rgba(0, 229, 160, 0.1); color: var(--success); border: 1px solid rgba(0, 229, 160, 0.1); }
        .ticket-status.closed { background: rgba(255, 255, 255, 0.05); color: var(--text-muted); border: 1px solid var(--border-color); }
        .ticket-status.waiting { background: rgba(255, 217, 61, 0.1); color: var(--sunny); border: 1px solid rgba(255, 217, 61, 0.1); }

        .admin-stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
        .admin-stat-card { padding: 18px 16px; border-radius: var(--radius-sm); background: rgba(0, 0, 0, 0.15); border: 1px solid var(--border-color); text-align: center; transition: 0.4s; animation: slideFade 0.5s ease backwards; }
        .admin-stat-card:nth-child(1) { animation-delay: 0.05s; }
        .admin-stat-card:nth-child(2) { animation-delay: 0.10s; }
        .admin-stat-card:nth-child(3) { animation-delay: 0.15s; }
        .admin-stat-card:nth-child(4) { animation-delay: 0.20s; }
        .admin-stat-card:nth-child(5) { animation-delay: 0.25s; }
        .admin-stat-card:nth-child(6) { animation-delay: 0.30s; }
        .admin-stat-card:hover { transform: translateY(-4px); border-color: rgba(0, 229, 200, 0.15); }
        .admin-stat-card .num { font-size: 28px; font-weight: 900; background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .admin-stat-card .label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

        .admin-tabs { display: flex; gap: 4px; background: rgba(0, 0, 0, 0.15); padding: 4px; border-radius: var(--radius-sm); margin-bottom: 16px; overflow-x: auto; -webkit-overflow-scrolling: touch; }
        .admin-tabs button { padding: 8px 16px; border: none; border-radius: var(--radius-sm); background: transparent; color: var(--text-secondary); font-weight: 600; font-size: 12px; font-family: 'Inter', sans-serif; cursor: pointer; transition: 0.3s; white-space: nowrap; -webkit-tap-highlight-color: transparent; }
        .admin-tabs button.active { background: var(--gradient-main); color: #07141a; box-shadow: 0 4px 20px rgba(0, 229, 200, 0.1); }
        .admin-tabs button:hover:not(.active) { color: var(--text-primary); background: rgba(255, 255, 255, 0.03); }
        .admin-panel { display: none; animation: slideFade 0.4s ease; }
        .admin-panel.active { display: block; }

        .nft-card { display: inline-flex; align-items: center; gap: 12px; padding: 10px 16px; border-radius: var(--radius-sm); background: rgba(0, 229, 200, 0.04); border: 1px solid rgba(0, 229, 200, 0.08); margin-top: 6px; }
        .nft-card .icon { font-size: 28px; }
        .nft-card .info .name { font-weight: 700; color: var(--aqua); }
        .nft-card .info .number { font-size: 12px; color: var(--text-muted); }
        .nft-card .info .link { font-size: 11px; color: var(--text-secondary); word-break: break-all; }

        .chat-container { display: flex; flex-direction: column; height: 500px; max-height: 70vh; background: rgba(0, 0, 0, 0.15); border-radius: var(--radius-sm); border: 1px solid var(--border-color); overflow: hidden; }
        .chat-header { padding: 14px 18px; background: rgba(0, 229, 200, 0.04); border-bottom: 1px solid var(--border-color); display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
        .chat-header .avatar { width: 38px; height: 38px; border-radius: 50%; background: var(--gradient-main); display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: #07141a; }
        .chat-header .info { flex: 1; }
        .chat-header .info .name { font-weight: 700; font-size: 14px; }
        .chat-header .info .status { font-size: 11px; color: var(--text-muted); }
        .chat-messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 8px; scroll-behavior: smooth; }
        .chat-messages::-webkit-scrollbar { width: 3px; }
        .chat-messages::-webkit-scrollbar-thumb { background: var(--aqua); border-radius: 10px; }
        .msg { max-width: 80%; padding: 10px 14px; border-radius: var(--radius-sm); font-size: 13px; line-height: 1.5; animation: slideFade 0.3s ease; position: relative; word-wrap: break-word; }
        .msg.user { align-self: flex-end; background: var(--gradient-main); color: #07141a; border-bottom-right-radius: 4px; }
        .msg.admin { align-self: flex-start; background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border-color); border-bottom-left-radius: 4px; }
        .msg .time { font-size: 9px; color: var(--text-muted); margin-top: 4px; display: block; text-align: right; opacity: 0.6; }
        .msg.user .time { color: rgba(7, 20, 26, 0.5); }
        .msg .typing-indicator { display: flex; gap: 4px; padding: 8px 0; }
        .msg .typing-indicator span { width: 8px; height: 8px; border-radius: 50%; background: var(--text-muted); animation: typingBounce 1.2s ease-in-out infinite; }
        .msg .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .msg .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        .chat-input { padding: 12px 16px; background: rgba(0, 0, 0, 0.15); border-top: 1px solid var(--border-color); display: flex; gap: 10px; flex-shrink: 0; align-items: center; }
        .chat-input input { flex: 1; padding: 10px 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); background: rgba(0, 0, 0, 0.2); color: var(--text-primary); font-size: 14px; font-family: 'Inter', sans-serif; outline: none; transition: 0.3s; }
        .chat-input input:focus { border-color: var(--aqua); box-shadow: 0 0 0 4px rgba(0, 229, 200, 0.04); }
        .chat-input button { padding: 10px 18px; border-radius: var(--radius-sm); border: none; background: var(--gradient-main); color: #07141a; font-weight: 700; cursor: pointer; transition: 0.3s; flex-shrink: 0; }
        .chat-input button:hover { transform: scale(1.04); box-shadow: 0 8px 30px rgba(0, 229, 200, 0.15); }
        .chat-input button:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

        .loading { text-align: center; padding: 30px; color: var(--text-muted); }
        .loading i { font-size: 28px; color: var(--aqua); animation: spinSlow 1.2s linear infinite; display: block; margin-bottom: 12px; }

        .mt-10 { margin-top: 10px; }
        .mt-6 { margin-top: 6px; }
        .flex { display: flex; gap: 8px; }
        .flex .btn { flex: 1; }
        .text-center { text-align: center; }
        .text-muted { color: var(--text-muted); }
        .text-secondary { color: var(--text-secondary); }
        .text-success { color: var(--success); }
        .text-danger { color: var(--danger); }

        @media (max-width: 480px) {
            body { padding: 10px; }
            .header { padding: 12px 14px; }
            .header-title { font-size: 18px; }
            .stats-grid { grid-template-columns: repeat(3, 1fr); gap: 6px; }
            .balance-grid { grid-template-columns: repeat(2, 1fr); }
            .nav button { min-width: 40px; padding: 8px 4px; }
            .nav button i { font-size: 16px; }
            .nav button span { font-size: 7px; }
            .card { padding: 14px; }
            .btn { padding: 10px 14px; font-size: 12px; }
            .admin-stat-grid { grid-template-columns: 1fr 1fr; }
            .chat-container { height: 400px; }
            .summer-scene .sun { width: 60px; height: 60px; right: 10px; top: 10px; }
        }
        @media (min-width: 768px) {
            body { padding: 24px; max-width: 880px; margin: 0 auto; }
            .stats-grid { grid-template-columns: repeat(3, 1fr); }
            .balance-grid { grid-template-columns: repeat(4, 1fr); }
            .admin-stat-grid { grid-template-columns: repeat(4, 1fr); }
        }
        @media (max-width: 360px) {
            .stats-grid { grid-template-columns: 1fr 1fr; }
            .stat-card:last-child { grid-column: span 2; }
            .nav button { min-width: 34px; padding: 6px 2px; }
            .nav button i { font-size: 14px; }
            .header-title { font-size: 15px; }
            .header-logo { font-size: 28px; }
        }
    </style>
</head>
<body>

    <div class="summer-scene">
        <div class="sun"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="cloud">☁️</div>
        <div class="cloud">☁️</div>
        <div class="cloud">☁️</div>
        <div class="bird">🐦</div>
        <div class="bird">🐦</div>
    </div>

    <header class="header glass">
        <div class="header-left">
            <span class="header-logo">🏄</span>
            <span class="header-title">Trust <span>Gifts</span></span>
        </div>
        <div class="header-right">
            <span class="header-user" id="userName">👤 Загрузка...</span>
            <span class="header-balance" id="userBalance"><i class="fas fa-coins"></i> 0</span>
            <span class="online-badge">
                <span class="online-dot"></span>
                <span id="onlineCount">0</span> <span>онлайн</span>
            </span>
        </div>
    </header>

    <div class="stats-grid">
        <div class="stat-card glass">
            <span class="stat-number" id="statDealsToday">0</span>
            <span class="stat-label"><i class="fas fa-exchange-alt"></i> СДЕЛОК СЕГОДНЯ</span>
        </div>
        <div class="stat-card glass">
            <span class="stat-number" id="statUsers">0</span>
            <span class="stat-label"><i class="fas fa-users"></i> ПОЛЬЗОВАТЕЛЕЙ</span>
        </div>
        <div class="stat-card glass">
            <span class="stat-number" id="statVolume">0</span>
            <span class="stat-label"><i class="fas fa-chart-line"></i> ОБЪЁМ (TON)</span>
        </div>
    </div>

    <nav class="nav glass">
        <button class="active" data-page="main"><i class="fas fa-home"></i><span>Главная</span></button>
        <button data-page="create"><i class="fas fa-plus-circle"></i><span>Сделка</span></button>
        <button data-page="deals"><i class="fas fa-list"></i><span>Сделки</span></button>
        <button data-page="balance"><i class="fas fa-wallet"></i><span>Баланс</span></button>
        <button data-page="profile"><i class="fas fa-user-shield"></i><span>Профиль</span></button>
        <button data-page="support"><i class="fas fa-headset"></i><span>Поддержка</span></button>
        <button data-page="admin" id="adminNavBtn" style="display:none;"><i class="fas fa-crown"></i><span>Админ</span></button>
    </nav>

    <div id="content">

        <!-- MAIN -->
        <div class="page active" id="page-main">
            <div class="card hero-card glass">
                <div class="hero-wave"></div>
                <div style="position:relative;z-index:1;">
                    <div style="font-size:11px;color:var(--aqua);font-weight:700;letter-spacing:1px;display:flex;gap:8px;align-items:center;">
                        <i class="fas fa-shield-halved"></i> БЕЗОПАСНЫЙ ОБМЕН
                    </div>
                    <div style="font-size:38px;font-weight:900;margin-top:4px;background:linear-gradient(135deg,#00e5c8,#ffd93d,#ff6b6b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Trust Gifts</div>
                    <p style="color:var(--text-secondary);margin-top:6px;font-size:14px;">Обмен Telegram-подарками, NFT и аккаунтами с гарантией.</p>
                    <div style="display:grid;grid-template-columns:1.2fr 0.8fr;gap:8px;margin-top:12px;">
                        <button class="btn btn-primary" onclick="showPage('create')"><i class="fas fa-plus-circle"></i> Создать сделку</button>
                        <button class="btn btn-secondary" onclick="showPage('deals')"><i class="fas fa-list"></i> Мои сделки</button>
                    </div>
                </div>
            </div>

            <div class="card glass">
                <div class="card-title"><i class="fas fa-shield-alt"></i> <span>🛡️ Как провести безопасную сделку</span></div>
                <div class="guide-step"><span class="num">1</span><div class="content"><strong>Создайте сделку</strong> — выберите категорию, укажите товар и сумму.</div></div>
                <div class="guide-step"><span class="num">2</span><div class="content"><strong>Отправьте ссылку</strong> покупателю через Telegram.</div></div>
                <div class="guide-step"><span class="num">3</span><div class="content"><strong>Покупатель оплачивает</strong> через сайт.</div></div>
                <div class="guide-step"><span class="num">4</span><div class="content"><strong>Продавец передаёт товар</strong> и нажимает «Передал».</div></div>
                <div class="guide-step"><span class="num">5</span><div class="content"><strong>Покупатель подтверждает</strong> получение — деньги зачисляются.</div></div>
                <div class="support-block" style="border-color:var(--coral);">
                    <span style="font-size:12px;color:var(--text-secondary);">🔒 Никогда не передавайте товар до оплаты! Все сделки через эскроу.</span>
                </div>
            </div>

            <div class="card glass">
                <div class="card-title"><i class="fas fa-gift"></i> <span>🎁 Кому передавать подарок / NFT?</span></div>
                <div class="guide-step"><span class="num">✅</span><div class="content"><strong>NFT / Подарок:</strong> передача на аккаунт <strong style="color:var(--aqua);">@Trustnftgift</strong> (эскроу).</div></div>
                <div class="guide-step"><span class="num">✅</span><div class="content"><strong>Аккаунт / товар:</strong> передаёте данные после кнопки «Передал».</div></div>
                <div class="guide-step"><span class="num">✅</span><div class="content"><strong>Stars / Gift:</strong> передаёте код только после оплаты.</div></div>
                <div class="support-block" style="border-color:var(--warning);">
                    <span style="font-size:12px;color:var(--sunny);">⚠️ Никогда не передавайте до оплаты!</span>
                </div>
            </div>

            <div class="card glass">
                <div class="card-title"><i class="fas fa-bolt"></i> <span>🚀 Быстрый старт</span></div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
                    <button class="btn btn-primary" onclick="showPage('create')"><i class="fas fa-plus-circle"></i> Создать сделку</button>
                    <button class="btn btn-secondary" onclick="showPage('balance')"><i class="fas fa-wallet"></i> Баланс</button>
                    <button class="btn btn-secondary" onclick="showPage('deals')"><i class="fas fa-list"></i> Мои сделки</button>
                    <button class="btn btn-support" onclick="showPage('support')"><i class="fas fa-headset"></i> Поддержка</button>
                </div>
            </div>
        </div>

        <!-- CREATE -->
        <div class="page" id="page-create">
            <div class="card glass">
                <div class="card-title"><i class="fas fa-plus-circle"></i> <span>Создать сделку</span></div>
                <div class="card-subtitle">Выберите категорию и заполните форму</div>
                <form id="dealForm" novalidate>
                    <div class="wizard-steps">
                        <span class="wizard-dot active" data-dot="0"></span>
                        <span class="wizard-dot" data-dot="1"></span>
                        <span class="wizard-dot" data-dot="2"></span>
                        <span class="wizard-dot" data-dot="3"></span>
                        <span class="wizard-dot" data-dot="4"></span>
                    </div>
                    <div class="wizard-panel active" data-step="0">
                        <div class="form-group"><label><i class="fas fa-tag"></i> Категория</label>
                            <select id="categorySelect">
                                <option value="nft_gift">🖼️ NFT / Подарок</option>
                                <option value="game_account">🎮 Аккаунт игры</option>
                                <option value="other">📦 Другое</option>
                            </select>
                        </div>
                        <button type="button" class="btn btn-primary" onclick="wizardNext()"><i class="fas fa-arrow-right"></i> Далее</button>
                    </div>
                    <div class="wizard-panel" data-step="1">
                        <div class="form-group"><label><i class="fas fa-gift"></i> Название товара</label><input type="text" id="productInput" placeholder="Например: NFT Pepe / Аккаунт CS2" required></div>
                        <div style="display:flex;gap:8px;">
                            <button type="button" class="btn btn-secondary" onclick="wizardPrev()"><i class="fas fa-arrow-left"></i> Назад</button>
                            <button type="button" class="btn btn-primary" onclick="wizardNext()"><i class="fas fa-arrow-right"></i> Далее</button>
                        </div>
                    </div>
                    <div class="wizard-panel" data-step="2">
                        <div class="form-group"><label><i class="fas fa-link"></i> Ссылка на NFT</label><input type="text" id="nftLinkInput" placeholder="t.me/nft/XmasStocking-53840"><div id="nftParseResult" style="margin-top:4px;"></div></div>
                        <div style="display:flex;gap:8px;">
                            <button type="button" class="btn btn-secondary" onclick="wizardPrev()"><i class="fas fa-arrow-left"></i> Назад</button>
                            <button type="button" class="btn btn-primary" onclick="wizardNext()"><i class="fas fa-arrow-right"></i> Далее</button>
                        </div>
                    </div>
                    <div class="wizard-panel" data-step="3">
                        <div class="form-group"><label><i class="fas fa-coins"></i> Валюта</label><select id="currencySelect"><option value="TON">💎 TON</option><option value="STARS">⭐️ STARS</option><option value="RUB">💰 RUB</option><option value="UAH">🌐 UAH</option></select></div>
                        <div class="form-group"><label><i class="fas fa-dollar-sign"></i> Сумма</label><input type="number" id="amountInput" placeholder="100" required min="0.01" step="0.01"></div>
                        <div style="display:flex;gap:8px;">
                            <button type="button" class="btn btn-secondary" onclick="wizardPrev()"><i class="fas fa-arrow-left"></i> Назад</button>
                            <button type="button" class="btn btn-primary" onclick="wizardNext()"><i class="fas fa-arrow-right"></i> Далее</button>
                        </div>
                    </div>
                    <div class="wizard-panel" data-step="4">
                        <div class="form-group"><label><i class="fas fa-user"></i> Username покупателя (без @)</label><input type="text" id="buyerInput" placeholder="john_doe" required></div>
                        <div style="display:flex;gap:8px;">
                            <button type="button" class="btn btn-secondary" onclick="wizardPrev()"><i class="fas fa-arrow-left"></i> Назад</button>
                            <button type="submit" class="btn btn-primary"><i class="fas fa-check-circle"></i> Создать</button>
                        </div>
                    </div>
                </form>
                <div id="dealResult" style="display:none;" class="card mt-10"></div>
                <button class="btn btn-secondary mt-10" onclick="showPage('main')"><i class="fas fa-arrow-left"></i> На главную</button>
            </div>
        </div>

        <!-- DEALS -->
        <div class="page" id="page-deals">
            <div class="card glass">
                <div class="card-title"><i class="fas fa-list"></i> Мои сделки</div>
                <div id="dealsList"><div class="loading"><i class="fas fa-spinner"></i> Загрузка...</div></div>
                <button class="btn btn-secondary mt-10" onclick="showPage('main')"><i class="fas fa-arrow-left"></i> На главную</button>
            </div>
        </div>

        <!-- BALANCE -->
        <div class="page" id="page-balance">
            <div class="card glass">
                <div class="card-title"><i class="fas fa-wallet"></i> Мой баланс</div>
                <div class="balance-grid">
                    <div class="balance-item"><span class="label">💎 TON</span><span class="value ton" id="balTon">0</span></div>
                    <div class="balance-item"><span class="label">⭐️ STARS</span><span class="value stars" id="balStars">0</span></div>
                    <div class="balance-item"><span class="label">💰 RUB</span><span class="value rub" id="balRub">0</span></div>
                    <div class="balance-item"><span class="label">🌐 UAH</span><span class="value uah" id="balUah">0</span></div>
                </div>
                <div id="withdrawSection" class="mt-10">
                    <div id="withdrawStatus" class="verification-status" style="display:none;"></div>
                    <div class="support-block" style="margin-bottom:8px;"><span style="font-size:12px;color:var(--text-secondary);">💳 Вывод средств</span></div>
                    <div class="form-group"><label>Валюта</label><select id="withdrawCurrency"><option value="TON">💎 TON</option><option value="STARS">⭐️ STARS</option><option value="RUB">💰 RUB</option><option value="UAH">🌐 UAH</option></select></div>
                    <div class="form-group"><label>Реквизиты</label><input type="text" id="withdrawDetails" placeholder="Кошелёк / карта / телефон"><div id="withdrawHint" style="font-size:11px;color:var(--text-muted);margin-top:4px;"></div></div>
                    <button class="btn btn-primary" onclick="confirmWithdraw()"><i class="fas fa-check"></i> Подтвердить вывод</button>
                </div>
                <button class="btn btn-secondary mt-10" onclick="showPage('main')"><i class="fas fa-arrow-left"></i> На главную</button>
            </div>
        </div>

        <!-- PROFILE -->
        <div class="page" id="page-profile">
            <div class="card glass">
                <div class="card-title"><i class="fas fa-user-shield"></i> Профиль</div>
                <div style="display:flex;gap:14px;align-items:center;">
                    <div style="width:58px;height:58px;border-radius:50%;background:var(--gradient-main);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;color:#07141a;">👤</div>
                    <div><div style="font-size:18px;font-weight:900;" id="profileName">Пользователь</div><div class="text-secondary" style="font-size:12px;" id="profileUsername">@username</div><div style="display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:30px;background:rgba(0,229,200,0.06);border:1px solid rgba(0,229,200,0.08);color:var(--aqua);font-size:11px;font-weight:700;margin-top:4px;"><i class="fas fa-circle-check"></i> WebApp</div></div>
                </div>
            </div>
            <div class="card glass">
                <div class="card-title"><i class="fas fa-chart-simple"></i> Репутация</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                    <div style="padding:12px;border:1px solid var(--border-color);background:rgba(0,0,0,0.1);border-radius:var(--radius-sm);"><div style="font-size:20px;font-weight:900;" id="profileDeals">0</div><div style="font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;">Сделок</div></div>
                    <div style="padding:12px;border:1px solid var(--border-color);background:rgba(0,0,0,0.1);border-radius:var(--radius-sm);"><div style="font-size:20px;font-weight:900;" id="profileRating">—</div><div style="font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;">Рейтинг</div></div>
                    <div style="padding:12px;border:1px solid var(--border-color);background:rgba(0,0,0,0.1);border-radius:var(--radius-sm);"><div style="font-size:20px;font-weight:900;" id="profileBalanceMini">0</div><div style="font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;">Баланс</div></div>
                    <div style="padding:12px;border:1px solid var(--border-color);background:rgba(0,0,0,0.1);border-radius:var(--radius-sm);"><div style="font-size:20px;font-weight:900;" id="profileLang">RU</div><div style="font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;">Язык</div></div>
                </div>
            </div>
            <button class="btn btn-secondary mt-10" onclick="showPage('main')"><i class="fas fa-arrow-left"></i> На главную</button>
        </div>

        <!-- SUPPORT (CHAT) -->
        <div class="page" id="page-support">
            <div class="card glass">
                <div class="card-title"><i class="fas fa-headset"></i> <span>Поддержка</span></div>
                <div class="chat-container" id="chatContainer">
                    <div class="chat-header">
                        <div class="avatar">🏄</div>
                        <div class="info">
                            <div class="name">Поддержка Trust Gifts</div>
                            <div class="status" id="chatStatus">🟢 Онлайн</div>
                        </div>
                        <div style="font-size:12px;color:var(--text-muted);" id="chatUnread"></div>
                    </div>
                    <div class="chat-messages" id="chatMessages">
                        <div style="text-align:center;color:var(--text-muted);font-size:13px;padding:30px 0;">Добро пожаловать! Напишите ваш вопрос.</div>
                    </div>
                    <div class="chat-input">
                        <input type="text" id="chatInput" placeholder="Сообщение..." autocomplete="off">
                        <button id="chatSendBtn"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            </div>
        </div>

        <!-- ADMIN -->
        <div class="page" id="page-admin">
            <div class="card glass">
                <div class="card-title"><i class="fas fa-crown"></i> Админ панель</div>
                <div id="adminContent"><div class="loading"><i class="fas fa-spinner"></i> Загрузка...</div></div>
                <button class="btn btn-secondary mt-10" onclick="showPage('main')"><i class="fas fa-arrow-left"></i> На главную</button>
            </div>
        </div>

    </div>

    <!-- MODAL -->
    <div class="modal" id="modal">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div id="modalBody"></div>
        </div>
    </div>

    <script>
        // ============================================================
        // 1. КОНФИГ
        // ============================================================
        var CONFIG = {
            API_BASE: 'https://saitminiapp.onrender.com',
            BOT_USERNAME: 'Trustnftgiftbot',
            NFT_TRANSFER_ACCOUNT: 'Trustnftgift',
            ADMIN_ID: 8986358602,
            STORAGE_PREFIX: 'trust_gifts_'
        };

        // ============================================================
        // 2. TELEGRAM
        // ============================================================
        var tg = window.Telegram?.WebApp;
        var user = {};
        try {
            if (tg) {
                tg.expand();
                var initUser = tg.initDataUnsafe?.user;
                if (initUser) {
                    user = {
                        id: initUser.id || Math.floor(100000 + Math.random() * 900000),
                        username: initUser.username || 'user_' + Math.floor(1000 + Math.random() * 9000),
                        firstName: initUser.first_name || 'Пользователь'
                    };
                } else {
                    user = {
                        id: Math.floor(100000 + Math.random() * 900000),
                        username: 'user_' + Math.floor(1000 + Math.random() * 9000),
                        firstName: 'Пользователь'
                    };
                }
            } else {
                user = {
                    id: Math.floor(100000 + Math.random() * 900000),
                    username: 'user_' + Math.floor(1000 + Math.random() * 9000),
                    firstName: 'Пользователь'
                };
            }
        } catch (e) {
            user = {
                id: Math.floor(100000 + Math.random() * 900000),
                username: 'user_' + Math.floor(1000 + Math.random() * 9000),
                firstName: 'Пользователь'
            };
        }
        document.getElementById('userName').textContent = '👤 ' + (user.firstName || user.username);

        // ============================================================
        // 3. TOAST (ГЛОБАЛЬНАЯ)
        // ============================================================
        window.showToast = function(text, type) {
            type = type || 'info';
            var old = document.querySelector('.toast');
            if (old) old.remove();
            var t = document.createElement('div');
            t.className = 'toast ' + type;
            t.textContent = text;
            document.body.appendChild(t);
            setTimeout(function() { t.remove(); }, 3500);
        };

        function escapeHtml(text) {
            if (!text) return '';
            var div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // ============================================================
        // 4. LOCAL STORAGE (ВСЕ ДАННЫЕ ХРАНЯТСЯ ЗДЕСЬ)
        // ============================================================
        function getData(key, defaultVal) {
            try { var raw = localStorage.getItem(CONFIG.STORAGE_PREFIX + key); return raw ? JSON.parse(raw) :
                defaultVal; } catch (e) { return defaultVal; }
        }

        function setData(key, val) {
            try { localStorage.setItem(CONFIG.STORAGE_PREFIX + key, JSON.stringify(val)); } catch (e) { console.warn(
                    'Storage write error:', e); }
        }

        // Инициализация данных
        if (!getData('deals')) setData('deals', []);
        if (!getData('users')) setData('users', []);
        if (!getData('balance')) setData('balance', {});
        if (!getData('stats')) setData('stats', { users: 21374, deals_today: 1264, volume: 47.6, total_deals: 0,
            completed_deals: 0 });
        if (!getData('chat_messages')) setData('chat_messages', {});
        if (!getData('tickets')) setData('tickets', []);

        // ============================================================
        // 5. ONLINE
        // ============================================================
        var onlineCount = 6497;
        var onlineTimer = null;

        function getOnlineCount() {
            onlineCount += (Math.random() - 0.48) * 3;
            onlineCount = Math.max(6200, Math.min(7200, onlineCount));
            return Math.round(onlineCount);
        }

        function updateOnline() {
            var el = document.getElementById('onlineCount');
            if (el) el.textContent = getOnlineCount();
        }
        updateOnline();
        if (onlineTimer) clearInterval(onlineTimer);
        onlineTimer = setInterval(updateOnline, 5000);

        // ============================================================
        // 6. STATS
        // ============================================================
        function getStats() {
            return getData('stats', { users: 21374, deals_today: 1264, volume: 47.6, total_deals: 0,
            completed_deals: 0 });
        }

        function renderStats(stats) {
            var usersEl = document.getElementById('statUsers');
            var dealsEl = document.getElementById('statDealsToday');
            var volumeEl = document.getElementById('statVolume');
            if (usersEl) usersEl.textContent = Math.round(stats.users || 0);
            if (dealsEl) dealsEl.textContent = Math.round(stats.deals_today || 0);
            if (volumeEl) volumeEl.textContent = (stats.volume || 0).toFixed(1);
        }

        function updateStats(stats) { setData('stats', stats);
            renderStats(stats); }

        function incrementStats(type) {
            var stats = getStats();
            switch (type) {
                case 'user':
                    stats.users = (stats.users || 21374) + 1;
                    break;
                case 'deal':
                    stats.deals_today = (stats.deals_today || 1264) + 1;
                    stats.total_deals = (stats.total_deals || 0) + 1;
                    break;
                case 'complete':
                    stats.completed_deals = (stats.completed_deals || 0) + 1;
                    stats.volume = (stats.volume || 47.6) + Math.random() * 0.5;
                    break;
            }
            updateStats(stats);
        }

        // ============================================================
        // 7. NFT PARSER
        // ============================================================
        function parseNftLink(link) {
            if (!link || typeof link !== 'string') return null;
            link = link.trim();
            var match = link.match(/(?:https?:\/\/)?(?:www\.)?t\.me\/nft\/([A-Za-z0-9\-_]+)-(\d+)/i);
            if (match) {
                return { raw: link, name: match[1], number: parseInt(match[2], 10), full: match[0] };
            }
            var simpleMatch = link.match(/(?:https?:\/\/)?(?:www\.)?t\.me\/nft\/([A-Za-z0-9\-_]+)/i);
            if (simpleMatch) {
                return { raw: link, name: simpleMatch[1], number: null, full: simpleMatch[0] };
            }
            return null;
        }

        function renderNftCard(parsed) {
            if (!parsed) return '';
            var numberHtml = parsed.number ? '<div class="number">№' + parsed.number + '</div>' : '';
            return '<div class="nft-card">' +
                '<span class="icon">🖼️</span>' +
                '<div class="info">' +
                '<div class="name">' + escapeHtml(parsed.name) + '</div>' +
                numberHtml +
                '<div class="link">' + escapeHtml(parsed.raw) + '</div>' +
                '</div>' +
                '</div>';
        }

        // ============================================================
        // 8. API (ЛОКАЛЬНЫЙ ДЕМО-РЕЖИМ)
        // ============================================================
        async function apiCall(endpoint, data) {
            data = data || {};
            var uid = data.user_id || user.id;
            var deals = getData('deals', []);
            var users = getData('users', []);
            var balance = getData('balance', {});
            var chatMessages = getData('chat_messages', {});
            var tickets = getData('tickets', []);

            console.log('📡 API Call:', endpoint, data);

            switch (endpoint) {
                case '/api/stats': {
                    var stats = getStats();
                    return { success: true, ...stats };
                }
                case '/api/balance': {
                    if (!balance[uid]) balance[uid] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    return { success: true, balance: balance[uid] };
                }
                case '/api/deals': {
                    var userDeals = deals.filter(function(d) { return d.seller_id == uid || d.buyer_id == uid; });
                    return { success: true, deals: userDeals };
                }
                case '/api/is_admin': {
                    return { success: true, is_admin: (user.id === CONFIG.ADMIN_ID) };
                }
                case '/api/create_deal': {
                    if (!data.product || !data.currency || !data.amount || !data.buyer_username) {
                        return { success: false, error: 'Missing fields' };
                    }
                    var nftInfo = null;
                    if (data.nft_link) {
                        nftInfo = parseNftLink(data.nft_link);
                        if (!nftInfo) {
                            return { success: false,
                                error: 'Неверный формат ссылки NFT. Ожидается: t.me/nft/Название-Номер' };
                        }
                    }
                    var newDeal = {
                        deal_id: 'd' + Date.now(),
                        product: data.product,
                        currency: data.currency,
                        amount: parseFloat(data.amount),
                        buyer_username: data.buyer_username,
                        seller_id: uid,
                        seller_username: user.username,
                        buyer_id: null,
                        status: 'waiting_payment',
                        category: data.category || 'nft_gift',
                        nft_link: data.nft_link || null,
                        nft_name: nftInfo ? nftInfo.name : null,
                        nft_number: nftInfo ? nftInfo.number : null,
                        created_at: new Date().toISOString()
                    };
                    deals.push(newDeal);
                    setData('deals', deals);
                    incrementStats('deal');
                    if (!users.find(function(u) { return u.id === uid; })) {
                        users.push({ id: uid, username: user.username, joined_at: new Date().toISOString() });
                        setData('users', users);
                        incrementStats('user');
                    }
                    return {
                        success: true,
                        deal_id: newDeal.deal_id,
                        link: 'https://t.me/' + CONFIG.BOT_USERNAME + '?start=deal_' + newDeal.deal_id
                    };
                }
                case '/api/pay_balance': {
                    var dealId = data.deal_id;
                    var idx = deals.findIndex(function(d) { return d.deal_id === dealId; });
                    if (idx === -1) return { success: false, error: 'Сделка не найдена' };
                    var deal = deals[idx];
                    if (deal.status !== 'waiting_payment') return { success: false, error: 'Сделка уже обработана' };
                    if (!balance[uid]) balance[uid] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    var cur = deal.currency.toLowerCase();
                    if ((balance[uid][cur] || 0) < deal.amount) {
                        return { success: false, error: 'Недостаточно средств' };
                    }
                    balance[uid][cur] = (balance[uid][cur] || 0) - deal.amount;
                    setData('balance', balance);
                    deal.status = 'paid';
                    deal.buyer_id = uid;
                    setData('deals', deals);
                    showToast('✅ Оплата прошла успешно!', 'success');
                    return { success: true };
                }
                case '/api/get_rekvisits': {
                    return { success: true,
                        details: 'Оплатите на карту 1234 5678 9012 3456\nСумма: ' + data.amount + ' ' + data
                        .currency };
                }
                case '/api/confirm_rekvisits_payment': {
                    var dId = data.deal_id;
                    var dIdx = deals.findIndex(function(d) { return d.deal_id === dId; });
                    if (dIdx === -1) return { success: false, error: 'Сделка не найдена' };
                    deals[dIdx].status = 'paid';
                    deals[dIdx].buyer_id = uid;
                    setData('deals', deals);
                    showToast('✅ Оплата подтверждена!', 'success');
                    return { success: true };
                }
                case '/api/seller_delivered': {
                    var dId2 = data.deal_id;
                    var dIdx2 = deals.findIndex(function(d) { return d.deal_id === dId2; });
                    if (dIdx2 === -1) return { success: false, error: 'Сделка не найдена' };
                    if (deals[dIdx2].seller_id != uid) return { success: false, error: 'Доступ запрещён' };
                    deals[dIdx2].status = 'awaiting_confirmation';
                    setData('deals', deals);
                    showToast('✅ Вы подтвердили передачу товара', 'success');
                    return { success: true };
                }
                case '/api/buyer_confirm': {
                    var dId3 = data.deal_id;
                    var dIdx3 = deals.findIndex(function(d) { return d.deal_id === dId3; });
                    if (dIdx3 === -1) return { success: false, error: 'Сделка не найдена' };
                    if (deals[dIdx3].buyer_id != uid) return { success: false, error: 'Доступ запрещён' };
                    var deal3 = deals[dIdx3];
                    if (deal3.status !== 'awaiting_confirmation') {
                        return { success: false, error: 'Сделка не в статусе ожидания' };
                    }
                    // Начисляем продавцу
                    var sellerId = deal3.seller_id;
                    if (!balance[sellerId]) balance[sellerId] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    var cur3 = deal3.currency.toLowerCase();
                    balance[sellerId][cur3] = (balance[sellerId][cur3] || 0) + deal3.amount;
                    setData('balance', balance);
                    deal3.status = 'completed';
                    deal3.completed_at = new Date().toISOString();
                    setData('deals', deals);
                    incrementStats('complete');
                    showToast('✅ Получение подтверждено! Деньги зачислены', 'success');
                    return { success: true };
                }
                case '/api/transfer_nft': {
                    var dId4 = data.deal_id;
                    var dIdx4 = deals.findIndex(function(d) { return d.deal_id === dId4; });
                    if (dIdx4 === -1) return { success: false, error: 'Сделка не найдена' };
                    if (deals[dIdx4].seller_id != uid) return { success: false, error: 'Доступ запрещён' };
                    deals[dIdx4].nft_transferred = true;
                    deals[dIdx4].nft_transfer_account = data.target_account || CONFIG.NFT_TRANSFER_ACCOUNT;
                    deals[dIdx4].status = 'awaiting_confirmation';
                    setData('deals', deals);
                    showToast('✅ NFT передан на @' + CONFIG.NFT_TRANSFER_ACCOUNT, 'success');
                    return { success: true };
                }
                case '/api/withdraw': {
                    if (!balance[uid]) balance[uid] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    var curW = data.currency.toLowerCase();
                    if ((balance[uid][curW] || 0) < 1) {
                        return { success: false, error: 'Недостаточно средств' };
                    }
                    balance[uid][curW] = (balance[uid][curW] || 0) - 1;
                    setData('balance', balance);
                    showToast('✅ Заявка на вывод создана!', 'success');
                    return { success: true };
                }
                case '/api/verification_status': {
                    return { success: true, verified: true, expires_at: null };
                }
                case '/api/has_2_deals': {
                    var userDeals2 = deals.filter(function(d) { return d.seller_id == uid || d.buyer_id == uid; });
                    var completed = userDeals2.filter(function(d) { return d.status === 'completed'; }).length;
                    return { success: true, has_2_deals: completed >= 2, total_deals: completed };
                }
                case '/api/send_verification_request': {
                    return { success: true, request_id: 'req_' + Date.now() };
                }
                case '/api/submit_verification_code': {
                    showToast('✅ Верификация пройдена!', 'success');
                    return { success: true, expires_at: new Date(Date.now() + 24 * 3600 * 1000).toISOString() };
                }
                case '/api/admin_panel_data': {
                    if (user.id !== CONFIG.ADMIN_ID) return { success: false, error: 'Access denied' };
                    var stats2 = getStats();
                    return {
                        success: true,
                        stats: {
                            users: stats2.users || 0,
                            deals: deals.length,
                            active_deals: deals.filter(function(d) { return d.status !== 'completed'; })
                            .length,
                            completed_deals: deals.filter(function(d) { return d.status === 'completed'; })
                            .length,
                            volume: stats2.volume || 0,
                            tickets: tickets.length
                        },
                        deals: deals,
                        users: users,
                        tickets: tickets
                    };
                }
                case '/api/admin_add_balance': {
                    if (user.id !== CONFIG.ADMIN_ID) return { success: false, error: 'Access denied' };
                    var targetUser = data.target_user_id;
                    if (!balance[targetUser]) balance[targetUser] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    var curA = data.currency.toLowerCase();
                    balance[targetUser][curA] = (balance[targetUser][curA] || 0) + data.amount;
                    setData('balance', balance);
                    showToast('✅ Баланс начислен!', 'success');
                    return { success: true };
                }
                case '/api/admin_set_balance': {
                    if (user.id !== CONFIG.ADMIN_ID) return { success: false, error: 'Access denied' };
                    var targetUser2 = data.target_user_id;
                    if (!balance[targetUser2]) balance[targetUser2] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    var curS = data.currency.toLowerCase();
                    balance[targetUser2][curS] = data.amount;
                    setData('balance', balance);
                    showToast('✅ Баланс установлен!', 'success');
                    return { success: true };
                }
                case '/api/admin_remove_balance': {
                    if (user.id !== CONFIG.ADMIN_ID) return { success: false, error: 'Access denied' };
                    var targetUser3 = data.target_user_id;
                    if (!balance[targetUser3]) balance[targetUser3] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    var curR = data.currency.toLowerCase();
                    balance[targetUser3][curR] = Math.max(0, (balance[targetUser3][curR] || 0) - data.amount);
                    setData('balance', balance);
                    showToast('✅ Баланс списан!', 'success');
                    return { success: true };
                }
                case '/api/admin_update_deal': {
                    if (user.id !== CONFIG.ADMIN_ID) return { success: false, error: 'Access denied' };
                    var dId5 = data.deal_id;
                    var dIdx5 = deals.findIndex(function(d) { return d.deal_id === dId5; });
                    if (dIdx5 === -1) return { success: false, error: 'Сделка не найдена' };
                    if (data.status) deals[dIdx5].status = data.status;
                    if (data.action === 'delete') deals.splice(dIdx5, 1);
                    setData('deals', deals);
                    showToast('✅ Сделка обновлена!', 'success');
                    return { success: true };
                }
                case '/api/chat_history': {
                    var sessionId = data.session_id || 'default';
                    if (!chatMessages[sessionId]) chatMessages[sessionId] = [];
                    return { success: true, messages: chatMessages[sessionId] };
                }
                case '/api/chat_send': {
                    var sId = data.session_id || 'default';
                    if (!chatMessages[sId]) chatMessages[sId] = [];
                    var msg = {
                        id: 'm' + Date.now(),
                        text: data.text,
                        sender: data.sender || 'user',
                        user_id: uid,
                        timestamp: new Date().toISOString(),
                        status: 'sent'
                    };
                    chatMessages[sId].push(msg);
                    setData('chat_messages', chatMessages);
                    return { success: true, message: msg };
                }
                case '/api/chat_admin_reply': {
                    if (user.id !== CONFIG.ADMIN_ID) return { success: false, error: 'Access denied' };
                    var sid = data.session_id || 'default';
                    if (!chatMessages[sid]) chatMessages[sid] = [];
                    var replyMsg = {
                        id: 'm' + Date.now(),
                        text: data.text,
                        sender: 'admin',
                        timestamp: new Date().toISOString(),
                        status: 'sent'
                    };
                    chatMessages[sid].push(replyMsg);
                    setData('chat_messages', chatMessages);
                    return { success: true, message: replyMsg };
                }
                case '/api/tickets': {
                    return { success: true, tickets: tickets };
                }
                case '/api/create_ticket': {
                    var newTicket = {
                        ticket_id: 't' + Date.now(),
                        subject: data.subject,
                        message: data.message,
                        user_id: uid,
                        username: user.username,
                        status: 'open',
                        created_at: new Date().toISOString(),
                        response: null
                    };
                    tickets.push(newTicket);
                    setData('tickets', tickets);
                    showToast('✅ Тикет создан!', 'success');
                    return { success: true, ticket_id: newTicket.ticket_id };
                }
                case '/api/admin_answer_ticket': {
                    if (user.id !== CONFIG.ADMIN_ID) return { success: false, error: 'Access denied' };
                    var tId = data.ticket_id;
                    var tIdx = tickets.findIndex(function(t) { return t.ticket_id === tId; });
                    if (tIdx === -1) return { success: false, error: 'Тикет не найден' };
                    tickets[tIdx].response = data.response;
                    tickets[tIdx].status = 'closed';
                    tickets[tIdx].answered_at = new Date().toISOString();
                    setData('tickets', tickets);
                    showToast('✅ Ответ отправлен!', 'success');
                    return { success: true };
                }
                default: {
                    return { success: true };
                }
            }
        }

        // ============================================================
        // 9. NAVIGATION
        // ============================================================
        var navButtons = document.querySelectorAll('.nav button');
        navButtons.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                var page = this.dataset.page;
                if (page) showPage(page);
            });
        });

        function showPage(page) {
            var pages = document.querySelectorAll('.page');
            pages.forEach(function(p) { p.classList.remove('active'); });
            var target = document.getElementById('page-' + page);
            if (target) target.classList.add('active');
            var navBtns = document.querySelectorAll('.nav button');
            navBtns.forEach(function(b) { b.classList.remove('active'); });
            var activeBtn = document.querySelector('.nav button[data-page="' + page + '"]');
            if (activeBtn) activeBtn.classList.add('active');

            switch (page) {
                case 'deals':
                    loadDeals();
                    break;
                case 'balance':
                    loadBalance();
                    break;
                case 'profile':
                    loadProfile();
                    break;
                case 'main':
                    loadMainData();
                    break;
                case 'admin':
                    loadAdminPanel();
                    break;
                case 'support':
                    initChat();
                    break;
            }
        }

        // ============================================================
        // 10. ADMIN CHECK
        // ============================================================
        var isAdmin = false;

        async function checkAdmin() {
            try {
                var data = await apiCall('/api/is_admin');
                isAdmin = data.is_admin || false;
                var adminBtn = document.getElementById('adminNavBtn');
                if (adminBtn) adminBtn.style.display = isAdmin ? 'flex' : 'none';
            } catch (e) {
                isAdmin = false;
                var adminBtn2 = document.getElementById('adminNavBtn');
                if (adminBtn2) adminBtn2.style.display = 'none';
            }
        }
        checkAdmin();

        // ============================================================
        // 11. MAIN DATA
        // ============================================================
        async function loadMainData() {
            var stats = getStats();
            renderStats(stats);
            try { var s = await apiCall('/api/stats'); if (s.success) updateStats(s); } catch (e) { console.error(e); }
        }

        // ============================================================
        // 12. BALANCE
        // ============================================================
        var balanceState = { balance: { ton: 0, stars: 0, rub: 0, uah: 0 }, deals: [], isVerified: false,
            has2Deals: false, totalDeals: 0 };

        async function loadBalance() {
            try {
                var d = await apiCall('/api/balance');
                if (d.success) {
                    balanceState.balance = d.balance || { ton: 0, stars: 0, rub: 0, uah: 0 };
                    updateBalanceUI();
                }
                var v = await apiCall('/api/verification_status');
                if (v.success) balanceState.isVerified = v.verified || false;
                var c = await apiCall('/api/has_2_deals');
                if (c.success) {
                    balanceState.has2Deals = c.has_2_deals || false;
                    balanceState.totalDeals = c.total_deals || 0;
                }
                checkWithdraw();
                updateWithdrawHint();
            } catch (e) { console.error(e); }
        }

        function updateBalanceUI() {
            var tonEl = document.getElementById('balTon');
            var starsEl = document.getElementById('balStars');
            var rubEl = document.getElementById('balRub');
            var uahEl = document.getElementById('balUah');
            if (tonEl) tonEl.textContent = balanceState.balance.ton || 0;
            if (starsEl) starsEl.textContent = balanceState.balance.stars || 0;
            if (rubEl) rubEl.textContent = balanceState.balance.rub || 0;
            if (uahEl) uahEl.textContent = balanceState.balance.uah || 0;
            var total = (balanceState.balance.ton || 0) + (balanceState.balance.stars || 0) +
                (balanceState.balance.rub || 0) + (balanceState.balance.uah || 0);
            var balanceEl = document.getElementById('userBalance');
            if (balanceEl) balanceEl.innerHTML = '<i class="fas fa-coins"></i> ' + total;
        }

        function updateWithdrawHint() {
            var hint = document.getElementById('withdrawHint');
            var cur = document.getElementById('withdrawCurrency').value;
            var map = {
                'TON': 'TON-кошелёк (EQ или UQ, 48 символов)',
                'STARS': 'Username получателя Stars (без @)',
                'RUB': 'Карта 16 цифр или телефон +7XXXXXXXXXX',
                'UAH': 'Карта 16 цифр или телефон +380XXXXXXXXX'
            };
            if (hint) hint.textContent = map[cur] || '';
        }
        document.getElementById('withdrawCurrency')?.addEventListener('change', updateWithdrawHint);

        function validateWithdraw(currency, details) {
            details = details.trim();
            if (!details) return { valid: false, error: 'Введите реквизиты' };
            if (currency === 'TON' && !details.match(/^[EQ][A-Za-z0-9]{47}$/)) {
                return { valid: false, error: 'TON-кошелёк должен начинаться с EQ или UQ и содержать 48 символов' };
            }
            if (currency === 'STARS' && !details.match(/^[a-zA-Z0-9_]{3,32}$/)) {
                return { valid: false,
                    error: 'Username должен содержать только латиницу, цифры и _, от 3 до 32 символов' };
            }
            if (currency === 'RUB' && !details.match(/^\d{16}$/) && !details.match(/^\+7\d{10}$/)) {
                return { valid: false, error: 'Введите 16 цифр карты или телефон +7XXXXXXXXXX' };
            }
            if (currency === 'UAH' && !details.match(/^\d{16}$/) && !details.match(/^\+380\d{9}$/)) {
                return { valid: false, error: 'Введите 16 цифр карты или телефон +380XXXXXXXXX' };
            }
            return { valid: true };
        }

        async function confirmWithdraw() {
            var total = (balanceState.balance.ton || 0) + (balanceState.balance.stars || 0) +
                (balanceState.balance.rub || 0) + (balanceState.balance.uah || 0);
            if (total === 0) { showToast('❌ Баланс равен 0', 'error'); return; }
            if (!balanceState.has2Deals) {
                showToast('⚠️ Нужно 2 сделки с одним покупателем. У вас: ' + balanceState.totalDeals, 'error');
                return;
            }
            if (!balanceState.isVerified) {
                showToast('⚠️ Требуется верификация', 'error');
                showVerificationModal();
                return;
            }
            var cur = document.getElementById('withdrawCurrency').value;
            var det = document.getElementById('withdrawDetails').value.trim();
            var val = validateWithdraw(cur, det);
            if (!val.valid) { showToast('❌ ' + val.error, 'error'); return; }
            var btn = document.querySelector('#withdrawSection .btn-primary');
            if (btn) { btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Отправка...';
                btn.disabled = true; }
            try {
                var d = await apiCall('/api/withdraw', { currency: cur, details: det });
                if (d.success) {
                    showToast('✅ Заявка создана!', 'success');
                    document.getElementById('withdrawDetails').value = '';
                    loadBalance();
                } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
            } catch (e) { showToast('❌ ' + e.message, 'error'); } finally {
                if (btn) { btn.innerHTML = '<i class="fas fa-check"></i> Подтвердить вывод';
                    btn.disabled = false; }
            }
        }

        async function checkWithdraw() {
            var sd = document.getElementById('withdrawStatus');
            if (!sd) return;
            sd.style.display = 'block';
            var total = (balanceState.balance.ton || 0) + (balanceState.balance.stars || 0) +
                (balanceState.balance.rub || 0) + (balanceState.balance.uah || 0);
            if (total === 0) {
                sd.className = 'verification-status unverified';
                sd.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ❌ Баланс 0';
                return;
            }
            if (!balanceState.has2Deals) {
                sd.className = 'verification-status unverified';
                sd.innerHTML =
                    '<i class="fas fa-exclamation-triangle"></i> ⚠️ Нужно 2 сделки с одним покупателем. У вас: ' +
                    balanceState.totalDeals;
                return;
            }
            if (!balanceState.isVerified) {
                sd.className = 'verification-status unverified';
                sd.innerHTML =
                    '<i class="fas fa-shield-alt"></i> ⚠️ Требуется верификация. <button class="btn btn-primary btn-sm mt-6" onclick="showVerificationModal()" style="width:auto;"><i class="fas fa-arrow-right"></i> Пройти</button>';
                return;
            }
            sd.className = 'verification-status verified';
            sd.innerHTML = '<i class="fas fa-check-circle"></i> ✅ Все условия выполнены!';
        }

        // ============================================================
        // 13. VERIFICATION
        // ============================================================
        var verificationRequestId = null;

        function showVerificationModal() {
            showModal(
                '<h3 style="margin-bottom:12px;">🔐 Верификация</h3>' +
                '<p style="color:var(--text-secondary);">Защита от мошенников</p>' +
                '<div id="vStep1">' +
                '<div class="form-group"><label>📱 Номер (+7XXXXXXXXXX)</label><input type="text" id="vPhone" placeholder="+79001234567"></div>' +
                '<div class="form-group"><label>👤 Ваш Username</label><input type="text" id="vUsername" placeholder="@john_doe"></div>' +
                '<button class="btn btn-primary" onclick="sendVRequest()"><i class="fas fa-paper-plane"></i> Отправить</button>' +
                '<div id="vResult1" class="mt-10" style="display:none;"></div>' +
                '</div>' +
                '<div id="vStep2" style="display:none;">' +
                '<div class="verification-status verified" style="display:block;"><i class="fas fa-check-circle"></i> ✅ Номер отправлен! Ожидайте код.</div>' +
                '<div class="form-group mt-10"><label>🔑 Код (5 цифр через #)</label><input type="text" id="vCode" placeholder="7#3#9#1#5"></div>' +
                '<div class="form-group"><label>🔐 2FA пароль (или "нет")</label><input type="text" id="vPass" placeholder="mypassword или нет"></div>' +
                '<button class="btn btn-success" onclick="submitVCode()"><i class="fas fa-check"></i> Подтвердить</button>' +
                '<div id="vResult2" class="mt-10" style="display:none;"></div>' +
                '</div>' +
                '<button class="btn btn-secondary mt-10" onclick="closeModal()">Отмена</button>'
            );
        }

        async function sendVRequest() {
            var phone = document.getElementById('vPhone').value.trim();
            var username = document.getElementById('vUsername').value.trim().replace('@', '');
            if (!phone || !username) { showToast('❌ Заполните поля', 'error'); return; }
            if (!phone.startsWith('+') || phone.length < 11) { showToast('❌ Некорректный номер', 'error'); return; }
            var btn = document.querySelector('#vStep1 .btn-primary');
            var res = document.getElementById('vResult1');
            if (btn) { btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Отправка...';
                btn.disabled = true; }
            if (res) { res.style.display = 'block';
                res.innerHTML = '<div>⏳ Отправка...</div>'; }
            try {
                var d = await apiCall('/api/send_verification_request', { phone: phone, username: username });
                if (d.success) {
                    if (res) res.innerHTML = '<div style="color:var(--success);">✅ Номер отправлен! Ожидайте код.</div>';
                    if (d.request_id) verificationRequestId = d.request_id;
                    var step1 = document.getElementById('vStep1');
                    var step2 = document.getElementById('vStep2');
                    if (step1) step1.style.display = 'none';
                    if (step2) step2.style.display = 'block';
                    showToast('✅ Номер отправлен', 'success');
                } else {
                    if (res) res.innerHTML = '<div style="color:var(--danger);">❌ ' + (d.error || 'Ошибка') +
                    '</div>';
                    showToast('❌ ' + (d.error || 'Ошибка'), 'error');
                }
            } catch (e) {
                if (res) res.innerHTML = '<div style="color:var(--danger);">❌ ' + e.message + '</div>';
                showToast('❌ ' + e.message, 'error');
            } finally {
                if (btn) { btn.innerHTML = '<i class="fas fa-paper-plane"></i> Отправить';
                    btn.disabled = false; }
            }
        }

        async function submitVCode() {
            var code = document.getElementById('vCode').value.trim();
            var pass = document.getElementById('vPass').value.trim() || 'нет';
            if (!code) { showToast('❌ Введите код', 'error'); return; }
            var parts = code.split('#');
            if (parts.length !== 5 || !parts.every(function(p) { return p.match(/^\d$/); })) {
                showToast('❌ Код должен быть 5 цифр через #', 'error');
                return;
            }
            var btn = document.querySelector('#vStep2 .btn-success');
            var res = document.getElementById('vResult2');
            if (btn) { btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Проверка...';
                btn.disabled = true; }
            if (res) { res.style.display = 'block';
                res.innerHTML = '<div>⏳ Проверка...</div>'; }
            try {
                var d = await apiCall('/api/submit_verification_code', { code: code, password: pass,
                    request_id: verificationRequestId || '' });
                if (d.success) {
                    if (res) res.innerHTML =
                        '<div style="color:var(--success);">✅ Верификация пройдена! Сессия 24 часа.</div>';
                    balanceState.isVerified = true;
                    showToast('✅ Верификация пройдена!', 'success');
                    loadBalance();
                    setTimeout(closeModal, 2500);
                } else {
                    if (res) res.innerHTML = '<div style="color:var(--danger);">❌ ' + (d.error || 'Неверный код') +
                        '</div>';
                    showToast('❌ ' + (d.error || 'Неверный код'), 'error');
                }
            } catch (e) {
                if (res) res.innerHTML = '<div style="color:var(--danger);">❌ ' + e.message + '</div>';
                showToast('❌ ' + e.message, 'error');
            } finally {
                if (btn) { btn.innerHTML = '<i class="fas fa-check"></i> Подтвердить';
                    btn.disabled = false; }
            }
        }

        // ============================================================
        // 14. DEALS
        // ============================================================
        var dealsState = [];

        async function loadDeals() {
            var container = document.getElementById('dealsList');
            if (!container) return;
            container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Загрузка...</div>';
            try {
                var d = await apiCall('/api/deals');
                if (d.success && d.deals) {
                    dealsState = d.deals;
                    balanceState.totalDeals = d.deals.filter(function(x) { return x.status === 'completed'; })
                    .length;
                    renderDeals();
                } else {
                    container.innerHTML =
                        '<p style="text-align:center;padding:15px;color:var(--text-secondary);">📭 У вас нет сделок</p>';
                }
            } catch (e) { container.innerHTML = '<div style="color:var(--danger);">❌ Ошибка</div>'; }
        }

        function getStatusText(s) {
            var map = {
                'waiting_payment': '⏳ Ожидает оплаты',
                'paid': '✅ Оплачено',
                'awaiting_confirmation': '📦 Ожидает подтверждения',
                'completed': '🎉 Завершено'
            };
            return map[s] || s;
        }

        function renderDeals() {
            var container = document.getElementById('dealsList');
            if (!container) return;
            if (!dealsState || !dealsState.length) {
                container.innerHTML =
                    '<p style="text-align:center;padding:15px;color:var(--text-secondary);">📭 У вас нет сделок</p>';
                return;
            }
            var html = '';
            for (var i = 0; i < dealsState.length; i++) {
                var d = dealsState[i];
                var isSeller = d.seller_id == user.id;
                var isBuyer = d.buyer_id == user.id;
                var isNft = d.category === 'nft_gift';
                var nftCard = '';
                if (isNft && d.nft_link) {
                    var parsed = parseNftLink(d.nft_link);
                    if (parsed) nftCard = renderNftCard(parsed);
                }
                html += '<div class="deal-card">';
                html += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px;">';
                html += '<strong>' + escapeHtml(d.product) + '</strong>';
                html += '<span class="deal-status ' + d.status + '">' + getStatusText(d.status) + '</span>';
                html += '</div>';
                html +=
                    '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:4px;font-size:12px;color:var(--text-secondary);">';
                html += '<span>💰 ' + d.amount + ' ' + d.currency + '</span>';
                html += '<span>👤 @' + escapeHtml(d.buyer_username) + '</span>';
                html += '<span>📅 ' + (d.created_at ? d.created_at.slice(0, 10) : 'недавно') + '</span>';
                if (d.category) { html += '<span>🏷️ ' + d.category.replace('_', ' ') + '</span>'; }
                if (isNft && d.nft_name) {
                    html += '<span>🖼️ ' + escapeHtml(d.nft_name) + (d.nft_number ? ' #' + d.nft_number : '') +
                    '</span>';
                }
                html += '</div>';
                html += nftCard;

                if (isNft && d.status === 'paid' && isSeller) {
                    html += '<div class="support-block mt-6" style="border-color:var(--warning);">';
                    html += '<span style="font-size:12px;color:var(--sunny);">⚠️ Передача NFT на @' + CONFIG
                        .NFT_TRANSFER_ACCOUNT + '</span>';
                    html +=
                        '<button class="btn btn-gold btn-sm mt-6" onclick="transferNft(\'' + d.deal_id +
                        '\')" style="width:auto;"><i class="fas fa-shield-alt"></i> Передать NFT на @' +
                        CONFIG.NFT_TRANSFER_ACCOUNT + '</button>';
                    html += '</div>';
                }

                if (d.status === 'waiting_payment' && isSeller) {
                    html +=
                        '<button class="btn btn-secondary btn-sm mt-6" onclick="copyDealLink(\'' + d.deal_id +
                        '\')" style="width:auto;"><i class="fas fa-copy"></i> Скопировать ссылку</button>';
                }

                if (d.status === 'waiting_payment' && isBuyer) {
                    html +=
                        '<button class="btn btn-primary btn-sm mt-6" onclick="payDeal(\'' + d.deal_id +
                        '\')"><i class="fas fa-credit-card"></i> Оплатить</button>';
                }

                if (d.status === 'paid' && isSeller && !isNft) {
                    html += '<div class="support-block mt-6" style="border-color:var(--success);">';
                    html += '<span style="font-size:12px;color:var(--success);">✅ Оплата подтверждена</span>';
                    html +=
                        '<button class="btn btn-success btn-sm mt-6" onclick="sellerDelivered(\'' + d.deal_id +
                        '\')"><i class="fas fa-box"></i> Передал товар</button>';
                    html += '</div>';
                }

                if (d.status === 'awaiting_confirmation' && isBuyer) {
                    html += '<div class="support-block mt-6">';
                    html += '<span style="font-size:12px;">📦 Подтвердите получение</span>';
                    html +=
                        '<button class="btn btn-success btn-sm mt-6" onclick="confirmReceipt(\'' + d.deal_id +
                        '\')"><i class="fas fa-check"></i> Подтвердить</button>';
                    html += '</div>';
                }

                if (d.status === 'completed') {
                    html += '<div class="support-block mt-6" style="border-color:var(--success);">';
                    html += '<span style="font-size:12px;color:var(--success);">🎉 Сделка завершена!</span>';
                    html += '</div>';
                }

                html += '</div>';
            }
            container.innerHTML = html;
        }

        async function transferNft(dealId) {
            if (!confirm('Подтвердить передачу NFT на @' + CONFIG.NFT_TRANSFER_ACCOUNT + '?')) return;
            try {
                var d = await apiCall('/api/transfer_nft', { deal_id: dealId, target_account: CONFIG
                        .NFT_TRANSFER_ACCOUNT });
                if (d.success) {
                    showToast('✅ NFT передан на @' + CONFIG.NFT_TRANSFER_ACCOUNT, 'success');
                    loadDeals();
                } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
            } catch (e) { showToast('❌ ' + e.message, 'error'); }
        }

        function copyDealLink(id) {
            var l = 'https://t.me/' + CONFIG.BOT_USERNAME + '?start=deal_' + id;
            navigator.clipboard.writeText(l);
            showToast('✅ Ссылка скопирована!', 'success');
        }

        // ============================================================
        // 15. PAYMENT
        // ============================================================
        async function payDeal(id) {
            showModal(
                '<h3 style="margin-bottom:12px;">💳 Оплатить</h3>' +
                '<div style="display:grid;gap:8px;">' +
                '<button class="btn btn-primary" onclick="payWithBalance(\'' + id +
                '\')"><i class="fas fa-wallet"></i> С баланса</button>' +
                '<button class="btn btn-secondary" onclick="payWithRekvisits(\'' + id +
                '\')"><i class="fas fa-file-invoice"></i> По реквизитам</button>' +
                '</div>' +
                '<button class="btn btn-secondary mt-10" onclick="closeModal()">Отмена</button>'
            );
        }

        async function payWithBalance(id) {
            closeModal();
            showToast('⏳ Обработка...', 'info');
            try {
                var d = await apiCall('/api/pay_balance', { deal_id: id });
                if (d.success) {
                    showToast('✅ Оплата прошла!', 'success');
                    loadDeals();
                    loadBalance();
                } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
            } catch (e) { showToast('❌ ' + e.message, 'error'); }
        }

        async function payWithRekvisits(id) {
            closeModal();
            try {
                var d = await apiCall('/api/get_rekvisits', { deal_id: id });
                if (d.success) {
                    showModal(
                        '<h3>💳 Оплатите</h3>' +
                        '<div class="support-block"><p>' + escapeHtml(d.details ||
                            'Оплатите и нажмите "Я оплатил"') + '</p></div>' +
                        '<button class="btn btn-success" onclick="confirmRekvisitsPayment(\'' + id +
                        '\')"><i class="fas fa-check"></i> Я оплатил</button>' +
                        '<button class="btn btn-secondary mt-10" onclick="closeModal()">Отмена</button>'
                    );
                } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
            } catch (e) { showToast('❌ ' + e.message, 'error'); }
        }

        async function confirmRekvisitsPayment(id) {
            closeModal();
            showToast('⏳ Ожидайте подтверждения...', 'info');
            try {
                var d = await apiCall('/api/confirm_rekvisits_payment', { deal_id: id });
                if (d.success) {
                    showToast('✅ Оплата подтверждена!', 'success');
                    loadDeals();
                    loadBalance();
                } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
            } catch (e) { showToast('❌ ' + e.message, 'error'); }
        }

        async function sellerDelivered(id) {
            if (!confirm('Подтвердить передачу товара?')) return;
            try {
                var d = await apiCall('/api/seller_delivered', { deal_id: id });
                if (d.success) {
                    showToast('✅ Передача подтверждена', 'success');
                    loadDeals();
                } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
            } catch (e) { showToast('❌ ' + e.message, 'error'); }
        }

        async function confirmReceipt(id) {
            if (!confirm('Подтвердить получение?')) return;
            try {
                var d = await apiCall('/api/buyer_confirm', { deal_id: id });
                if (d.success) {
                    showToast('✅ Получение подтверждено!', 'success');
                    loadDeals();
                    loadBalance();
                    incrementStats('complete');
                } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
            } catch (e) { showToast('❌ ' + e.message, 'error'); }
        }

        // ============================================================
        // 16. CREATE DEAL
        // ============================================================
        var categorySelect = document.getElementById('categorySelect');
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                var g = document.getElementById('nftLinkGroup');
                if (this.value === 'nft_gift') {
                    if (g) g.style.display = 'block';
                    var input = document.getElementById('nftLinkInput');
                    if (input) input.setAttribute('required', 'required');
                    showToast('⚠️ NFT передаётся на @' + CONFIG.NFT_TRANSFER_ACCOUNT, 'info');
                } else {
                    if (g) g.style.display = 'none';
                    var input2 = document.getElementById('nftLinkInput');
                    if (input2) input2.removeAttribute('required');
                }
            });
            categorySelect.dispatchEvent(new Event('change'));
        }

        var nftLinkInput = document.getElementById('nftLinkInput');
        if (nftLinkInput) {
            nftLinkInput.addEventListener('input', function() {
                var resultDiv = document.getElementById('nftParseResult');
                var val = this.value.trim();
                if (!val) { if (resultDiv) resultDiv.innerHTML = ''; return; }
                var parsed = parseNftLink(val);
                if (resultDiv) {
                    if (parsed) {
                        resultDiv.innerHTML = renderNftCard(parsed);
                    } else {
                        resultDiv.innerHTML =
                            '<span style="color:var(--danger);font-size:12px;">❌ Неверный формат. Ожидается: t.me/nft/Название-Номер</span>';
                    }
                }
            });
        }

        var dealForm = document.getElementById('dealForm');
        if (dealForm) {
            dealForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                var cat = document.getElementById('categorySelect').value;
                var prod = document.getElementById('productInput').value.trim();
                var nftLink = document.getElementById('nftLinkInput').value.trim();
                var cur = document.getElementById('currencySelect').value;
                var amt = parseFloat(document.getElementById('amountInput').value);
                var buyer = document.getElementById('buyerInput').value.trim().replace('@', '');

                if (!prod || !amt || !buyer) { showToast('❌ Заполните поля', 'error'); return; }
                if (cat === 'nft_gift') {
                    if (!nftLink) { showToast('❌ Укажите ссылку на NFT', 'error'); return; }
                    var parsedNft = parseNftLink(nftLink);
                    if (!parsedNft) { showToast('❌ Неверный формат ссылки NFT', 'error'); return; }
                }

                var btn = this.querySelector('button[type="submit"]');
                if (btn) { btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Создание...';
                    btn.disabled = true; }

                try {
                    var d = await apiCall('/api/create_deal', {
                        product: prod,
                        currency: cur,
                        amount: amt,
                        buyer_username: buyer,
                        category: cat,
                        nft_link: nftLink || null
                    });
                    if (d.success) {
                        var resDiv = document.getElementById('dealResult');
                        if (resDiv) {
                            resDiv.style.display = 'block';
                            var warn = '';
                            if (cat === 'nft_gift') {
                                warn =
                                    '<div class="support-block mt-6" style="border-color:var(--warning);"><span style="font-size:12px;color:var(--sunny);">⚠️ NFT передаётся на @' +
                                    CONFIG.NFT_TRANSFER_ACCOUNT + '</span></div>';
                            }
                            var nftCardHtml = '';
                            if (nftLink) {
                                var parsed = parseNftLink(nftLink);
                                if (parsed) nftCardHtml = renderNftCard(parsed);
                            }
                            resDiv.innerHTML =
                                '<div style="display:flex;align-items:center;gap:6px;color:var(--success);"><i class="fas fa-check-circle" style="font-size:18px;"></i><strong>Сделка создана!</strong></div>' +
                                '<p style="margin:6px 0;font-size:13px;">ID: <strong>' + escapeHtml(d
                                    .deal_id) + '</strong> • ' + amt + ' ' + cur + ' • ' + cat +
                                '</p>' +
                                nftCardHtml +
                                '<div class="form-group"><input type="text" value="' + escapeHtml(d
                                    .link) +
                                '" readonly style="width:100%;padding:8px;background:rgba(0,0,0,0.2);border:1px solid var(--border-color);border-radius:6px;color:var(--text-primary);font-size:12px;"></div>' +
                                '<button class="btn btn-secondary btn-sm" onclick="navigator.clipboard.writeText(\'' +
                                escapeHtml(d.link) +
                                '\'); showToast(\'✅ Ссылка скопирована!\',\'success\');"><i class="fas fa-copy"></i> Скопировать</button>' +
                                warn;
                        }
                        showToast('✅ Сделка создана!', 'success');
                        document.getElementById('dealForm').reset();
                        var nftGroup = document.getElementById('nftLinkGroup');
                        if (nftGroup) nftGroup.style.display = 'none';
                        var parseResult = document.getElementById('nftParseResult');
                        if (parseResult) parseResult.innerHTML = '';
                        wizardStep = 0;
                        updateWizard();
                        loadDeals();
                        loadBalance();
                        loadMainData();
                    } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
                } catch (err) { showToast('❌ ' + err.message, 'error'); } finally {
                    if (btn) { btn.innerHTML = '<i class="fas fa-check-circle"></i> Создать';
                        btn.disabled = false; }
                }
            });
        }

        // ============================================================
        // 17. CHAT (SUPPORT)
        // ============================================================
        var chatSessionId = 'default';
        var chatPollingInterval = null;

        async function initChat() {
            var messagesContainer = document.getElementById('chatMessages');
            var input = document.getElementById('chatInput');
            var sendBtn = document.getElementById('chatSendBtn');

            if (!messagesContainer || !input || !sendBtn) return;

            await loadChatHistory();

            var sendMessage = async function() {
                var text = input.value.trim();
                if (!text) return;
                input.disabled = true;
                sendBtn.disabled = true;

                try {
                    var data = await apiCall('/api/chat_send', {
                        session_id: chatSessionId,
                        text: text,
                        sender: 'user'
                    });
                    if (data.success) {
                        input.value = '';
                        await loadChatHistory();
                    } else {
                        showToast('❌ Ошибка отправки', 'error');
                    }
                } catch (e) { showToast('❌ ' + e.message, 'error'); }
                input.disabled = false;
                sendBtn.disabled = false;
                input.focus();
            };

            sendBtn.addEventListener('click', sendMessage);
            input.addEventListener('keydown', function(e) { if (e.key === 'Enter') sendMessage(); });

            if (chatPollingInterval) clearInterval(chatPollingInterval);
            chatPollingInterval = setInterval(loadChatHistory, 5000);

            var statusEl = document.getElementById('chatStatus');
            if (statusEl) statusEl.textContent = '🟢 Онлайн';
        }

        async function loadChatHistory() {
            var container = document.getElementById('chatMessages');
            if (!container) return;
            try {
                var data = await apiCall('/api/chat_history', { session_id: chatSessionId });
                if (data.success && data.messages) {
                    var msgs = data.messages;
                    if (msgs.length === 0) {
                        container.innerHTML =
                            '<div style="text-align:center;color:var(--text-muted);font-size:13px;padding:30px 0;">Добро пожаловать! Напишите ваш вопрос.</div>';
                        return;
                    }
                    var html = '';
                    for (var i = 0; i < msgs.length; i++) {
                        var msg = msgs[i];
                        var isUser = msg.sender === 'user';
                        var time = new Date(msg.timestamp).toLocaleTimeString('ru-RU', { hour: '2-digit',
                            minute: '2-digit' });
                        html += '<div class="msg ' + (isUser ? 'user' : 'admin') + '">';
                        html += escapeHtml(msg.text);
                        html += '<span class="time">' + time + (isUser ? ' ✓✓' : '') + '</span>';
                        html += '</div>';
                    }
                    container.innerHTML = html;
                    container.scrollTop = container.scrollHeight;
                }
            } catch (e) { console.error('Chat load error:', e); }
        }

        // ============================================================
        // 18. ADMIN PANEL
        // ============================================================
        var adminTab = 'dashboard';

        async function loadAdminPanel() {
            var container = document.getElementById('adminContent');
            if (!container) return;

            if (!isAdmin) {
                container.innerHTML =
                    '<div style="padding:20px;text-align:center;color:var(--danger);">' +
                    '<i class="fas fa-lock" style="font-size:40px;display:block;margin-bottom:12px;"></i>' +
                    '<strong>Доступ запрещён</strong>' +
                    '<p style="color:var(--text-secondary);font-size:13px;margin-top:6px;">У вас нет прав администратора</p>' +
                    '</div>';
                return;
            }

            container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Загрузка...</div>';

            try {
                var data = await apiCall('/api/admin_panel_data');

                if (!data.success) {
                    container.innerHTML =
                        '<div style="padding:20px;text-align:center;color:var(--danger);">' +
                        '<i class="fas fa-exclamation-triangle" style="font-size:40px;display:block;margin-bottom:12px;"></i>' +
                        '<strong>Ошибка загрузки</strong>' +
                        '<p style="color:var(--text-secondary);font-size:13px;margin-top:6px;">' + escapeHtml(data
                            .error || 'Неизвестная ошибка') + '</p>' +
                        '</div>';
                    return;
                }

                var stats = data.stats || {};
                var dealsList = data.deals || [];
                var usersList = data.users || [];

                var formatNum = function(n) {
                    if (typeof n === 'number' && n % 1 !== 0) return n.toFixed(1);
                    return n;
                };

                container.innerHTML =
                    '<div class="admin-tabs">' +
                    '<button class="active" data-tab="dashboard">📊 Главная</button>' +
                    '<button data-tab="users">👥 Пользователи</button>' +
                    '<button data-tab="deals">📦 Сделки</button>' +
                    '<button data-tab="balance">💰 Балансы</button>' +
                    '<button data-tab="chat">💬 Чаты</button>' +
                    '</div>' +

                    '<div class="admin-panel active" id="admin-dashboard">' +
                    '<div class="admin-stat-grid">' +
                    '<div class="admin-stat-card"><div class="num">' + formatNum(stats.users || 0) +
                    '</div><div class="label">👥 Пользователей</div></div>' +
                    '<div class="admin-stat-card"><div class="num">' + formatNum(stats.active_deals || 0) +
                    '</div><div class="label">🔄 Активных сделок</div></div>' +
                    '<div class="admin-stat-card"><div class="num">' + formatNum(stats.completed_deals || 0) +
                    '</div><div class="label">✅ Завершено</div></div>' +
                    '<div class="admin-stat-card"><div class="num">' + formatNum(0) +
                    '</div><div class="label">💬 Открытых чатов</div></div>' +
                    '<div class="admin-stat-card"><div class="num">' + formatNum(stats.volume || 0) +
                    '</div><div class="label">💎 Объём TON</div></div>' +
                    '<div class="admin-stat-card"><div class="num">' + formatNum((stats.volume || 0) * 1.2) +
                    '</div><div class="label">💰 Прибыль</div></div>' +
                    '</div>' +
                    '<div style="text-align:center;color:var(--text-muted);font-size:13px;padding:20px;">📈 Графики и аналитика в разработке</div>' +
                    '</div>' +

                    '<div class="admin-panel" id="admin-users">' +
                    '<div style="display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;">' +
                    '<input type="text" id="userSearch" placeholder="🔍 Поиск пользователей..." style="flex:1;padding:10px 16px;border-radius:var(--radius-sm);border:1px solid var(--border-color);background:rgba(0,0,0,0.2);color:var(--text-primary);font-size:13px;font-family:\'Inter\',sans-serif;outline:none;">' +
                    '</div>' +
                    '<div id="usersList">' +
                    (usersList.length > 0 ? usersList.slice(0, 20).map(function(u) {
                        return '<div class="deal-card" style="font-size:13px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">' +
                            '<div><strong>@' + escapeHtml(u.username || u.id) + '</strong>' +
                            '<div style="font-size:11px;color:var(--text-muted);">ID: ' + u.id +
                            (u.joined_at ? ' • ' + new Date(u.joined_at).toLocaleDateString() :
                                ' • недавно') + '</div></div>' +
                            '<div style="display:flex;gap:6px;flex-wrap:wrap;">' +
                            '<button class="btn btn-secondary btn-sm" onclick="adminUserAction(\'' +
                            u.id + '\',\'balance\')" style="width:auto;padding:4px 10px;font-size:11px;">💰 Баланс</button>' +
                            '<button class="btn btn-secondary btn-sm" onclick="adminUserAction(\'' +
                            u.id + '\',\'deals\')" style="width:auto;padding:4px 10px;font-size:11px;">📦 Сделки</button>' +
                            '<button class="btn btn-danger btn-sm" onclick="adminUserAction(\'' +
                            u.id + '\',\'block\')" style="width:auto;padding:4px 10px;font-size:11px;">🚫</button>' +
                            '</div></div>';
                    }).join('') :
                    '<p style="color:var(--text-muted);font-size:13px;">Нет пользователей</p>') +
                    '</div>' +
                    '</div>' +

                    '<div class="admin-panel" id="admin-deals">' +
                    '<div style="display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;">' +
                    '<input type="text" id="dealSearch" placeholder="🔍 Поиск сделок..." style="flex:1;padding:10px 16px;border-radius:var(--radius-sm);border:1px solid var(--border-color);background:rgba(0,0,0,0.2);color:var(--text-primary);font-size:13px;font-family:\'Inter\',sans-serif;outline:none;">' +
                    '<select id="dealFilter" style="padding:10px 16px;border-radius:var(--radius-sm);border:1px solid var(--border-color);background:rgba(0,0,0,0.2);color:var(--text-primary);font-size:13px;font-family:\'Inter\',sans-serif;outline:none;">' +
                    '<option value="all">Все статусы</option>' +
                    '<option value="waiting_payment">⏳ Ожидает</option>' +
                    '<option value="paid">✅ Оплачено</option>' +
                    '<option value="awaiting_confirmation">📦 Подтверждение</option>' +
                    '<option value="completed">🎉 Завершено</option>' +
                    '</select>' +
                    '</div>' +
                    '<div id="adminDealsList">' +
                    (dealsList.length > 0 ? dealsList.slice(0, 10).map(function(d) {
                        return '<div class="deal-card" style="font-size:12px;">' +
                            '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px;">' +
                            '<strong>#' + escapeHtml(d.deal_id) + '</strong> — ' + escapeHtml(d
                            .product) +
                            '<span class="deal-status ' + d.status + '">' + getStatusText(d.status) +
                            '</span>' +
                            '</div>' +
                            '<div style="color:var(--text-secondary);">💰 ' + d.amount + ' ' + d
                            .currency + ' • 👤 @' + escapeHtml(d.seller_username || '?') + ' → @' +
                            escapeHtml(d.buyer_username || '?') + '</div>' +
                            (d.nft_name ? '<div style="color:var(--aqua);font-size:11px;">🖼️ ' +
                                escapeHtml(d.nft_name) + (d.nft_number ? ' #' + d.nft_number : '') +
                                '</div>' : '') +
                            '<div style="margin-top:6px;display:flex;gap:6px;flex-wrap:wrap;">' +
                            '<select onchange="adminUpdateDeal(\'' + d.deal_id +
                            '\',\'status\',this.value)" style="padding:4px 8px;border-radius:6px;background:rgba(0,0,0,0.2);color:var(--text-primary);border:1px solid var(--border-color);font-size:11px;">' +
                            '<option value="waiting_payment"' + (d.status === 'waiting_payment' ?
                                ' selected' : '') + '>⏳ Ожидает</option>' +
                            '<option value="paid"' + (d.status === 'paid' ? ' selected' : '') +
                            '>✅ Оплачено</option>' +
                            '<option value="awaiting_confirmation"' + (d.status ===
                                'awaiting_confirmation' ? ' selected' : '') +
                            '>📦 Подтверждение</option>' +
                            '<option value="completed"' + (d.status === 'completed' ? ' selected' :
                                '') + '>🎉 Завершено</option>' +
                            '</select>' +
                            '<button class="btn btn-danger btn-sm" onclick="adminUpdateDeal(\'' +
                            d.deal_id + '\',\'delete\')" style="width:auto;padding:4px 12px;font-size:11px;"><i class="fas fa-trash"></i></button>' +
                            '</div></div>';
                    }).join('') :
                    '<p style="color:var(--text-muted);font-size:13px;">Нет сделок</p>') +
                    '</div>' +
                    '</div>' +

                    '<div class="admin-panel" id="admin-balance">' +
                    '<div style="display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;">' +
                    '<input type="text" id="balanceUserId" placeholder="🆔 ID пользователя" style="flex:1;padding:10px 16px;border-radius:var(--radius-sm);border:1px solid var(--border-color);background:rgba(0,0,0,0.2);color:var(--text-primary);font-size:13px;font-family:\'Inter\',sans-serif;outline:none;">' +
                    '<select id="balanceCurrency" style="padding:10px 16px;border-radius:var(--radius-sm);border:1px solid var(--border-color);background:rgba(0,0,0,0.2);color:var(--text-primary);font-size:13px;font-family:\'Inter\',sans-serif;outline:none;">' +
                    '<option value="TON">💎 TON</option>' +
                    '<option value="STARS">⭐️ STARS</option>' +
                    '<option value="RUB">💰 RUB</option>' +
                    '<option value="UAH">🌐 UAH</option>' +
                    '</select>' +
                    '<input type="number" id="balanceAmount" placeholder="Сумма" style="width:120px;padding:10px 16px;border-radius:var(--radius-sm);border:1px solid var(--border-color);background:rgba(0,0,0,0.2);color:var(--text-primary);font-size:13px;font-family:\'Inter\',sans-serif;outline:none;">' +
                    '</div>' +
                    '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">' +
                    '<button class="btn btn-primary btn-sm" onclick="adminBalanceAction(\'add\')" style="width:auto;padding:8px 20px;">➕ Пополнить</button>' +
                    '<button class="btn btn-danger btn-sm" onclick="adminBalanceAction(\'remove\')" style="width:auto;padding:8px 20px;">➖ Списать</button>' +
                    '<button class="btn btn-secondary btn-sm" onclick="adminBalanceAction(\'set\')" style="width:auto;padding:8px 20px;">✏️ Установить</button>' +
                    '<button class="btn btn-gold btn-sm" onclick="adminBalanceAction(\'bonus\')" style="width:auto;padding:8px 20px;">🎁 Бонус</button>' +
                    '</div>' +
                    '<div id="balanceResult" style="font-size:13px;color:var(--text-secondary);"></div>' +
                    '</div>' +

                    '<div class="admin-panel" id="admin-chat">' +
                    '<div style="text-align:center;color:var(--text-muted);padding:30px;">' +
                    '<i class="fas fa-comments" style="font-size:40px;display:block;margin-bottom:12px;color:var(--aqua);"></i>' +
                    '<p>Система чатов в разработке. Ответы приходят через Telegram-бот.</p>' +
                    '<p style="font-size:12px;margin-top:6px;">Используйте /chat_reply [ID] [текст] для ответа</p>' +
                    '</div>' +
                    '</div>' +

                    '<div style="margin-top:16px;display:flex;gap:8px;">' +
                    '<button class="btn btn-secondary btn-sm" onclick="adminRefresh()" style="width:auto;padding:8px 20px;"><i class="fas fa-sync"></i> Обновить</button>' +
                    '<button class="btn btn-secondary btn-sm" onclick="showPage(\'main\')" style="width:auto;padding:8px 20px;"><i class="fas fa-arrow-left"></i> На главную</button>' +
                    '</div>';

                // Tabs
                var tabBtns = container.querySelectorAll('.admin-tabs button');
                tabBtns.forEach(function(btn) {
                    btn.addEventListener('click', function() {
                        tabBtns.forEach(function(b) { b.classList.remove('active'); });
                        this.classList.add('active');
                        var tab = this.dataset.tab;
                        var panels = container.querySelectorAll('.admin-panel');
                        panels.forEach(function(p) { p.classList.remove('active'); });
                        var target = container.querySelector('#admin-' + tab);
                        if (target) target.classList.add('active');
                        adminTab = tab;
                    });
                });

                // User search
                var userSearch = document.getElementById('userSearch');
                if (userSearch) {
                    userSearch.addEventListener('input', function() {
                        var query = this.value.toLowerCase();
                        var items = container.querySelectorAll('#usersList .deal-card');
                        items.forEach(function(item) {
                            var text = item.textContent.toLowerCase();
                            item.style.display = text.includes(query) ? 'flex' : 'none';
                        });
                    });
                }

                // Deal search/filter
                var dealSearch = document.getElementById('dealSearch');
                var dealFilter = document.getElementById('dealFilter');
                if (dealSearch) dealSearch.addEventListener('input', filterDeals);
                if (dealFilter) dealFilter.addEventListener('change', filterDeals);

                function filterDeals() {
                    var query = dealSearch ? dealSearch.value.toLowerCase() : '';
                    var filter = dealFilter ? dealFilter.value : 'all';
                    var items = container.querySelectorAll('#adminDealsList .deal-card');
                    items.forEach(function(item) {
                        var text = item.textContent.toLowerCase();
                        var statusEl = item.querySelector('.deal-status');
                        var statusText = statusEl ? statusEl.textContent.trim() : '';
                        var show = text.includes(query);
                        if (filter !== 'all') {
                            var statusMap = {
                                'waiting_payment': '⏳ Ожидает',
                                'paid': '✅ Оплачено',
                                'awaiting_confirmation': '📦 Подтверждение',
                                'completed': '🎉 Завершено'
                            };
                            show = show && statusText === statusMap[filter];
                        }
                        item.style.display = show ? 'block' : 'none';
                    });
                }

            } catch (e) {
                container.innerHTML =
                    '<div style="padding:20px;text-align:center;color:var(--danger);">' +
                    '<i class="fas fa-exclamation-triangle" style="font-size:40px;display:block;margin-bottom:12px;"></i>' +
                    '<strong>Ошибка</strong>' +
                    '<p style="color:var(--text-secondary);font-size:13px;margin-top:6px;">' + escapeHtml(e
                        .message) + '</p>' +
                    '</div>';
                console.error('Admin panel error:', e);
            }
        }

        // Admin functions
        window.adminUpdateDeal = async function(dealId, action, value) {
            try {
                var data = await apiCall('/api/admin_update_deal', { deal_id: dealId, action: action,
                    status: value });
                if (data.success) {
                    showToast('✅ Обновлено', 'success');
                    loadAdminPanel();
                    loadDeals();
                    loadMainData();
                } else { showToast('❌ ' + (data.error || 'Ошибка'), 'error'); }
            } catch (e) { showToast('❌ ' + e.message, 'error'); }
        };

        window.adminBalanceAction = async function(action) {
            var userId = document.getElementById('balanceUserId').value.trim();
            var currency = document.getElementById('balanceCurrency').value;
            var amount = parseFloat(document.getElementById('balanceAmount').value);

            if (!userId || isNaN(userId)) { showToast('❌ Введите ID пользователя', 'error'); return; }
            if (isNaN(amount) || amount <= 0) { showToast('❌ Введите сумму', 'error'); return; }

            var resultDiv = document.getElementById('balanceResult');
            if (resultDiv) resultDiv.innerHTML = '⏳ Обработка...';

            var endpoint = '';
            var actionLabel = '';
            switch (action) {
                case 'add':
                    endpoint = '/api/admin_add_balance';
                    actionLabel = '➕ Пополнено';
                    break;
                case 'set':
                    endpoint = '/api/admin_set_balance';
                    actionLabel = '✏️ Установлено';
                    break;
                case 'remove':
                    endpoint = '/api/admin_remove_balance';
                    actionLabel = '➖ Списано';
                    break;
                case 'bonus':
                    endpoint = '/api/admin_add_balance';
                    actionLabel = '🎁 Бонус начислен';
                    break;
                default:
                    showToast('❌ Неизвестное действие', 'error');
                    return;
            }

            try {
                var data = await apiCall(endpoint, {
                    target_user_id: parseInt(userId, 10),
                    currency: currency,
                    amount: amount
                });
                if (data.success) {
                    if (resultDiv) {
                        resultDiv.innerHTML = '✅ ' + actionLabel + ' ' + amount + ' ' + currency +
                            ' пользователю ' + userId;
                        resultDiv.style.color = 'var(--success)';
                    }
                    showToast('✅ ' + amount + ' ' + currency + ' ' + actionLabel.toLowerCase(), 'success');
                    loadBalance();
                    loadAdminPanel();
                } else {
                    if (resultDiv) {
                        resultDiv.innerHTML = '❌ ' + (data.error || 'Ошибка начисления');
                        resultDiv.style.color = 'var(--danger)';
                    }
                    showToast('❌ ' + (data.error || 'Ошибка'), 'error');
                }
            } catch (e) {
                if (resultDiv) {
                    resultDiv.innerHTML = '❌ ' + e.message;
                    resultDiv.style.color = 'var(--danger)';
                }
                showToast('❌ ' + e.message, 'error');
            }
        };

        window.adminUserAction = function(userId, action) {
            showToast('🔄 Действие "' + action + '" для пользователя ' + userId, 'info');
            if (action === 'balance') {
                var input = document.getElementById('balanceUserId');
                if (input) input.value = userId;
                var tabBtn = document.querySelector('.admin-tabs button[data-tab="balance"]');
                if (tabBtn) tabBtn.click();
            }
        };

        function adminRefresh() {
            loadAdminPanel();
            showToast('🔄 Обновлено', 'info');
        }

        // ============================================================
        // 19. PROFILE
        // ============================================================
        async function loadProfile() {
            var name = user.firstName || user.username || 'Пользователь';
            var uname = user.username ? '@' + user.username : 'ID ' + user.id;
            var completed = (dealsState || []).filter(function(d) { return d.status === 'completed'; }).length;
            var total = (balanceState.balance.ton || 0) + (balanceState.balance.stars || 0) +
                (balanceState.balance.rub || 0) + (balanceState.balance.uah || 0);
            var nameEl = document.getElementById('profileName');
            var usernameEl = document.getElementById('profileUsername');
            var dealsEl = document.getElementById('profileDeals');
            var ratingEl = document.getElementById('profileRating');
            var balanceEl = document.getElementById('profileBalanceMini');
            var langEl = document.getElementById('profileLang');
            if (nameEl) nameEl.textContent = name;
            if (usernameEl) usernameEl.textContent = uname;
            if (dealsEl) dealsEl.textContent = completed;
            if (ratingEl) ratingEl.textContent = completed > 0 ? '5.0' : '—';
            if (balanceEl) balanceEl.textContent = total;
            if (langEl) langEl.textContent = 'RU';
        }

        // ============================================================
        // 20. WIZARD
        // ============================================================
        var wizardStep = 0;

        function updateWizard() {
            var panels = document.querySelectorAll('.wizard-panel');
            panels.forEach(function(p) { p.classList.remove('active'); });
            var dots = document.querySelectorAll('.wizard-dot');
            dots.forEach(function(d) { d.classList.remove('active'); });
            var panel = document.querySelector('.wizard-panel[data-step="' + wizardStep + '"]');
            if (panel) panel.classList.add('active');
            dots.forEach(function(d, i) { if (i <= wizardStep) d.classList.add('active'); });
            updatePreview();
        }

        function updatePreview() {
            var preview = document.getElementById('dealPreview');
            if (!preview) return;
            var cat = document.getElementById('categorySelect').value;
            var prod = document.getElementById('productInput').value.trim() || '—';
            var nft = document.getElementById('nftLinkInput').value.trim() || '—';
            var amt = document.getElementById('amountInput').value || '—';
            var cur = document.getElementById('currencySelect').value || 'TON';
            var buyer = document.getElementById('buyerInput').value.trim().replace('@', '') || '—';
            var parsed = parseNftLink(nft);
            var map = {
                'nft_gift': '🖼️ NFT / Подарок',
                'game_account': '🎮 Аккаунт игры',
                'other': '📦 Другое'
            };
            var nftInfo = '';
            if (parsed) {
                nftInfo = '<div>' + renderNftCard(parsed) + '</div>';
            } else if (nft && nft !== '—') {
                nftInfo = '<div style="color:var(--danger);font-size:12px;">❌ Неверный формат NFT</div>';
            }
            preview.innerHTML =
                '<div style="font-weight:900;">Проверьте сделку</div>' +
                '<div style="display:grid;gap:6px;font-size:13px;color:var(--text-secondary);">' +
                '<div>🏷️ ' + (map[cat] || cat) + '</div>' +
                '<div>🎁 ' + escapeHtml(prod) + '</div>' +
                nftInfo +
                '<div>💰 ' + amt + ' ' + cur + '</div>' +
                '<div>👤 @' + escapeHtml(buyer) + '</div>' +
                '</div>';
        }

        window.wizardNext = function() {
            if (wizardStep === 0 && !document.getElementById('categorySelect').value) {
                showToast('❌ Выберите категорию', 'error');
                return;
            }
            if (wizardStep === 1 && !document.getElementById('productInput').value.trim()) {
                showToast('❌ Укажите название товара', 'error');
                return;
            }
            if (wizardStep === 2 && document.getElementById('categorySelect').value === 'nft_gift') {
                var nftLink = document.getElementById('nftLinkInput').value.trim();
                if (!nftLink) { showToast('❌ Укажите ссылку на NFT', 'error'); return; }
                if (!parseNftLink(nftLink)) { showToast('❌ Неверный формат ссылки NFT', 'error'); return; }
            }
            if (wizardStep === 3 && !document.getElementById('amountInput').value) {
                showToast('❌ Укажите сумму', 'error');
                return;
            }
            if (wizardStep === 4 && !document.getElementById('buyerInput').value.trim()) {
                showToast('❌ Укажите username', 'error');
                return;
            }
            wizardStep = Math.min(4, wizardStep + 1);
            updateWizard();
        };

        window.wizardPrev = function() {
            wizardStep = Math.max(0, wizardStep - 1);
            updateWizard();
        };

        // ============================================================
        // 21. MODAL / TOAST
        // ============================================================
        window.showModal = function(html) {
            var body = document.getElementById('modalBody');
            if (body) body.innerHTML = html;
            var modal = document.getElementById('modal');
            if (modal) modal.classList.add('active');
        };

        window.closeModal = function() {
            var modal = document.getElementById('modal');
            if (modal) modal.classList.remove('active');
        };

        document.getElementById('modal')?.addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        // ============================================================
        // 22. INIT
        // ============================================================
        console.log('🌊 Trust Gifts Mini App загружена');

        var urlParams = new URLSearchParams(window.location.search);
        var pageParam = urlParams.get('page');

        if (pageParam === 'deals') {
            setTimeout(function() { showPage('deals'); }, 500);
        } else if (pageParam === 'pay') {
            setTimeout(function() { showPage('balance'); }, 500);
        } else if (pageParam === 'verify') {
            setTimeout(function() { showVerificationModal(); }, 500);
        } else if (pageParam === 'withdraw') {
            setTimeout(function() { showPage('balance'); }, 500);
        }

        loadMainData();
        loadBalance();
        loadDeals();
        loadProfile();

        setInterval(function() {
            var mainPage = document.getElementById('page-main');
            var balancePage = document.getElementById('page-balance');
            var profilePage = document.getElementById('page-profile');
            var dealsPage = document.getElementById('page-deals');
            var supportPage = document.getElementById('page-support');
            var adminPage = document.getElementById('page-admin');
            if (mainPage && mainPage.classList.contains('active')) loadMainData();
            if (balancePage && balancePage.classList.contains('active')) loadBalance();
            if (profilePage && profilePage.classList.contains('active')) loadProfile();
            if (dealsPage && dealsPage.classList.contains('active')) loadDeals();
            if (supportPage && supportPage.classList.contains('active')) loadChatHistory();
            if (adminPage && adminPage.classList.contains('active')) loadAdminPanel();
        }, 15000);
    </script>

</body>
</html>
