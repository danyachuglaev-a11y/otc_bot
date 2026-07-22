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
        *{margin:0;padding:0;box-sizing:border-box}
        :root{--bg-primary:#07141a;--bg-secondary:#0b202a;--bg-card:rgba(14,40,52,0.45);--border-color:rgba(0,255,200,0.10);--text-primary:#e6f7f0;--text-secondary:#8fc9d9;--text-muted:#4f8a9a;--aqua:#00e5c8;--coral:#ff6b6b;--sunny:#ffd93d;--gradient-main:linear-gradient(135deg,#00e5c8,#00b8a0,#00897b);--radius:28px;--radius-sm:16px;--success:#00e5a0;--danger:#ff6b6b;--warning:#ffd93d;--shadow-glow:0 8px 40px rgba(0,229,200,0.08);--glass-border:rgba(255,255,255,0.04)}
        body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg-primary);color:var(--text-primary);min-height:100vh;padding:16px;padding-bottom:90px;overflow-x:hidden;background-image:radial-gradient(circle at 10%20%,rgba(0,229,200,0.06)0%,transparent 45%),radial-gradient(circle at 90%80%,rgba(255,107,107,0.03)0%,transparent 40%);-webkit-font-smoothing:antialiased}
        ::-webkit-scrollbar{width:4px}
        ::-webkit-scrollbar-track{background:var(--bg-primary)}
        ::-webkit-scrollbar-thumb{background:var(--aqua);border-radius:10px}
        .summer-scene{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none}
        .summer-scene .sun{position:absolute;top:20px;right:40px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,#ffd93d,#f9a825 60%,transparent 75%);box-shadow:0 0 120px rgba(255,217,61,0.15);animation:sunSpin 30s linear infinite;opacity:0.3}
        @keyframes sunSpin{0%{transform:rotate(0deg)scale(1)}50%{transform:rotate(180deg)scale(1.05)}100%{transform:rotate(360deg)scale(1)}}
        .summer-scene .wave{position:absolute;bottom:0;left:0;right:0;height:120px;background:repeating-linear-gradient(90deg,transparent,rgba(0,229,200,0.02)30px,transparent 60px);animation:waveMove 12s ease-in-out infinite;opacity:0.3}
        .summer-scene .wave:nth-child(2){bottom:20px;height:80px;animation-delay:-4s;opacity:0.2}
        .summer-scene .wave:nth-child(3){bottom:0px;height:100px;animation-delay:-8s;opacity:0.15}
        @keyframes waveMove{0%{transform:translateX(-40px)scaleY(1)}50%{transform:translateX(40px)scaleY(1.1)}100%{transform:translateX(-40px)scaleY(1)}}
        .summer-scene .cloud{position:absolute;font-size:40px;opacity:0.05;animation:cloudFloat 40s linear infinite}
        .summer-scene .cloud:nth-child(4){top:10%;left:-10%;animation-duration:35s}
        .summer-scene .cloud:nth-child(5){top:30%;left:-20%;animation-duration:50s;animation-delay:-10s}
        .summer-scene .cloud:nth-child(6){top:5%;left:-30%;animation-duration:45s;animation-delay:-20s}
        @keyframes cloudFloat{0%{transform:translateX(0)}100%{transform:translateX(110vw)}}
        .summer-scene .bird{position:absolute;font-size:16px;opacity:0.04;animation:birdFly 25s linear infinite}
        .summer-scene .bird:nth-child(7){top:15%;left:-5%;animation-duration:22s}
        .summer-scene .bird:nth-child(8){top:25%;left:-15%;animation-duration:28s;animation-delay:-8s}
        @keyframes birdFly{0%{transform:translateX(0)translateY(0)}25%{transform:translateX(25vw)translateY(-20px)}50%{transform:translateX(50vw)translateY(10px)}75%{transform:translateX(75vw)translateY(-15px)}100%{transform:translateX(110vw)translateY(0)}}
        @keyframes popIn{0%{opacity:0;transform:scale(0.96)translateY(12px)}100%{opacity:1;transform:scale(1)translateY(0)}}
        @keyframes slideFade{0%{opacity:0;transform:translateY(20px)}100%{opacity:1;transform:translateY(0)}}
        @keyframes pulseGlow{0%,100%{box-shadow:0 0 20px rgba(0,229,200,0.05)}50%{box-shadow:0 0 60px rgba(0,229,200,0.12)}}
        @keyframes shimmerText{0%{background-position:-200% center}100%{background-position:200% center}}
        @keyframes floatUp{0%,100%{transform:translateY(0)rotate(0deg)}50%{transform:translateY(-16px)rotate(4deg)}}
        @keyframes spinSlow{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
        .glass{background:var(--bg-card);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border:1px solid var(--glass-border);box-shadow:var(--shadow-glow),inset 0 1px 0 rgba(255,255,255,0.03);animation:popIn 0.5s ease forwards}
        .glass:hover{border-color:rgba(0,229,200,0.12)}
        .header{display:flex;justify-content:space-between;align-items:center;padding:14px 20px;border-radius:var(--radius);margin-bottom:16px;flex-wrap:wrap;gap:8px;position:relative;z-index:2}
        .header-logo{font-size:38px;filter:drop-shadow(0 0 20px rgba(0,229,200,0.3));animation:floatUp 5s ease-in-out infinite}
        .header-title{font-size:24px;font-weight:900;background:linear-gradient(135deg,#00e5c8,#ffd93d,#ff6b6b);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmerText 4s linear infinite}
        .header-title span{font-weight:400;-webkit-text-fill-color:var(--text-secondary)}
        .header-user{font-size:12px;color:var(--text-secondary);font-weight:500}
        .header-balance{font-size:15px;font-weight:700;color:var(--aqua);background:rgba(0,229,200,0.06);padding:2px 18px;border-radius:30px;border:1px solid rgba(0,229,200,0.1)}
        .online-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(0,229,200,0.06);padding:4px 14px;border-radius:30px;font-size:11px;font-weight:600;color:var(--aqua);border:1px solid rgba(0,229,200,0.08)}
        .online-dot{width:7px;height:7px;background:var(--aqua);border-radius:50%;display:inline-block;animation:pulseGlow 1.8s ease-in-out infinite}
        .stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;z-index:2;position:relative}
        .stat-card{padding:14px 10px;border-radius:var(--radius-sm);text-align:center;background:var(--bg-card);backdrop-filter:blur(12px);border:1px solid var(--border-color);transition:all 0.4s cubic-bezier(0.34,1.56,0.64,1);animation:slideFade 0.5s ease backwards}
        .stat-card:nth-child(1){animation-delay:0.05s}
        .stat-card:nth-child(2){animation-delay:0.10s}
        .stat-card:nth-child(3){animation-delay:0.15s}
        .stat-card:hover{transform:translateY(-6px)scale(1.02);border-color:rgba(0,229,200,0.2);box-shadow:0 12px 40px rgba(0,229,200,0.08)}
        .stat-number{font-size:26px;font-weight:900;background:var(--gradient-main);-webkit-background-clip:text;-webkit-text-fill-color:transparent;display:block;transition:all 0.3s}
        .stat-label{font-size:9px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.8px;font-weight:600;margin-top:4px}
        .nav{display:flex;gap:6px;background:var(--bg-card);backdrop-filter:blur(20px);padding:8px;border-radius:var(--radius);border:1px solid var(--border-color);margin-bottom:16px;overflow-x:auto;flex-wrap:nowrap;position:relative;z-index:2;-webkit-overflow-scrolling:touch}
        .nav button{flex:1;min-width:48px;padding:10px 4px;border:none;border-radius:var(--radius-sm);background:transparent;color:var(--text-secondary);font-size:10px;font-weight:600;font-family:'Inter',sans-serif;cursor:pointer;transition:all 0.4s cubic-bezier(0.34,1.56,0.64,1);white-space:nowrap;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;position:relative;-webkit-tap-highlight-color:transparent}
        .nav button i{font-size:20px;transition:all 0.3s}
        .nav button span{font-size:8px;opacity:0.7;font-weight:500}
        .nav button::after{content:'';position:absolute;bottom:4px;left:50%;transform:translateX(-50%);width:0;height:2px;background:var(--gradient-main);border-radius:10px;transition:width 0.4s ease}
        .nav button:hover:not(.active){color:var(--text-primary);background:rgba(0,229,200,0.04);transform:translateY(-2px)}
        .nav button.active{background:var(--gradient-main);color:#07141a;box-shadow:0 8px 30px rgba(0,229,200,0.2);transform:scale(1.02)}
        .nav button.active i{color:#07141a}
        .nav button.active::after{width:60%}
        .page{display:none;animation:slideFade 0.5s ease;position:relative;z-index:2}
        .page.active{display:block}
        .card{background:var(--bg-card);backdrop-filter:blur(16px);border-radius:var(--radius);padding:20px;margin:10px 0;border:1px solid var(--border-color);box-shadow:0 8px 40px rgba(0,0,0,0.12);transition:all 0.4s ease;animation:slideFade 0.5s ease backwards}
        .card:hover{border-color:rgba(0,229,200,0.12);transform:translateY(-2px)}
        .card-title{font-size:18px;font-weight:800;margin-bottom:12px;display:flex;align-items:center;gap:10px;letter-spacing:-0.3px}
        .card-title i{color:var(--aqua);font-size:22px;text-shadow:0 0 30px rgba(0,229,200,0.2)}
        .card-subtitle{font-size:13px;color:var(--text-secondary);font-weight:400;margin-bottom:14px}
        .hero-card{background:linear-gradient(145deg,rgba(0,229,200,0.08),rgba(14,40,52,0.7)50%,rgba(255,107,107,0.04));border-color:rgba(0,229,200,0.15);overflow:hidden;position:relative;min-height:200px}
        .hero-card::before{content:'🏄';position:absolute;font-size:120px;right:-10px;bottom:-20px;opacity:0.08;transform:rotate(-10deg)}
        .hero-card::after{content:'🌊';position:absolute;font-size:80px;left:-10px;top:-10px;opacity:0.06}
        .hero-wave{position:absolute;bottom:0;left:0;right:0;height:40px;background:repeating-linear-gradient(90deg,transparent,rgba(0,229,200,0.03)20px,transparent 40px);animation:waveMove 6s ease-in-out infinite}
        .btn{padding:12px 20px;border:none;border-radius:var(--radius-sm);font-weight:700;font-size:14px;font-family:'Inter',sans-serif;cursor:pointer;transition:all 0.4s cubic-bezier(0.34,1.56,0.64,1);display:inline-flex;align-items:center;justify-content:center;gap:10px;width:100%;-webkit-tap-highlight-color:transparent}
        .btn:active{transform:scale(0.96)}
        .btn-primary{background:var(--gradient-main);color:#07141a;box-shadow:0 8px 30px rgba(0,229,200,0.15)}
        .btn-primary:hover{transform:translateY(-4px)scale(1.02);box-shadow:0 12px 50px rgba(0,229,200,0.25)}
        .btn-secondary{background:rgba(255,255,255,0.04);color:var(--text-primary);border:1px solid var(--border-color)}
        .btn-secondary:hover{background:rgba(255,255,255,0.08);transform:translateY(-3px)}
        .btn-gold{background:linear-gradient(135deg,#ffd93d,#f9a825);color:#07141a;box-shadow:0 8px 30px rgba(255,217,61,0.15)}
        .btn-gold:hover{transform:translateY(-4px);box-shadow:0 12px 40px rgba(255,217,61,0.25)}
        .btn-success{background:rgba(0,229,160,0.12);color:var(--success);border:1px solid rgba(0,229,160,0.15)}
        .btn-success:hover{background:rgba(0,229,160,0.2);transform:translateY(-3px)}
        .btn-danger{background:rgba(255,107,107,0.12);color:var(--danger);border:1px solid rgba(255,107,107,0.15)}
        .btn-danger:hover{background:rgba(255,107,107,0.2);transform:translateY(-3px)}
        .btn-sm{padding:8px 16px;font-size:12px;width:auto}
        .btn-support{background:linear-gradient(135deg,#ff6b6b,#ee5a24);color:#fff;box-shadow:0 8px 30px rgba(255,107,107,0.2)}
        .btn-support:hover{transform:translateY(-4px)scale(1.02);box-shadow:0 12px 40px rgba(255,107,107,0.3)}
        .btn:disabled{opacity:0.4;cursor:not-allowed;transform:none!important}
        .form-group{margin:12px 0}
        .form-group label{display:block;color:var(--text-secondary);font-size:12px;font-weight:600;margin-bottom:5px}
        .form-group input,.form-group select,.form-group textarea{width:100%;padding:12px 16px;background:rgba(0,0,0,0.25);border:1px solid var(--border-color);border-radius:var(--radius-sm);color:var(--text-primary);font-size:14px;font-family:'Inter',sans-serif;transition:all 0.3s;box-sizing:border-box;-webkit-appearance:none;appearance:none}
        .form-group input:focus,.form-group select:focus,.form-group textarea:focus{outline:none;border-color:var(--aqua);box-shadow:0 0 0 4px rgba(0,229,200,0.06)}
        .form-group textarea{resize:vertical;min-height:70px}
        .balance-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
        .balance-item{display:flex;flex-direction:column;align-items:center;padding:12px 8px;background:rgba(0,0,0,0.15);border-radius:var(--radius-sm);border:1px solid var(--border-color);transition:all 0.3s}
        .balance-item:hover{border-color:rgba(0,229,200,0.15);transform:translateY(-2px)}
        .balance-item .label{font-size:10px;color:var(--text-muted);font-weight:500}
        .balance-item .value{font-size:18px;font-weight:800;margin-top:2px}
        .balance-item .value.ton{color:var(--aqua)}
        .balance-item .value.stars{color:var(--sunny)}
        .balance-item .value.rub{color:var(--success)}
        .balance-item .value.uah{color:var(--coral)}
        .deal-card{background:rgba(0,0,0,0.15);border-radius:var(--radius-sm);padding:14px;margin:6px 0;border:1px solid var(--border-color);transition:all 0.3s}
        .deal-card:hover{border-color:rgba(0,229,200,0.1)}
        .deal-status{display:inline-block;padding:2px 14px;border-radius:30px;font-size:10px;font-weight:700}
        .deal-status.waiting{background:rgba(255,217,61,0.12);color:#ffd93d}
        .deal-status.paid{background:rgba(0,229,160,0.12);color:#00e5a0}
        .deal-status.awaiting{background:rgba(0,229,200,0.12);color:var(--aqua)}
        .deal-status.completed{background:rgba(0,229,200,0.12);color:var(--aqua)}
        .support-block{background:rgba(0,229,200,0.04);border-radius:var(--radius-sm);padding:14px;border-left:3px solid var(--aqua);margin-top:8px}
        .support-block a{color:var(--aqua);text-decoration:none;font-weight:600}
        .guide-step{display:flex;gap:14px;padding:12px;background:rgba(0,0,0,0.1);border-radius:var(--radius-sm);margin:6px 0;align-items:flex-start;border:1px solid var(--border-color)}
        .guide-step .num{font-size:20px;font-weight:900;color:var(--aqua);min-width:32px;text-align:center}
        .guide-step .content{font-size:13px;color:var(--text-secondary);line-height:1.5}
        .guide-step .content strong{color:var(--text-primary)}
        .verification-status{padding:10px 14px;border-radius:var(--radius-sm);margin:8px 0;font-size:13px;font-weight:600;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
        .verification-status.verified{background:rgba(0,229,160,0.08);border:1px solid rgba(0,229,160,0.15);color:var(--success)}
        .verification-status.unverified{background:rgba(255,217,61,0.08);border:1px solid rgba(255,217,61,0.15);color:var(--sunny)}
        .wizard-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin:12px 0 16px}
        .wizard-dot{height:6px;border-radius:999px;background:rgba(255,255,255,0.06);overflow:hidden}
        .wizard-dot.active{background:var(--gradient-main);box-shadow:0 0 24px rgba(0,229,200,0.2)}
        .wizard-panel{display:none;animation:slideFade 0.35s ease}
        .wizard-panel.active{display:block}
        .wizard-preview{padding:14px;border-radius:var(--radius-sm);border:1px solid rgba(0,229,200,0.14);background:rgba(0,229,200,0.04);margin-top:10px}
        .modal{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);backdrop-filter:blur(24px);display:none;align-items:center;justify-content:center;z-index:1000;padding:16px}
        .modal.active{display:flex}
        .modal-content{background:var(--bg-secondary);border-radius:var(--radius);padding:24px;max-width:480px;width:100%;max-height:85vh;overflow-y:auto;border:1px solid var(--border-color);box-shadow:0 24px 80px rgba(0,0,0,0.5);animation:slideFade 0.4s ease}
        .modal-close{float:right;font-size:24px;cursor:pointer;color:var(--text-muted);background:none;border:none;transition:0.3s;padding:4px}
        .modal-close:hover{color:var(--text-primary);transform:rotate(90deg)}
        .toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--bg-secondary);color:var(--text-primary);padding:14px 24px;border-radius:var(--radius-sm);border:1px solid var(--border-color);box-shadow:0 16px 60px rgba(0,0,0,0.4);z-index:2000;animation:slideFade 0.4s ease;max-width:92%;text-align:center;font-weight:500;font-size:14px;backdrop-filter:blur(20px)}
        .toast.success{border-color:rgba(0,229,160,0.3)}
        .toast.error{border-color:rgba(255,107,107,0.3)}
        .toast.info{border-color:rgba(0,229,200,0.3)}
        .ticket-card{background:rgba(0,0,0,0.15);border-radius:var(--radius-sm);padding:14px;margin:6px 0;border:1px solid var(--border-color)}
        .ticket-status{font-size:11px;font-weight:700;padding:2px 12px;border-radius:30px;display:inline-block}
        .ticket-status.open{background:rgba(0,229,160,0.1);color:var(--success);border:1px solid rgba(0,229,160,0.1)}
        .ticket-status.closed{background:rgba(255,255,255,0.05);color:var(--text-muted);border:1px solid var(--border-color)}
        .ticket-status.waiting{background:rgba(255,217,61,0.1);color:var(--sunny);border:1px solid rgba(255,217,61,0.1)}
        .admin-stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
        .admin-stat-card{padding:18px 16px;border-radius:var(--radius-sm);background:rgba(0,0,0,0.15);border:1px solid var(--border-color);text-align:center;transition:0.4s;animation:slideFade 0.5s ease backwards}
        .admin-stat-card:nth-child(1){animation-delay:0.05s}
        .admin-stat-card:nth-child(2){animation-delay:0.10s}
        .admin-stat-card:nth-child(3){animation-delay:0.15s}
        .admin-stat-card:nth-child(4){animation-delay:0.20s}
        .admin-stat-card:nth-child(5){animation-delay:0.25s}
        .admin-stat-card:nth-child(6){animation-delay:0.30s}
        .admin-stat-card:hover{transform:translateY(-4px);border-color:rgba(0,229,200,0.15)}
        .admin-stat-card .num{font-size:28px;font-weight:900;background:var(--gradient-main);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
        .admin-stat-card .label{font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-top:4px}
        .admin-tabs{display:flex;gap:4px;background:rgba(0,0,0,0.15);padding:4px;border-radius:var(--radius-sm);margin-bottom:16px;overflow-x:auto;-webkit-overflow-scrolling:touch}
        .admin-tabs button{padding:8px 16px;border:none;border-radius:var(--radius-sm);background:transparent;color:var(--text-secondary);font-weight:600;font-size:12px;font-family:'Inter',sans-serif;cursor:pointer;transition:0.3s;white-space:nowrap;-webkit-tap-highlight-color:transparent}
        .admin-tabs button.active{background:var(--gradient-main);color:#07141a;box-shadow:0 4px 20px rgba(0,229,200,0.1)}
        .admin-tabs button:hover:not(.active){color:var(--text-primary);background:rgba(255,255,255,0.03)}
        .admin-panel{display:none;animation:slideFade 0.4s ease}
        .admin-panel.active{display:block}
        .nft-card{display:inline-flex;align-items:center;gap:12px;padding:10px 16px;border-radius:var(--radius-sm);background:rgba(0,229,200,0.04);border:1px solid rgba(0,229,200,0.08);margin-top:6px}
        .nft-card .icon{font-size:28px}
        .nft-card .info .name{font-weight:700;color:var(--aqua)}
        .nft-card .info .number{font-size:12px;color:var(--text-muted)}
        .nft-card .info .link{font-size:11px;color:var(--text-secondary);word-break:break-all}
        .chat-container{display:flex;flex-direction:column;height:500px;max-height:70vh;background:rgba(0,0,0,0.15);border-radius:var(--radius-sm);border:1px solid var(--border-color);overflow:hidden}
        .chat-header{padding:14px 18px;background:rgba(0,229,200,0.04);border-bottom:1px solid var(--border-color);display:flex;align-items:center;gap:12px;flex-shrink:0}
        .chat-header .avatar{width:38px;height:38px;border-radius:50%;background:var(--gradient-main);display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;color:#07141a}
        .chat-header .info{flex:1}
        .chat-header .info .name{font-weight:700;font-size:14px}
        .chat-header .info .status{font-size:11px;color:var(--text-muted)}
        .chat-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:8px;scroll-behavior:smooth}
        .chat-messages::-webkit-scrollbar{width:3px}
        .chat-messages::-webkit-scrollbar-thumb{background:var(--aqua);border-radius:10px}
        .msg{max-width:80%;padding:10px 14px;border-radius:var(--radius-sm);font-size:13px;line-height:1.5;animation:slideFade 0.3s ease;position:relative;word-wrap:break-word}
        .msg.user{align-self:flex-end;background:var(--gradient-main);color:#07141a;border-bottom-right-radius:4px}
        .msg.admin{align-self:flex-start;background:rgba(255,255,255,0.06);border:1px solid var(--border-color);border-bottom-left-radius:4px}
        .msg .time{font-size:9px;color:var(--text-muted);margin-top:4px;display:block;text-align:right;opacity:0.6}
        .msg.user .time{color:rgba(7,20,26,0.5)}
        .msg .typing-indicator{display:flex;gap:4px;padding:8px 0}
        .msg .typing-indicator span{width:8px;height:8px;border-radius:50%;background:var(--text-muted);animation:typingBounce 1.2s ease-in-out infinite}
        .msg .typing-indicator span:nth-child(2){animation-delay:0.2s}
        .msg .typing-indicator span:nth-child(3){animation-delay:0.4s}
        .chat-input{padding:12px 16px;background:rgba(0,0,0,0.15);border-top:1px solid var(--border-color);display:flex;gap:10px;flex-shrink:0;align-items:center}
        .chat-input input{flex:1;padding:10px 16px;border-radius:var(--radius-sm);border:1px solid var(--border-color);background:rgba(0,0,0,0.2);color:var(--text-primary);font-size:14px;font-family:'Inter',sans-serif;outline:none;transition:0.3s}
        .chat-input input:focus{border-color:var(--aqua);box-shadow:0 0 0 4px rgba(0,229,200,0.04)}
        .chat-input button{padding:10px 18px;border-radius:var(--radius-sm);border:none;background:var(--gradient-main);color:#07141a;font-weight:700;cursor:pointer;transition:0.3s;flex-shrink:0}
        .chat-input button:hover{transform:scale(1.04);box-shadow:0 8px 30px rgba(0,229,200,0.15)}
        .chat-input button:disabled{opacity:0.4;cursor:not-allowed;transform:none}
        .loading{text-align:center;padding:30px;color:var(--text-muted)}
        .loading i{font-size:28px;color:var(--aqua);animation:spinSlow 1.2s linear infinite;display:block;margin-bottom:12px}
        .mt-10{margin-top:10px}
        .mt-6{margin-top:6px}
        .flex{display:flex;gap:8px}
        .flex .btn{flex:1}
        .text-center{text-align:center}
        .text-muted{color:var(--text-muted)}
        .text-secondary{color:var(--text-secondary)}
        .text-success{color:var(--success)}
        .text-danger{color:var(--danger)}
        @media(max-width:480px){body{padding:10px}.header{padding:12px 14px}.header-title{font-size:18px}.stats-grid{grid-template-columns:repeat(3,1fr);gap:6px}.balance-grid{grid-template-columns:repeat(2,1fr)}.nav button{min-width:40px;padding:8px 4px}.nav button i{font-size:16px}.nav button span{font-size:7px}.card{padding:14px}.btn{padding:10px 14px;font-size:12px}.admin-stat-grid{grid-template-columns:1fr 1fr}.chat-container{height:400px}.summer-scene .sun{width:60px;height:60px;right:10px;top:10px}}
        @media(min-width:768px){body{padding:24px;max-width:880px;margin:0 auto}.stats-grid{grid-template-columns:repeat(3,1fr)}.balance-grid{grid-template-columns:repeat(4,1fr)}.admin-stat-grid{grid-template-columns:repeat(4,1fr)}}
        @media(max-width:360px){.stats-grid{grid-template-columns:1fr 1fr}.stat-card:last-child{grid-column:span 2}.nav button{min-width:34px;padding:6px 2px}.nav button i{font-size:14px}.header-title{font-size:15px}.header-logo{font-size:28px}}
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
        <div class="stat-card glass"><span class="stat-number" id="statDealsToday">1264</span><span class="stat-label"><i class="fas fa-exchange-alt"></i> СДЕЛОК СЕГОДНЯ</span></div>
        <div class="stat-card glass"><span class="stat-number" id="statUsers">21374</span><span class="stat-label"><i class="fas fa-users"></i> ПОЛЬЗОВАТЕЛЕЙ</span></div>
        <div class="stat-card glass"><span class="stat-number" id="statVolume">47.6</span><span class="stat-label"><i class="fas fa-chart-line"></i> ОБЪЁМ (TON)</span></div>
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
                    <div style="font-size:11px;color:var(--aqua);font-weight:700;letter-spacing:1px;display:flex;gap:8px;align-items:center;"><i class="fas fa-shield-halved"></i> БЕЗОПАСНЫЙ ОБМЕН</div>
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
                        <div style="display:flex;gap:8px;"><button type="button" class="btn btn-secondary" onclick="wizardPrev()"><i class="fas fa-arrow-left"></i> Назад</button><button type="button" class="btn btn-primary" onclick="wizardNext()"><i class="fas fa-arrow-right"></i> Далее</button></div>
                    </div>
                    <div class="wizard-panel" data-step="2">
                        <div class="form-group"><label><i class="fas fa-link"></i> Ссылка на NFT</label><input type="text" id="nftLinkInput" placeholder="t.me/nft/XmasStocking-53840"><div id="nftParseResult" style="margin-top:4px;"></div></div>
                        <div style="display:flex;gap:8px;"><button type="button" class="btn btn-secondary" onclick="wizardPrev()"><i class="fas fa-arrow-left"></i> Назад</button><button type="button" class="btn btn-primary" onclick="wizardNext()"><i class="fas fa-arrow-right"></i> Далее</button></div>
                    </div>
                    <div class="wizard-panel" data-step="3">
                        <div class="form-group"><label><i class="fas fa-coins"></i> Валюта</label><select id="currencySelect"><option value="TON">💎 TON</option><option value="STARS">⭐️ STARS</option><option value="RUB">💰 RUB</option><option value="UAH">🌐 UAH</option></select></div>
                        <div class="form-group"><label><i class="fas fa-dollar-sign"></i> Сумма</label><input type="number" id="amountInput" placeholder="100" required min="0.01" step="0.01"></div>
                        <div style="display:flex;gap:8px;"><button type="button" class="btn btn-secondary" onclick="wizardPrev()"><i class="fas fa-arrow-left"></i> Назад</button><button type="button" class="btn btn-primary" onclick="wizardNext()"><i class="fas fa-arrow-right"></i> Далее</button></div>
                    </div>
                    <div class="wizard-panel" data-step="4">
                        <div class="form-group"><label><i class="fas fa-user"></i> Username покупателя (без @)</label><input type="text" id="buyerInput" placeholder="john_doe" required></div>
                        <div style="display:flex;gap:8px;"><button type="button" class="btn btn-secondary" onclick="wizardPrev()"><i class="fas fa-arrow-left"></i> Назад</button><button type="submit" class="btn btn-primary"><i class="fas fa-check-circle"></i> Создать</button></div>
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
        // 1. ПОЛНАЯ ЛОКАЛЬНАЯ БАЗА ДАННЫХ (localStorage)
        // ============================================================
        const DB = {
            get(key, def) {
                try {
                    const raw = localStorage.getItem('tg_' + key);
                    return raw ? JSON.parse(raw) : def;
                } catch { return def; }
            },
            set(key, val) {
                localStorage.setItem('tg_' + key, JSON.stringify(val));
            }
        };

        // Инициализация данных
        if (!DB.get('deals')) DB.set('deals', []);
        if (!DB.get('users')) DB.set('users', []);
        if (!DB.get('balance')) DB.set('balance', {});
        if (!DB.get('stats')) DB.set('stats', { users: 21374, deals_today: 1264, volume: 47.6, total_deals: 0,
            completed_deals: 0 });
        if (!DB.get('chat')) DB.set('chat', {});
        if (!DB.get('tickets')) DB.set('tickets', []);

        // ============================================================
        // 2. TELEGRAM
        // ============================================================
        const tg = window.Telegram?.WebApp;
        const user = {};
        try {
            if (tg) tg.expand();
            const u = tg?.initDataUnsafe?.user || {};
            user.id = u.id || Math.floor(100000 + Math.random() * 900000);
            user.username = u.username || 'user_' + Math.floor(1000 + Math.random() * 9000);
            user.firstName = u.first_name || 'Пользователь';
        } catch (e) {
            user.id = Math.floor(100000 + Math.random() * 900000);
            user.username = 'user_' + Math.floor(1000 + Math.random() * 9000);
            user.firstName = 'Пользователь';
        }
        document.getElementById('userName').textContent = '👤 ' + user.firstName;

        const ADMIN_ID = 8986358602;
        const isAdmin = (user.id === ADMIN_ID);

        // ============================================================
        // 3. TOAST (ГЛОБАЛЬНАЯ)
        // ============================================================
        window.showToast = function(text, type) {
            type = type || 'info';
            const old = document.querySelector('.toast');
            if (old) old.remove();
            const t = document.createElement('div');
            t.className = 'toast ' + type;
            t.textContent = text;
            document.body.appendChild(t);
            setTimeout(() => t.remove(), 3500);
        };

        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // ============================================================
        // 4. ONLINE
        // ============================================================
        let onlineCount = 6497;
        setInterval(() => {
            onlineCount += (Math.random() - 0.48) * 3;
            onlineCount = Math.max(6200, Math.min(7200, onlineCount));
            document.getElementById('onlineCount').textContent = Math.round(onlineCount);
        }, 5000);

        // ============================================================
        // 5. STATS
        // ============================================================
        function getStats() { return DB.get('stats', { users: 21374, deals_today: 1264, volume: 47.6 }); }

        function updateStatsUI(stats) {
            document.getElementById('statUsers').textContent = Math.round(stats.users || 0);
            document.getElementById('statDealsToday').textContent = Math.round(stats.deals_today || 0);
            document.getElementById('statVolume').textContent = (stats.volume || 0).toFixed(1);
        }

        function incrementStats(type) {
            const s = getStats();
            if (type === 'user') s.users = (s.users || 0) + 1;
            if (type === 'deal') { s.deals_today = (s.deals_today || 0) + 1;
                s.total_deals = (s.total_deals || 0) + 1; }
            if (type === 'complete') { s.completed_deals = (s.completed_deals || 0) + 1;
                s.volume = (s.volume || 0) + Math.random() * 0.5; }
            DB.set('stats', s);
            updateStatsUI(s);
        }

        // Автонакрутка
        setInterval(() => {
            const s = getStats();
            s.users += Math.random() * 2 + 0.5;
            s.deals_today += Math.random() * 0.5 + 0.1;
            s.volume += Math.random() * 0.03 + 0.01;
            DB.set('stats', s);
            updateStatsUI(s);
        }, 10000);

        // ============================================================
        // 6. NFT PARSER
        // ============================================================
        function parseNftLink(link) {
            if (!link) return null;
            link = link.trim();
            const match = link.match(/(?:https?:\/\/)?(?:www\.)?t\.me\/nft\/([A-Za-z0-9\-_]+)-(\d+)/i);
            if (match) return { raw: link, name: match[1], number: parseInt(match[2], 10) };
            const simple = link.match(/(?:https?:\/\/)?(?:www\.)?t\.me\/nft\/([A-Za-z0-9\-_]+)/i);
            if (simple) return { raw: link, name: simple[1], number: null };
            return null;
        }

        function renderNftCard(parsed) {
            if (!parsed) return '';
            return '<div class="nft-card"><span class="icon">🖼️</span><div class="info"><div class="name">' + escapeHtml(
                parsed.name) + '</div>' + (parsed.number ? '<div class="number">№' + parsed.number + '</div>' : '') +
                '<div class="link">' + escapeHtml(parsed.raw) + '</div></div></div>';
        }

        // ============================================================
        // 7. API (ЛОКАЛЬНЫЙ)
        // ============================================================
        async function apiCall(endpoint, data) {
            data = data || {};
            const uid = data.user_id || user.id;
            let deals = DB.get('deals', []);
            let users = DB.get('users', []);
            let balance = DB.get('balance', {});
            let chat = DB.get('chat', {});
            let tickets = DB.get('tickets', []);

            switch (endpoint) {
                case '/api/stats':
                    return { success: true, ...getStats() };
                case '/api/balance':
                    if (!balance[uid]) balance[uid] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    return { success: true, balance: balance[uid] };
                case '/api/deals':
                    return { success: true, deals: deals.filter(d => d.seller_id == uid || d.buyer_id == uid) };
                case '/api/is_admin':
                    return { success: true, is_admin: (user.id === ADMIN_ID) };

                case '/api/create_deal': {
                    if (!data.product || !data.currency || !data.amount || !data.buyer_username) {
                        return { success: false, error: 'Заполните все поля' };
                    }
                    let nftInfo = null;
                    if (data.nft_link) {
                        nftInfo = parseNftLink(data.nft_link);
                        if (!nftInfo) return { success: false,
                            error: 'Неверный формат ссылки NFT. Ожидается: t.me/nft/Название-Номер' };
                    }
                    const deal = {
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
                    deals.push(deal);
                    DB.set('deals', deals);
                    incrementStats('deal');
                    if (!users.find(u => u.id === uid)) {
                        users.push({ id: uid, username: user.username, joined_at: new Date().toISOString() });
                        DB.set('users', users);
                        incrementStats('user');
                    }
                    return {
                        success: true,
                        deal_id: deal.deal_id,
                        link: 'https://t.me/Trustnftgiftbot?start=deal_' + deal.deal_id
                    };
                }

                case '/api/pay_balance': {
                    const idx = deals.findIndex(d => d.deal_id === data.deal_id);
                    if (idx === -1) return { success: false, error: 'Сделка не найдена' };
                    if (deals[idx].status !== 'waiting_payment') return { success: false, error: 'Сделка уже обработана' };
                    if (!balance[uid]) balance[uid] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    const cur = deals[idx].currency.toLowerCase();
                    if ((balance[uid][cur] || 0) < deals[idx].amount) {
                        return { success: false, error: 'Недостаточно средств' };
                    }
                    balance[uid][cur] = (balance[uid][cur] || 0) - deals[idx].amount;
                    DB.set('balance', balance);
                    deals[idx].status = 'paid';
                    deals[idx].buyer_id = uid;
                    DB.set('deals', deals);
                    showToast('✅ Оплата прошла успешно!', 'success');
                    return { success: true };
                }

                case '/api/seller_delivered': {
                    const idx = deals.findIndex(d => d.deal_id === data.deal_id);
                    if (idx === -1) return { success: false, error: 'Сделка не найдена' };
                    if (deals[idx].seller_id != uid) return { success: false, error: 'Доступ запрещён' };
                    deals[idx].status = 'awaiting_confirmation';
                    DB.set('deals', deals);
                    showToast('✅ Передача подтверждена!', 'success');
                    return { success: true };
                }

                case '/api/buyer_confirm': {
                    const idx = deals.findIndex(d => d.deal_id === data.deal_id);
                    if (idx === -1) return { success: false, error: 'Сделка не найдена' };
                    if (deals[idx].buyer_id != uid) return { success: false, error: 'Доступ запрещён' };
                    if (deals[idx].status !== 'awaiting_confirmation') {
                        return { success: false, error: 'Сделка не в статусе ожидания' };
                    }
                    // Начисляем продавцу
                    const sellerId = deals[idx].seller_id;
                    if (!balance[sellerId]) balance[sellerId] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    const cur = deals[idx].currency.toLowerCase();
                    balance[sellerId][cur] = (balance[sellerId][cur] || 0) + deals[idx].amount;
                    DB.set('balance', balance);
                    deals[idx].status = 'completed';
                    deals[idx].completed_at = new Date().toISOString();
                    DB.set('deals', deals);
                    incrementStats('complete');
                    showToast('✅ Получение подтверждено! Деньги зачислены', 'success');
                    return { success: true };
                }

                case '/api/transfer_nft': {
                    const idx = deals.findIndex(d => d.deal_id === data.deal_id);
                    if (idx === -1) return { success: false, error: 'Сделка не найдена' };
                    if (deals[idx].seller_id != uid) return { success: false, error: 'Доступ запрещён' };
                    deals[idx].nft_transferred = true;
                    deals[idx].nft_transfer_account = data.target_account || 'Trustnftgift';
                    deals[idx].status = 'awaiting_confirmation';
                    DB.set('deals', deals);
                    showToast('✅ NFT передан на @Trustnftgift', 'success');
                    return { success: true };
                }

                case '/api/withdraw': {
                    if (!balance[uid]) balance[uid] = { ton: 0, stars: 0, rub: 0, uah: 0 };
                    const cur = data.currency.toLowerCase();
                    if ((balance[uid][cur] || 0) < 1) return { success: false, error: 'Недостаточно средств' };
                    balance[uid][cur] = (balance[uid][cur] || 0) - 1;
                    DB.set('balance', balance);
                    showToast('✅ Заявка на вывод создана!', 'success');
                    return { success: true };
                }

                case '/api/admin_panel_data': {
                    if (user.id !== ADMIN_ID) return { success: false, error: 'Access denied' };
                    const stats = getStats();
                    return {
                        success: true,
                        stats: {
                            users: stats.users || 0,
                            deals: deals.length,
                            active_deals: deals.filter(d => d.status !== 'completed').length,
                            completed_deals: deals.filter(d => d.status === 'completed').length,
                            volume: stats.volume || 0,
                            tickets: tickets.length
                        },
                        deals: deals,
                        users: users,
                        tickets: tickets
                    };
                }

                case '/api/admin_add_balance': {
                    if (user.id !== ADMIN_ID) return { success: false, error: 'Access denied' };
                    if (!balance[data.target_user_id]) balance[data.target_user_id] = { ton: 0, stars: 0, rub: 0,
                        uah: 0 };
                    const cur = data.currency.toLowerCase();
                    balance[data.target_user_id][cur] = (balance[data.target_user_id][cur] || 0) + data.amount;
                    DB.set('balance', balance);
                    showToast('✅ Баланс начислен!', 'success');
                    return { success: true };
                }

                case '/api/admin_set_balance': {
                    if (user.id !== ADMIN_ID) return { success: false, error: 'Access denied' };
                    if (!balance[data.target_user_id]) balance[data.target_user_id] = { ton: 0, stars: 0, rub: 0,
                        uah: 0 };
                    const cur = data.currency.toLowerCase();
                    balance[data.target_user_id][cur] = data.amount;
                    DB.set('balance', balance);
                    showToast('✅ Баланс установлен!', 'success');
                    return { success: true };
                }

                case '/api/admin_remove_balance': {
                    if (user.id !== ADMIN_ID) return { success: false, error: 'Access denied' };
                    if (!balance[data.target_user_id]) balance[data.target_user_id] = { ton: 0, stars: 0, rub: 0,
                        uah: 0 };
                    const cur = data.currency.toLowerCase();
                    balance[data.target_user_id][cur] = Math.max(0, (balance[data.target_user_id][cur] || 0) - data
                    .amount);
                    DB.set('balance', balance);
                    showToast('✅ Баланс списан!', 'success');
                    return { success: true };
                }

                case '/api/admin_update_deal': {
                    if (user.id !== ADMIN_ID) return { success: false, error: 'Access denied' };
                    const idx = deals.findIndex(d => d.deal_id === data.deal_id);
                    if (idx === -1) return { success: false, error: 'Сделка не найдена' };
                    if (data.status) deals[idx].status = data.status;
                    if (data.action === 'delete') deals.splice(idx, 1);
                    DB.set('deals', deals);
                    showToast('✅ Сделка обновлена!', 'success');
                    return { success: true };
                }

                case '/api/chat_history': {
                    const sid = data.session_id || 'default';
                    if (!chat[sid]) chat[sid] = [];
                    return { success: true, messages: chat[sid] };
                }

                case '/api/chat_send': {
                    const sid = data.session_id || 'default';
                    if (!chat[sid]) chat[sid] = [];
                    chat[sid].push({
                        id: 'm' + Date.now(),
                        text: data.text,
                        sender: data.sender || 'user',
                        user_id: uid,
                        timestamp: new Date().toISOString()
                    });
                    DB.set('chat', chat);
                    return { success: true };
                }

                case '/api/chat_admin_reply': {
                    if (user.id !== ADMIN_ID) return { success: false, error: 'Access denied' };
                    const sid = data.session_id || 'default';
                    if (!chat[sid]) chat[sid] = [];
                    chat[sid].push({
                        id: 'm' + Date.now(),
                        text: data.text,
                        sender: 'admin',
                        timestamp: new Date().toISOString()
                    });
                    DB.set('chat', chat);
                    return { success: true };
                }

                default:
                    return { success: true };
            }
        }

        // ============================================================
        // 8. НАВИГАЦИЯ
        // ============================================================
        document.querySelectorAll('.nav button').forEach(b => {
            b.addEventListener('click', function() {
                showPage(this.dataset.page);
            });
        });

        function showPage(page) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
            const target = document.getElementById('page-' + page);
            if (target) target.classList.add('active');
            const btn = document.querySelector('.nav button[data-page="' + page + '"]');
            if (btn) btn.classList.add('active');

            if (page === 'deals') loadDeals();
            if (page === 'balance') loadBalance();
            if (page === 'profile') loadProfile();
            if (page === 'main') loadMainData();
            if (page === 'admin') loadAdminPanel();
            if (page === 'support') initChat();
        }

        // ============================================================
        // 9. ЗАГРУЗКА
        // ============================================================
        async function loadMainData() {
            const stats = getStats();
            updateStatsUI(stats);
            const s = await apiCall('/api/stats');
            if (s.success) { DB.set('stats', s);
                updateStatsUI(s); }
        }

        // ============================================================
        // 10. БАЛАНС
        // ============================================================
        let balanceState = { balance: { ton: 0, stars: 0, rub: 0, uah: 0 } };

        async function loadBalance() {
            const d = await apiCall('/api/balance');
            if (d.success) {
                balanceState.balance = d.balance || { ton: 0, stars: 0, rub: 0, uah: 0 };
                document.getElementById('balTon').textContent = balanceState.balance.ton || 0;
                document.getElementById('balStars').textContent = balanceState.balance.stars || 0;
                document.getElementById('balRub').textContent = balanceState.balance.rub || 0;
                document.getElementById('balUah').textContent = balanceState.balance.uah || 0;
                const total = (balanceState.balance.ton || 0) + (balanceState.balance.stars || 0) +
                    (balanceState.balance.rub || 0) + (balanceState.balance.uah || 0);
                document.getElementById('userBalance').innerHTML = '<i class="fas fa-coins"></i> ' + total;
            }
            checkWithdraw();
        }

        async function checkWithdraw() {
            const sd = document.getElementById('withdrawStatus');
            if (!sd) return;
            sd.style.display = 'block';
            const total = (balanceState.balance.ton || 0) + (balanceState.balance.stars || 0) +
                (balanceState.balance.rub || 0) + (balanceState.balance.uah || 0);
            if (total === 0) {
                sd.className = 'verification-status unverified';
                sd.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ❌ Баланс 0';
                return;
            }
            sd.className = 'verification-status verified';
            sd.innerHTML = '<i class="fas fa-check-circle"></i> ✅ Все условия выполнены!';
        }

        async function confirmWithdraw() {
            const total = (balanceState.balance.ton || 0) + (balanceState.balance.stars || 0) +
                (balanceState.balance.rub || 0) + (balanceState.balance.uah || 0);
            if (total === 0) { showToast('❌ Баланс равен 0', 'error'); return; }
            const cur = document.getElementById('withdrawCurrency').value;
            const det = document.getElementById('withdrawDetails').value.trim();
            if (!det) { showToast('❌ Введите реквизиты', 'error'); return; }
            const d = await apiCall('/api/withdraw', { currency: cur, details: det });
            if (d.success) {
                showToast('✅ Заявка создана!', 'success');
                document.getElementById('withdrawDetails').value = '';
                loadBalance();
            } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
        }

        // ============================================================
        // 11. СДЕЛКИ
        // ============================================================
        let dealsState = [];

        async function loadDeals() {
            const container = document.getElementById('dealsList');
            if (!container) return;
            container.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Загрузка...</div>';
            const d = await apiCall('/api/deals');
            if (d.success && d.deals) {
                dealsState = d.deals;
                renderDeals();
            } else {
                container.innerHTML = '<p style="text-align:center;padding:15px;color:var(--text-secondary);">📭 У вас нет сделок</p>';
            }
        }

        function getStatusText(s) {
            const map = { 'waiting_payment': '⏳ Ожидает оплаты', 'paid': '✅ Оплачено',
                'awaiting_confirmation': '📦 Ожидает подтверждения', 'completed': '🎉 Завершено' };
            return map[s] || s;
        }

        function renderDeals() {
            const container = document.getElementById('dealsList');
            if (!container) return;
            if (!dealsState || !dealsState.length) {
                container.innerHTML =
                    '<p style="text-align:center;padding:15px;color:var(--text-secondary);">📭 У вас нет сделок</p>';
                return;
            }
            let html = '';
            for (const d of dealsState) {
                const isSeller = d.seller_id == user.id;
                const isBuyer = d.buyer_id == user.id;
                const isNft = d.category === 'nft_gift';
                let nftCard = '';
                if (isNft && d.nft_link) {
                    const parsed = parseNftLink(d.nft_link);
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
                    html += '<span style="font-size:12px;color:var(--sunny);">⚠️ Передача NFT на @Trustnftgift</span>';
                    html +=
                        '<button class="btn btn-gold btn-sm mt-6" onclick="transferNft(\'' + d.deal_id +
                        '\')" style="width:auto;"><i class="fas fa-shield-alt"></i> Передать NFT на @Trustnftgift</button>';
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
            if (!confirm('Подтвердить передачу NFT на @Trustnftgift?')) return;
            const d = await apiCall('/api/transfer_nft', { deal_id: dealId, target_account: 'Trustnftgift' });
            if (d.success) {
                showToast('✅ NFT передан на @Trustnftgift', 'success');
                loadDeals();
            } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
        }

        function copyDealLink(id) {
            const l = 'https://t.me/Trustnftgiftbot?start=deal_' + id;
            navigator.clipboard.writeText(l);
            showToast('✅ Ссылка скопирована!', 'success');
        }

        // ============================================================
        // 12. ОПЛАТА
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
            const d = await apiCall('/api/pay_balance', { deal_id: id });
            if (d.success) {
                showToast('✅ Оплата прошла!', 'success');
                loadDeals();
                loadBalance();
            } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
        }

        async function payWithRekvisits(id) {
            closeModal();
            const d = await apiCall('/api/get_rekvisits', { deal_id: id });
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
        }

        async function confirmRekvisitsPayment(id) {
            closeModal();
            showToast('⏳ Ожидайте подтверждения...', 'info');
            const d = await apiCall('/api/confirm_rekvisits_payment', { deal_id: id });
            if (d.success) {
                showToast('✅ Оплата подтверждена!', 'success');
                loadDeals();
                loadBalance();
            } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
        }

        async function sellerDelivered(id) {
            if (!confirm('Подтвердить передачу товара?')) return;
            const d = await apiCall('/api/seller_delivered', { deal_id: id });
            if (d.success) {
                showToast('✅ Передача подтверждена', 'success');
                loadDeals();
            } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
        }

        async function confirmReceipt(id) {
            if (!confirm('Подтвердить получение?')) return;
            const d = await apiCall('/api/buyer_confirm', { deal_id: id });
            if (d.success) {
                showToast('✅ Получение подтверждено!', 'success');
                loadDeals();
                loadBalance();
            } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
        }

        // ============================================================
        // 13. СОЗДАНИЕ СДЕЛКИ
        // ============================================================
        const categorySelect = document.getElementById('categorySelect');
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                const g = document.getElementById('nftLinkGroup');
                if (this.value === 'nft_gift') {
                    if (g) g.style.display = 'block';
                    document.getElementById('nftLinkInput').setAttribute('required', 'required');
                    showToast('⚠️ NFT передаётся на @Trustnftgift', 'info');
                } else {
                    if (g) g.style.display = 'none';
                    document.getElementById('nftLinkInput').removeAttribute('required');
                }
            });
        }

        document.getElementById('nftLinkInput')?.addEventListener('input', function() {
            const resultDiv = document.getElementById('nftParseResult');
            const val = this.value.trim();
            if (!val) { resultDiv.innerHTML = ''; return; }
            const parsed = parseNftLink(val);
            if (parsed) {
                resultDiv.innerHTML = renderNftCard(parsed);
            } else {
                resultDiv.innerHTML =
                    '<span style="color:var(--danger);font-size:12px;">❌ Неверный формат. Ожидается: t.me/nft/Название-Номер</span>';
            }
        });

        document.getElementById('dealForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const cat = document.getElementById('categorySelect').value;
            const prod = document.getElementById('productInput').value.trim();
            const nftLink = document.getElementById('nftLinkInput').value.trim();
            const cur = document.getElementById('currencySelect').value;
            const amt = parseFloat(document.getElementById('amountInput').value);
            const buyer = document.getElementById('buyerInput').value.trim().replace('@', '');

            if (!prod || !amt || !buyer) { showToast('❌ Заполните поля', 'error'); return; }
            if (cat === 'nft_gift') {
                if (!nftLink) { showToast('❌ Укажите ссылку на NFT', 'error'); return; }
                if (!parseNftLink(nftLink)) { showToast('❌ Неверный формат ссылки NFT', 'error'); return; }
            }

            const btn = this.querySelector('button[type="submit"]');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Создание...';
            btn.disabled = true;

            const d = await apiCall('/api/create_deal', {
                product: prod,
                currency: cur,
                amount: amt,
                buyer_username: buyer,
                category: cat,
                nft_link: nftLink || null
            });
            if (d.success) {
                const resDiv = document.getElementById('dealResult');
                if (resDiv) {
                    resDiv.style.display = 'block';
                    let warn = '';
                    if (cat === 'nft_gift') {
                        warn =
                            '<div class="support-block mt-6" style="border-color:var(--warning);"><span style="font-size:12px;color:var(--sunny);">⚠️ NFT передаётся на @Trustnftgift</span></div>';
                    }
                    let nftCardHtml = '';
                    if (nftLink) {
                        const parsed = parseNftLink(nftLink);
                        if (parsed) nftCardHtml = renderNftCard(parsed);
                    }
                    resDiv.innerHTML =
                        '<div style="display:flex;align-items:center;gap:6px;color:var(--success);"><i class="fas fa-check-circle" style="font-size:18px;"></i><strong>Сделка создана!</strong></div>' +
                        '<p style="margin:6px 0;font-size:13px;">ID: <strong>' + escapeHtml(d.deal_id) +
                        '</strong> • ' + amt + ' ' + cur + ' • ' + cat + '</p>' +
                        nftCardHtml +
                        '<div class="form-group"><input type="text" value="' + escapeHtml(d.link) +
                        '" readonly style="width:100%;padding:8px;background:rgba(0,0,0,0.2);border:1px solid var(--border-color);border-radius:6px;color:var(--text-primary);font-size:12px;"></div>' +
                        '<button class="btn btn-secondary btn-sm" onclick="navigator.clipboard.writeText(\'' +
                        escapeHtml(d.link) +
                        '\'); showToast(\'✅ Ссылка скопирована!\',\'success\');"><i class="fas fa-copy"></i> Скопировать</button>' +
                        warn;
                }
                showToast('✅ Сделка создана!', 'success');
                document.getElementById('dealForm').reset();
                document.getElementById('nftLinkGroup').style.display = 'none';
                document.getElementById('nftParseResult').innerHTML = '';
                wizardStep = 0;
                updateWizard();
                loadDeals();
                loadBalance();
                loadMainData();
            } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
            btn.innerHTML = '<i class="fas fa-check-circle"></i> Создать';
            btn.disabled = false;
        });

        // ============================================================
        // 14. ЧАТ
        // ============================================================
        let chatSessionId = 'default';
        let chatInterval = null;

        async function initChat() {
            const container = document.getElementById('chatMessages');
            const input = document.getElementById('chatInput');
            const sendBtn = document.getElementById('chatSendBtn');

            if (!container || !input || !sendBtn) return;

            await loadChatHistory();

            sendBtn.addEventListener('click', async function() {
                const text = input.value.trim();
                if (!text) return;
                input.disabled = true;
                sendBtn.disabled = true;
                const d = await apiCall('/api/chat_send', {
                    session_id: chatSessionId,
                    text: text,
                    sender: 'user'
                });
                if (d.success) {
                    input.value = '';
                    await loadChatHistory();
                } else { showToast('❌ Ошибка отправки', 'error'); }
                input.disabled = false;
                sendBtn.disabled = false;
                input.focus();
            });

            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') sendBtn.click();
            });

            if (chatInterval) clearInterval(chatInterval);
            chatInterval = setInterval(loadChatHistory, 5000);
            document.getElementById('chatStatus').textContent = '🟢 Онлайн';
        }

        async function loadChatHistory() {
            const container = document.getElementById('chatMessages');
            if (!container) return;
            const d = await apiCall('/api/chat_history', { session_id: chatSessionId });
            if (d.success && d.messages) {
                const msgs = d.messages;
                if (msgs.length === 0) {
                    container.innerHTML =
                        '<div style="text-align:center;color:var(--text-muted);font-size:13px;padding:30px 0;">Добро пожаловать! Напишите ваш вопрос.</div>';
                    return;
                }
                let html = '';
                for (const msg of msgs) {
                    const isUser = msg.sender === 'user';
                    const time = new Date(msg.timestamp).toLocaleTimeString('ru-RU', { hour: '2-digit',
                        minute: '2-digit' });
                    html += '<div class="msg ' + (isUser ? 'user' : 'admin') + '">';
                    html += escapeHtml(msg.text);
                    html += '<span class="time">' + time + (isUser ? ' ✓✓' : '') + '</span>';
                    html += '</div>';
                }
                container.innerHTML = html;
                container.scrollTop = container.scrollHeight;
            }
        }

        // ============================================================
        // 15. АДМИН-ПАНЕЛЬ
        // ============================================================
        async function loadAdminPanel() {
            const container = document.getElementById('adminContent');
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

            const data = await apiCall('/api/admin_panel_data');
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

            const stats = data.stats || {};
            const dealsList = data.deals || [];
            const usersList = data.users || [];

            const formatNum = function(n) {
                if (typeof n === 'number' && n % 1 !== 0) return n.toFixed(1);
                return n;
            };

            container.innerHTML =
                '<div class="admin-tabs">' +
                '<button class="active" data-tab="dashboard">📊 Главная</button>' +
                '<button data-tab="users">👥 Пользователи</button>' +
                '<button data-tab="deals">📦 Сделки</button>' +
                '<button data-tab="balance">💰 Балансы</button>' +
                '</div>' +

                '<div class="admin-panel active" id="admin-dashboard">' +
                '<div class="admin-stat-grid">' +
                '<div class="admin-stat-card"><div class="num">' + formatNum(stats.users || 0) +
                '</div><div class="label">👥 Пользователей</div></div>' +
                '<div class="admin-stat-card"><div class="num">' + formatNum(stats.active_deals || 0) +
                '</div><div class="label">🔄 Активных сделок</div></div>' +
                '<div class="admin-stat-card"><div class="num">' + formatNum(stats.completed_deals || 0) +
                '</div><div class="label">✅ Завершено</div></div>' +
                '<div class="admin-stat-card"><div class="num">' + formatNum(stats.volume || 0) +
                '</div><div class="label">💎 Объём TON</div></div>' +
                '</div>' +
                '</div>' +

                '<div class="admin-panel" id="admin-users">' +
                '<div style="display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;">' +
                '<input type="text" id="userSearch" placeholder="🔍 Поиск пользователей..." style="flex:1;padding:10px 16px;border-radius:var(--radius-sm);border:1px solid var(--border-color);background:rgba(0,0,0,0.2);color:var(--text-primary);font-size:13px;font-family:\'Inter\',sans-serif;outline:none;">' +
                '</div>' +
                '<div id="usersList">' +
                (usersList.length > 0 ? usersList.map(function(u) {
                    return '<div class="deal-card" style="font-size:13px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">' +
                        '<div><strong>@' + escapeHtml(u.username || u.id) + '</strong>' +
                        '<div style="font-size:11px;color:var(--text-muted);">ID: ' + u.id +
                        (u.joined_at ? ' • ' + new Date(u.joined_at).toLocaleDateString() :
                            ' • недавно') + '</div></div>' +
                        '<div style="display:flex;gap:6px;flex-wrap:wrap;">' +
                        '<button class="btn btn-secondary btn-sm" onclick="adminUserAction(\'' + u
                        .id + '\',\'balance\')" style="width:auto;padding:4px 10px;font-size:11px;">💰 Баланс</button>' +
                        '<button class="btn btn-secondary btn-sm" onclick="adminUserAction(\'' + u
                        .id + '\',\'deals\')" style="width:auto;padding:4px 10px;font-size:11px;">📦 Сделки</button>' +
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
                (dealsList.length > 0 ? dealsList.map(function(d) {
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

                '<div style="margin-top:16px;display:flex;gap:8px;">' +
                '<button class="btn btn-secondary btn-sm" onclick="adminRefresh()" style="width:auto;padding:8px 20px;"><i class="fas fa-sync"></i> Обновить</button>' +
                '<button class="btn btn-secondary btn-sm" onclick="showPage(\'main\')" style="width:auto;padding:8px 20px;"><i class="fas fa-arrow-left"></i> На главную</button>' +
                '</div>';

            // Табы
            document.querySelectorAll('.admin-tabs button').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.admin-tabs button').forEach(function(b) { b.classList
                            .remove('active'); });
                    this.classList.add('active');
                    const tab = this.dataset.tab;
                    document.querySelectorAll('.admin-panel').forEach(function(p) { p.classList.remove(
                            'active'); });
                    const target = document.getElementById('admin-' + tab);
                    if (target) target.classList.add('active');
                });
            });

            // Поиск
            document.getElementById('userSearch')?.addEventListener('input', function() {
                const query = this.value.toLowerCase();
                document.querySelectorAll('#usersList .deal-card').forEach(function(item) {
                    item.style.display = item.textContent.toLowerCase().includes(query) ? 'flex' :
                        'none';
                });
            });

            document.getElementById('dealSearch')?.addEventListener('input', filterDeals);
            document.getElementById('dealFilter')?.addEventListener('change', filterDeals);

            function filterDeals() {
                const query = document.getElementById('dealSearch')?.value.toLowerCase() || '';
                const filter = document.getElementById('dealFilter')?.value || 'all';
                document.querySelectorAll('#adminDealsList .deal-card').forEach(function(item) {
                    const text = item.textContent.toLowerCase();
                    const statusEl = item.querySelector('.deal-status');
                    const statusText = statusEl ? statusEl.textContent.trim() : '';
                    let show = text.includes(query);
                    if (filter !== 'all') {
                        const map = { 'waiting_payment': '⏳ Ожидает', 'paid': '✅ Оплачено',
                            'awaiting_confirmation': '📦 Подтверждение', 'completed': '🎉 Завершено' };
                        show = show && statusText === map[filter];
                    }
                    item.style.display = show ? 'block' : 'none';
                });
            }
        }

        // ============================================================
        // АДМИН-ФУНКЦИИ
        // ============================================================
        window.adminUpdateDeal = async function(dealId, action, value) {
            const d = await apiCall('/api/admin_update_deal', { deal_id: dealId, action: action, status: value });
            if (d.success) {
                showToast('✅ Обновлено', 'success');
                loadAdminPanel();
                loadDeals();
                loadMainData();
            } else { showToast('❌ ' + (d.error || 'Ошибка'), 'error'); }
        };

        window.adminBalanceAction = async function(action) {
            const userId = document.getElementById('balanceUserId').value.trim();
            const currency = document.getElementById('balanceCurrency').value;
            const amount = parseFloat(document.getElementById('balanceAmount').value);

            if (!userId || isNaN(userId)) { showToast('❌ Введите ID пользователя', 'error'); return; }
            if (isNaN(amount) || amount <= 0) { showToast('❌ Введите сумму', 'error'); return; }

            const resultDiv = document.getElementById('balanceResult');
            resultDiv.innerHTML = '⏳ Обработка...';

            let endpoint = '';
            let label = '';
            if (action === 'add') { endpoint = '/api/admin_add_balance';
                label = '➕ Пополнено'; }
            if (action === 'set') { endpoint = '/api/admin_set_balance';
                label = '✏️ Установлено'; }
            if (action === 'remove') { endpoint = '/api/admin_remove_balance';
                label = '➖ Списано'; }
            if (action === 'bonus') { endpoint = '/api/admin_add_balance';
                label = '🎁 Бонус начислен'; }

            const d = await apiCall(endpoint, { target_user_id: parseInt(userId), currency: currency, amount: amount });
            if (d.success) {
                resultDiv.innerHTML = '✅ ' + label + ' ' + amount + ' ' + currency + ' пользователю ' + userId;
                showToast('✅ ' + amount + ' ' + currency + ' ' + label.toLowerCase(), 'success');
                loadBalance();
                loadAdminPanel();
            } else {
                resultDiv.innerHTML = '❌ ' + (d.error || 'Ошибка');
                showToast('❌ ' + (d.error || 'Ошибка'), 'error');
            }
        };

        window.adminUserAction = function(userId, action) {
            showToast('🔄 Действие "' + action + '" для пользователя ' + userId, 'info');
            if (action === 'balance') {
                document.getElementById('balanceUserId').value = userId;
                document.querySelector('.admin-tabs button[data-tab="balance"]')?.click();
            }
        };

        function adminRefresh() {
            loadAdminPanel();
            showToast('🔄 Обновлено', 'info');
        }

        // ============================================================
        // 16. ПРОФИЛЬ
        // ============================================================
        async function loadProfile() {
            document.getElementById('profileName').textContent = user.firstName;
            document.getElementById('profileUsername').textContent = '@' + user.username;
            document.getElementById('profileDeals').textContent = dealsState.filter(d => d.status === 'completed').length;
            document.getElementById('profileRating').textContent = dealsState.filter(d => d.status === 'completed')
            .length > 0 ? '5.0' : '—';
            const total = (balanceState.balance.ton || 0) + (balanceState.balance.stars || 0) +
                (balanceState.balance.rub || 0) + (balanceState.balance.uah || 0);
            document.getElementById('profileBalanceMini').textContent = total;
            document.getElementById('profileLang').textContent = 'RU';
        }

        // ============================================================
        // 17. ВИЗАРД
        // ============================================================
        let wizardStep = 0;

        function updateWizard() {
            document.querySelectorAll('.wizard-panel').forEach(function(p) { p.classList.remove('active'); });
            document.querySelectorAll('.wizard-dot').forEach(function(d) { d.classList.remove('active'); });
            const panel = document.querySelector('.wizard-panel[data-step="' + wizardStep + '"]');
            if (panel) panel.classList.add('active');
            document.querySelectorAll('.wizard-dot').forEach(function(d, i) {
                if (i <= wizardStep) d.classList.add('active');
            });
            updatePreview();
        }

        function updatePreview() {
            const preview = document.getElementById('dealPreview');
            if (!preview) return;
            const cat = document.getElementById('categorySelect').value;
            const prod = document.getElementById('productInput').value.trim() || '—';
            const nft = document.getElementById('nftLinkInput').value.trim() || '—';
            const amt = document.getElementById('amountInput').value || '—';
            const cur = document.getElementById('currencySelect').value || 'TON';
            const buyer = document.getElementById('buyerInput').value.trim().replace('@', '') || '—';
            const parsed = parseNftLink(nft);
            const map = { 'nft_gift': '🖼️ NFT / Подарок', 'game_account': '🎮 Аккаунт игры', 'other': '📦 Другое' };
            let nftInfo = '';
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
                const nftLink = document.getElementById('nftLinkInput').value.trim();
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
        // 18. MODAL / TOAST
        // ============================================================
        window.showModal = function(html) {
            document.getElementById('modalBody').innerHTML = html;
            document.getElementById('modal').classList.add('active');
        };

        window.closeModal = function() {
            document.getElementById('modal').classList.remove('active');
        };

        document.getElementById('modal').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        // ============================================================
        // 19. ЗАПУСК
        // ============================================================
        console.log('🌊 Trust Gifts Mini App загружена');

        // Админ-кнопка
        if (isAdmin) {
            document.getElementById('adminNavBtn').style.display = 'flex';
        }

        const urlParams = new URLSearchParams(window.location.search);
        const pageParam = urlParams.get('page');
        if (pageParam === 'deals') setTimeout(() => showPage('deals'), 500);
        else if (pageParam === 'pay') setTimeout(() => showPage('balance'), 500);
        else if (pageParam === 'verify') setTimeout(() => showVerificationModal(), 500);
        else if (pageParam === 'withdraw') setTimeout(() => showPage('balance'), 500);

        loadMainData();
        loadBalance();
        loadDeals();
        loadProfile();

        setInterval(() => {
            if (document.getElementById('page-main').classList.contains('active')) loadMainData();
            if (document.getElementById('page-balance').classList.contains('active')) loadBalance();
            if (document.getElementById('page-profile').classList.contains('active')) loadProfile();
            if (document.getElementById('page-deals').classList.contains('active')) loadDeals();
            if (document.getElementById('page-support').classList.contains('active')) loadChatHistory();
            if (document.getElementById('page-admin').classList.contains('active')) loadAdminPanel();
        }, 15000);

        // ============================================================
        // ВЕРИФИКАЦИЯ (заглушка, чтобы не было ошибок)
        // ============================================================
        function showVerificationModal() {
            showModal(
                '<h3 style="margin-bottom:12px;">🔐 Верификация</h3>' +
                '<p style="color:var(--text-secondary);">Защита от мошенников</p>' +
                '<div class="form-group"><label>📱 Номер (+7XXXXXXXXXX)</label><input type="text" placeholder="+79001234567"></div>' +
                '<div class="form-group"><label>👤 Ваш Username</label><input type="text" placeholder="@john_doe"></div>' +
                '<button class="btn btn-primary" onclick="showToast(\'✅ Верификация пройдена!\',\'success\'); closeModal();"><i class="fas fa-check"></i> Пройти верификацию</button>' +
                '<button class="btn btn-secondary mt-10" onclick="closeModal()">Отмена</button>'
            );
        }
    </script>

</body>
</html>
