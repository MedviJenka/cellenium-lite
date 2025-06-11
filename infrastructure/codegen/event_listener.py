JS_SCRIPT = """
window.recordedInteractions = [];

// Debounce utility to delay logging until typing is finished
function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

// Capture click events
document.addEventListener('click', (event) => {
    const target = event.target;

    // Skip logging click events for checkboxes
    if (target.tagName.toLowerCase() === 'input' && target.type === 'checkbox') {
        return;
    }

    const tag_name = target.tagName.toLowerCase();
    const element_text = target.textContent.trim();
    const element_id = target.id.toLowerCase();
    const element_name = target.name.toLowerCase();
    
    
    const interaction = {
        action: 'click',
        tag_name: `${element_text}_${tag_name}` || `${element_id}_${tag_name}` || `${element_name}_${tag_name}` ,
        id: target.id || null,
        name: target.name || null,
        xpath: generateXPath(target),
        action_description: `Clicked on ${element_text || tag_name}`,
        value: null // No value for clicks
    };
    window.recordedInteractions.push(interaction);
});

// Capture input events with debouncing
document.addEventListener('input', debounce((event) => {

    const target = event.target;
    const tag_name = target.tagName.toLowerCase();
    const element_id = target.id ? target.id.toLowerCase() : 'undetected';
    const element_name = target.name ? target.name.toLowerCase() : 'undetected';
    
    // Only handle inputs or textareas
    if (target.tagName.toLowerCase() === 'input' || target.tagName.toLowerCase() === 'textarea') {
        const interaction = {
            action: 'input',
            tag_name: `${element_id}_${tag_name}` || tag_name || element_id,
            id: target.id || null,
            name: target.name || null,
            xpath: generateXPath(target),
            action_description: `Typed in ${target.tagName.toLowerCase()}`,
            value: target.value || '' // Explicitly capture the full typed value
        };
        window.recordedInteractions.push(interaction);
    }
}, 2000)); // Adjust debounce delay as needed (300ms is typical)

// Capture checkbox events
document.addEventListener('change', (event) => {
    const target = event.target;

    // Only handle checkboxes
    if (target.tagName.toLowerCase() === 'input' && target.type === 'checkbox') {
        const interaction = {
            action: 'change',
            tag_name: target.tagName.toLowerCase(),
            id: target.id || null,
            name: target.name || null,
            xpath: generateXPath(target),
            action_description: `Checkbox ${target.checked ? 'unchecked' : 'checked'}`,
        };
        window.recordedInteractions.push(interaction);
    }
});

// Generate XPath for an element
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


def init_code(device: str) -> str:

    st_import = "from qasharedinfra.devices.audc.smarttap.smarttap import SmartTap"
    mi_import = "from qasharedinfra.devices.audc.meetinginsights.meetinginsights import MeetingInsightsSaaS"

    CODE = f"""
    import pytest
    import coreinfra.core.environment.environment_variables as env
    from coreinfra.services.selenium.mappedselenium import MappedSelenium
    {st_import if device == 'st' else mi_import}
    from qasharedinfra.infra.smarttap.selenium.utils.bini_utils import IRBiniUtils
    
    HEADLESS = False
    {device}: {'SmartTap' if device == 'st' else 'MeetingInsightsSaaS'} = env.devices['Device_1']
    log = env.logger
    
    
    @pytest.fixture(scope='module', autouse=True)
    def init_globals() -> None:
    
        {device}.logger_.info('\n******** Module (Script) Setup ********')
        bini = IRBiniUtils()
        {device}.test_prerequisites(selenium=True, headless=HEADLESS)
        {device}.ui.utils.st_selenium_go_to_screen_in_current_window({device}.selenium, {device}.st_screens)  # add screen
    
        yield bini
    
        {device}.logger.info('******** Module (Script) TearDown ********')
        {device}.selenium.finalize()
    
    
    @pytest.fixture(scope='function', autouse=True)
    def setup_and_teardown() -> None:
        {device}.logger_.info('******** Test Setup ********')
    
        yield
    
        {device}.logger_.info('******** Test TearDown ********')
    
    @pytest.fixture
    def driver() -> MappedSelenium:
        return {device}.selenium
    
    """
    return CODE
