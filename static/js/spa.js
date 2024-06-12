import { initializeSPA} from './spa-utils.js';

if (!localStorage.getItem('language')) {
	localStorage.setItem('language', 'en');
}

document.addEventListener('DOMContentLoaded', function() {
    initializeSPA();
});