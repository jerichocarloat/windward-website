# Windward icon set: 24px grid, 1.5px stroke, square caps, miter joins, no fills.
ICONS = {
    'Search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>',
    'Conversation': '<path d="M3 4h12v9H8l-3.5 3v-3H3z"/><path d="M17.5 8H21v9h-1.5v3l-3.5-3h-5v-2"/>',
    'Firm': '<path d="M3 21h18M4.5 21V9L12 4l7.5 5v12"/><path d="M8.5 21v-8M12 21v-8M15.5 21v-8"/>',
    'Person': '<circle cx="12" cy="8" r="3.75"/><path d="M4.5 21c.8-4.2 3.8-6.5 7.5-6.5s6.7 2.3 7.5 6.5"/>',
    'Team': '<circle cx="9" cy="8.5" r="3.25"/><path d="M3 20c.6-3.6 3-5.6 6-5.6s5.4 2 6 5.6"/><path d="M15 5.5a3 3 0 010 6M17 14.6c2.2.6 3.6 2.4 4 5.4"/>',
    'Insight': '<path d="M3 18l6-6 4 4 8-9"/><path d="M15 7h6v6"/>',
    'Discretion': '<rect x="4.5" y="10.5" width="15" height="10.5"/><path d="M8 10.5V7.5a4 4 0 018 0v3"/><path d="M12 14.5v3"/>',
    'Calendar': '<rect x="3.5" y="5" width="17" height="15.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    'Document': '<path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14.5 3v4.5H19M9 12h7M9 16h7"/>',
    'Phone': '<path d="M5 3.5h4l1.8 4.5-2.3 1.4a11 11 0 006.1 6.1l1.4-2.3 4.5 1.8v4c0 .8-.7 1.5-1.5 1.5C10.6 20.5 3.5 13.4 3.5 5 3.5 4.2 4.2 3.5 5 3.5z"/>',
    'Email': '<rect x="3" y="5.5" width="18" height="13"/><path d="M3 6l9 7 9-7"/>',
    'Location': '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0113 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.25"/>',
    'Role': '<rect x="3" y="7.5" width="18" height="12.5"/><path d="M8.5 7.5V4.5h7v3M3 13h18"/>',
    'Shortlist': '<path d="M9.5 6.5H21M9.5 12H21M9.5 17.5H21"/><path d="M3 6.5l1.5 1.5L7 5M3 12l1.5 1.5L7 10.5M3 17.5l1.5 1.5L7 16"/>',
    'Fit': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    'Trust': '<path d="M12 3l7.5 3v6c0 4.5-3.2 7.8-7.5 9-4.3-1.2-7.5-4.5-7.5-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    'Network': '<circle cx="12" cy="5" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/><circle cx="12" cy="13" r="2"/><path d="M12 7v4M10.4 14.2L6.6 16.8M13.6 14.2l3.8 2.6"/>',
    'Reach': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.7 5.6 3.7 9s-1.2 6.4-3.7 9c-2.5-2.6-3.7-5.6-3.7-9S9.5 5.6 12 3z"/>',
    'Market data': '<path d="M3 21h18"/><path d="M6 17v-5M10.5 17V8M15 17v-7M19.5 17V5"/>',
    'Compensation': '<circle cx="12" cy="12" r="9"/><path d="M14.8 9c-.5-1.1-1.5-1.6-2.8-1.6-1.6 0-2.8.8-2.8 2.1 0 3 5.7 1.6 5.7 4.6 0 1.4-1.3 2.3-2.9 2.3-1.4 0-2.5-.6-3-1.8M12 6v1.4M12 16.4V18"/>',
    'Judgment': '<path d="M12 4v16M7 20h10M5 7h14"/><path d="M5 7l-2.5 6a2.5 2.5 0 005 0zM19 7l-2.5 6a2.5 2.5 0 005 0z"/>',
    'Time': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    'Perspective': '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    'Idea': '<path d="M9 18h6M10 21h4"/><path d="M8.5 15c-1.6-1.2-2.5-3-2.5-5a6 6 0 0112 0c0 2-.9 3.8-2.5 5z"/>',
    'Growth': '<path d="M12 21v-9"/><path d="M12 12c0-4 2.5-6.5 7-6.5 0 4.5-2.5 6.5-7 6.5zM12 15c0-3-2-5-6-5 0 3.5 2 5 6 5z"/>',
    'Succession': '<path d="M4 9a8 8 0 0114-3l2 2M20 15a8 8 0 01-14 3l-2-2"/><path d="M20 3.5V8h-4.5M4 20.5V16h4.5"/>',
    'Credentials': '<path d="M2.5 9L12 4.5 21.5 9 12 13.5z"/><path d="M6.5 11v5c1.5 1.4 3.4 2 5.5 2s4-.6 5.5-2v-5M21.5 9v5"/>',
    'Article': '<rect x="3.5" y="4" width="17" height="16"/><path d="M7 8h10M7 12h10M7 16h6"/>',
    'Link': '<path d="M7 17L17 7M9 7h8v8"/>',
    'Bearing point': '<path d="M12 2.5L17 12l-5 9.5L7 12z"/>',
}

ORDER = list(ICONS.keys())


def icon(name, size=28, color='#0B0C0E', sw=1.5):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="square" stroke-linejoin="miter" style="display:block;flex:none">{ICONS[name]}</svg>')
