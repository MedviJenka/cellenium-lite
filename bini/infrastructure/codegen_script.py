JS_SCRIPT = """
    window.recordedInteractions = [];

    document.addEventListener('click', (event) => {
        const target = event.target;
        const interaction = {
            action: 'click',
            tag_name: target.tagName.toLowerCase(),
            id: target.id || null,
            name: target.name || null,
            xpath: generateXPath(target),
            action_description: `Clicked on ${target.tagName.toLowerCase()}`,
            value: null  // No value for clicks
        };
        window.recordedInteractions.push(interaction);
    });

    document.addEventListener('input', (event) => {
        const target = event.target;
        const interaction = {
            action: 'input',
            tag_name: target.tagName.toLowerCase(),
            id: target.id || null,
            name: target.name || null,
            xpath: generateXPath(target),
            action_description: `Typed in ${target.tagName.toLowerCase()}`,
            value: target.value || ''  // Explicitly capture the typed value
        };
        window.recordedInteractions.push(interaction);
    });

    function generateXPath(element) {
        if (element.id) return `//*[@id="${element.id}"]`;
        if (element === document.body) return '/html/body';
        let ix = 0;
        const siblings = element.parentNode ? element.parentNode.childNodes : [];
        for (let i = 0; i < siblings.length; i++) {
            const sibling = siblings[i];
            if (sibling === element) {
                const path = generateXPath(element.parentNode);
                return `${path}/${element.tagName.toLowerCase()}[${ix + 1}]`;
            }
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
        }
        return '';
    }
"""