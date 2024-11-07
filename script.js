class Calculator {
    constructor() {
        this.memory = 0;
        this.current = '';
        this.result = '0';
        this.history = [];
        this.isDarkMode = true;
        
        this.initializeElements();
        this.attachEventListeners();
        this.loadHistory();
    }

    initializeElements() {
        this.historyDisplay = document.getElementById('history');
        this.expressionDisplay = document.getElementById('expression');
        this.resultDisplay = document.getElementById('result');
        this.memoryDisplay = document.getElementById('memory-display');
        this.themeToggle = document.getElementById('theme-toggle');
    }

    attachEventListeners() {
        document.querySelectorAll('.buttons button').forEach(button => {
            button.addEventListener('click', () => this.handleButton(button.textContent));
        });

        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    handleButton(value) {
        switch(value) {
            case '=':
                this.calculate();
                break;
            case 'C':
                this.clear();
                break;
            case '⌫':
                this.delete();
                break;
            case 'MC':
                this.memory = 0;
                this.updateMemoryDisplay();
                break;
            case 'MR':
                this.current = this.memory.toString();
                this.updateDisplay();
                break;
            case 'M+':
                this.memory += parseFloat(this.result) || 0;
                this.updateMemoryDisplay();
                break;
            case 'M-':
                this.memory -= parseFloat(this.result) || 0;
                this.updateMemoryDisplay();
                break;
            case '±':
                this.toggleSign();
                break;
            case 'sin':
            case 'cos':
            case 'tan':
                this.calculateTrig(value);
                break;
            case '√':
                this.calculateSquareRoot();
                break;
            default:
                this.appendValue(value);
        }
    }

    handleKeyboard(e) {
        if (e.key.match(/[0-9.]/)) {
            this.appendValue(e.key);
        } else if (e.key === 'Enter') {
            this.calculate();
        } else if (e.key === 'Backspace') {
            this.delete();
        } else if (e.key === 'Escape') {
            this.clear();
        } else if (e.key.match(/[+\-*/()]/)) {
            this.appendValue(e.key);
        }
    }

    appendValue(value) {
        this.current += value;
        this.updateDisplay();
    }

    calculate() {
        try {
            const expression = this.current
                .replace(/×/g, '*')
                .replace(/÷/g, '/');
            const result = eval(expression);
            
            if (isFinite(result)) {
                this.history.push(`${this.current} = ${result}`);
                this.saveHistory();
                this.result = result.toString();
                this.current = result.toString();
                this.updateDisplay();
            } else {
                this.result = 'Error';
                this.current = '';
            }
        } catch {
            this.result = 'Error';
            this.current = '';
        }
        this.updateDisplay();
    }

    calculateTrig(func) {
        const value = parseFloat(this.current);
        if (isNaN(value)) return;
        
        const radians = value * Math.PI / 180;
        let result;
        
        switch(func) {
            case 'sin':
                result = Math.sin(radians);
                break;
            case 'cos':
                result = Math.cos(radians);
                break;
            case 'tan':
                result = Math.tan(radians);
                break;
        }
        
        this.current = result.toString();
        this.result = result.toString();
        this.updateDisplay();
    }

    calculateSquareRoot() {
        const value = parseFloat(this.current);
        if (isNaN(value) || value < 0) return;
        
        const result = Math.sqrt(value);
        this.current = result.toString();
        this.result = result.toString();
        this.updateDisplay();
    }

    toggleSign() {
        if (this.current.startsWith('-')) {
            this.current = this.current.slice(1);
        } else {
            this.current = '-' + this.current;
        }
        this.updateDisplay();
    }

    clear() {
        this.current = '';
        this.result = '0';
        this.updateDisplay();
    }

    delete() {
        this.current = this.current.slice(0, -1);
        this.updateDisplay();
    }

    updateDisplay() {
        this.expressionDisplay.textContent = this.current;
        this.resultDisplay.textContent = this.result;
        
        const recentHistory = this.history.slice(-2);
        this.historyDisplay.textContent = recentHistory.join(' | ');
    }

    updateMemoryDisplay() {
        this.memoryDisplay.textContent = `M: ${this.memory}`;
    }

    toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        document.body.setAttribute('data-theme', this.isDarkMode ? 'dark' : 'light');
        this.themeToggle.textContent = this.isDarkMode ? '🌙' : '☀️';
    }

    saveHistory() {
        localStorage.setItem('calculatorHistory', JSON.stringify(this.history.slice(-100)));
    }

    loadHistory() {
        const saved = localStorage.getItem('calculatorHistory');
        if (saved) {
            this.history = JSON.parse(saved);
            this.updateDisplay();
        }
    }
}

// Initialize calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new Calculator();
});