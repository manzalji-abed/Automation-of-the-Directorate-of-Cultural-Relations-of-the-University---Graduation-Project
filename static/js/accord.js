const app = document.getElementById('content');

const accordions = {
    Experience: { isOpen: false },
    Personal: { isOpen: false },
    Contact: { isOpen: false },
    Social: { isOpen: false },
    Unvdegree: { isOpen: false },
    High: { isOpen: false },
    Cer: { isOpen: false },
    Efad: { isOpen: false },
};

function toggleAccordion(label) {
    const accordion = accordions[label];
    if (accordion) {
        accordion.isOpen = !accordion.isOpen;
        updateAccordion(label);
    } else {
        console.error(`Could not find accordion '${label}'`);
    }
}

function areAllAccordionsOpen() {
    return Object.keys(accordions).every((key) => accordions[key].isOpen);
}

function updateAccordion(label) {
    const accordionHeader = app.querySelector(
        `[onclick="toggleAccordion('${label}')"`
    );
    const accordionIcon = accordionHeader.querySelector('.accordion-icon');
    const accordionContent = app.querySelector(
        `#${label.toLowerCase()}-content`
    );
    if (accordions[label].isOpen) {
        accordionHeader.classList.add('accordions__button--active');
        accordionContent.classList.add('accordions__content--expanded');
    } else {
        accordionHeader.classList.remove('accordions__button--active');
        accordionContent.classList.remove('accordions__content--expanded');
    }
}

function init() {
    Object.keys(accordions).forEach((key) => {
        updateAccordion(key);
    });
}

init();
