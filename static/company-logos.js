/**
 * InternHub Official Company Vector Logos & Dynamic Monogram Generator
 */
const CompanyLogos = {
  // Official Vector SVGs
  logos: {
    google: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
      <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
      <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
      <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
    </svg>`,

    microsoft: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <rect x="2" y="2" width="20" height="20" fill="#f25022"/>
      <rect x="26" y="2" width="20" height="20" fill="#7fba00"/>
      <rect x="2" y="26" width="20" height="20" fill="#00a4ef"/>
      <rect x="26" y="26" width="20" height="20" fill="#ffb900"/>
    </svg>`,

    amazon: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <path fill="#FF9900" d="M37.3 36.4c-4.4 3.3-10.7 5.1-16.3 5.1-7.8 0-14.8-2.9-20.1-7.7-.4-.4-.1-.9.4-.6 5.8 3.3 12.8 5.3 20.1 5.3 5.1 0 10.6-1.3 15.5-4.1.6-.4 1 .3.4.7z"/>
      <path fill="#FF9900" d="M39.1 34.2c-.5-.7-3.4-.3-4.9-.2-.5 0-.6-.4-.1-.7 2.9-2 7.7-1.4 8.2-.7.4.7-.4 5.5-3.1 7.7-.4.3-.8.1-.6-.3.6-1.5 1-4.7.5-5.8z"/>
      <path fill="#ffffff" d="M24.8 12c-5.7 0-9.8 4.3-9.8 10.3 0 6.6 4.6 10.3 10.4 10.3 3.6 0 6.4-1.6 7.9-3.7v3.2c0 .4.3.7.7.7h3.3c.4 0 .7-.3.7-.7V12.7c0-.4-.3-.7-.7-.7h-3.3c-.4 0-.7.3-.7.7v3.1c-1.6-2.3-4.4-3.8-7.9-3.8zm1.2 4.2c3.5 0 6.1 2.7 6.1 6.5 0 4-2.6 6.5-6.1 6.5-3.6 0-6.1-2.6-6.1-6.5 0-3.8 2.5-6.5 6.1-6.5z"/>
    </svg>`,

    infosys: `<svg viewBox="0 0 60 28" width="100%" height="100%">
      <rect width="60" height="28" rx="6" fill="#007cc3"/>
      <text x="30" y="19" font-family="'Plus Jakarta Sans', Arial, sans-serif" font-size="14" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="0.5">Infosys</text>
    </svg>`,

    tcs: `<svg viewBox="0 0 60 28" width="100%" height="100%">
      <rect width="60" height="28" rx="6" fill="#0c2340"/>
      <path d="M6 14 C12 6, 20 6, 26 14 C20 22, 12 22, 6 14 Z" fill="#0072ce" opacity="0.6"/>
      <text x="38" y="19" font-family="'Plus Jakarta Sans', Arial, sans-serif" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="1">TCS</text>
    </svg>`,

    apple: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <path fill="#ffffff" d="M35.6 24.5c0-5.7 4.7-8.4 4.9-8.6-2.7-3.9-6.8-4.4-8.3-4.5-3.5-.4-6.8 2.1-8.6 2.1-1.8 0-4.6-2-7.5-2-3.8 0-7.4 2.2-9.4 5.7-4 7-1 17.3 2.9 22.9 1.9 2.8 4.2 5.8 7.2 5.7 2.9-.1 4-1.9 7.5-1.9 3.5 0 4.5 1.9 7.6 1.8 3.1-.1 5.1-2.8 7-5.6 2.2-3.2 3.1-6.4 3.2-6.5-.1-.1-6.5-2.5-6.5-9.1zm-4.7-16.1c1.6-1.9 2.6-4.6 2.3-7.3-2.3.1-5 1.5-6.6 3.4-1.4 1.6-2.6 4.3-2.3 6.9 2.5.2 5-1.1 6.6-3z"/>
    </svg>`,

    meta: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <path fill="url(#meta-grad)" d="M24 16.5c-4.2-6-8.2-9-12.8-9C5 7.5 0 12.8 0 19.3c0 7.8 6.5 14.7 13.8 14.7 4.8 0 8.3-2.6 10.2-5.4 1.9 2.8 5.4 5.4 10.2 5.4 7.3 0 13.8-6.9 13.8-14.7 0-6.5-5-11.8-11.2-11.8-4.6 0-8.6 3-12.8 9zm-10.2 12c-4.4 0-8.3-4.5-8.3-9.2 0-3.9 3-7.1 6.8-7.1 2.8 0 5.4 2 8.3 6.6-2.4 4.5-4.8 9.7-6.8 9.7zm20.4 0c-2 0-4.4-5.2-6.8-9.7 2.9-4.6 5.5-6.6 8.3-6.6 3.8 0 6.8 3.2 6.8 7.1 0 4.7-3.9 9.2-8.3 9.2z"/>
      <defs>
        <linearGradient id="meta-grad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop stop-color="#0081fb"/>
          <stop offset="1" stop-color="#0064e0"/>
        </linearGradient>
      </defs>
    </svg>`,

    careconnect: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <rect width="48" height="48" rx="12" fill="url(#care-grad)"/>
      <path d="M24 12v24M12 24h24" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
      <path d="M16 24h4l2-4 4 8 2-4h4" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <defs>
        <linearGradient id="care-grad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop stop-color="#0ea5e9"/>
          <stop offset="1" stop-color="#059669"/>
        </linearGradient>
      </defs>
    </svg>`,

    digitaldynamics: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <rect width="48" height="48" rx="12" fill="url(#digital-grad)"/>
      <path d="M14 16l10-6 10 6v16l-10 6-10-6V16z" fill="none" stroke="#ffffff" stroke-width="3"/>
      <path d="M14 16l10 6 10-6M24 22v16" stroke="#ffffff" stroke-width="2.5"/>
      <circle cx="24" cy="22" r="3" fill="#38bdf8"/>
      <defs>
        <linearGradient id="digital-grad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop stop-color="#8b5cf6"/>
          <stop offset="1" stop-color="#3b82f6"/>
        </linearGradient>
      </defs>
    </svg>`,

    basehub: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <rect width="48" height="48" rx="12" fill="url(#basehub-grad)"/>
      <path d="M14 16c0-2.2 4.5-4 10-4s10 1.8 10 4M14 16v16c0 2.2 4.5 4 10 4s10-1.8 10-4V16M14 24c0 2.2 4.5 4 10 4s10-1.8 10-4" stroke="#ffffff" stroke-width="2.8" stroke-linecap="round" fill="none"/>
      <defs>
        <linearGradient id="basehub-grad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop stop-color="#06b6d4"/>
          <stop offset="1" stop-color="#2563eb"/>
        </linearGradient>
      </defs>
    </svg>`,

    techcorp: `<svg viewBox="0 0 48 48" width="100%" height="100%">
      <rect width="48" height="48" rx="12" fill="url(#techcorp-grad)"/>
      <circle cx="24" cy="24" r="8" fill="none" stroke="#ffffff" stroke-width="3"/>
      <path d="M24 8v6M24 34v6M8 24h6M34 24h6" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
      <defs>
        <linearGradient id="techcorp-grad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop stop-color="#1e1b4b"/>
          <stop offset="1" stop-color="#4338ca"/>
        </linearGradient>
      </defs>
    </svg>`
  },

  // Generates a deterministic luxury gradient monogram badge
  generateMonogram: function(name) {
    const cleanName = (name || 'Company').trim();
    const initials = cleanName.split(' ').map(w => w[0]).filter(Boolean).slice(0, 2).join('').toUpperCase() || 'CO';
    
    // Deterministic hue based on name hash
    let hash = 0;
    for (let i = 0; i < cleanName.length; i++) {
      hash = cleanName.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue1 = Math.abs(hash % 360);
    const hue2 = (hue1 + 45) % 360;

    return `<div class="monogram-badge" style="background: linear-gradient(135deg, hsl(${hue1}, 75%, 50%), hsl(${hue2}, 85%, 35%));">
      <span class="monogram-text">${initials}</span>
      <div class="monogram-shine"></div>
    </div>`;
  },

  // Returns SVG HTML for a given company name
  getLogoHtml: function(name) {
    if (!name) return this.generateMonogram('Company');
    const key = name.toLowerCase().replace(/[^a-z0-9]/g, '');

    if (key.includes('google')) return this.logos.google;
    if (key.includes('microsoft')) return this.logos.microsoft;
    if (key.includes('amazon') || key.includes('aws')) return this.logos.amazon;
    if (key.includes('infosys')) return this.logos.infosys;
    if (key.includes('tcs') || key.includes('tata')) return this.logos.tcs;
    if (key.includes('apple')) return this.logos.apple;
    if (key.includes('meta') || key.includes('facebook')) return this.logos.meta;
    if (key.includes('careconnect') || key.includes('care connect') || key.includes('health')) return this.logos.careconnect;
    if (key.includes('digitaldynamics') || key.includes('digital dynamics')) return this.logos.digitaldynamics;
    if (key.includes('basehub')) return this.logos.basehub;
    if (key.includes('techcorp')) return this.logos.techcorp;

    return this.generateMonogram(name);
  },

  // Injects logos into all DOM elements with [data-company]
  init: function() {
    document.querySelectorAll('[data-company-logo]').forEach(el => {
      const companyName = el.getAttribute('data-company-logo') || el.innerText;
      el.innerHTML = this.getLogoHtml(companyName);
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  CompanyLogos.init();
});
