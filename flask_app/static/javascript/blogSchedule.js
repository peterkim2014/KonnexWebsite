const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

const today = new Date();
let selectedDate = null;

document.addEventListener("DOMContentLoaded", function() {
    populateSelectors();
    generateCalendar();
});

function populateSelectors() {
    const monthSelector = document.getElementById('month-selector');
    const yearSelector = document.getElementById('year-selector');

    months.forEach((month, index) => {
        let option = document.createElement('option');
        option.value = index;
        option.text = month;
        if (index === today.getMonth()) {
            option.selected = true;
        }
        monthSelector.add(option);
    });

    let currentYear = today.getFullYear();
    for (let i = currentYear - 10; i <= currentYear + 10; i++) {
        let option = document.createElement('option');
        option.value = i;
        option.text = i;
        if (i === currentYear) {
            option.selected = true;
        }
        yearSelector.add(option);
    }
}

function generateCalendar() {
    const month = document.getElementById('month-selector').value;
    const year = document.getElementById('year-selector').value;

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, parseInt(month) + 1, 0).getDate();
    const calendar = document.getElementById('calendar');
    calendar.innerHTML = '';

    const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    dayNames.forEach(day => {
        const dayNameElem = document.createElement('div');
        dayNameElem.className = 'day-name';
        dayNameElem.innerText = day;
        calendar.appendChild(dayNameElem);
    });

    // Create empty cells for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'day hidden';
        calendar.appendChild(emptyCell);
    }

    // Create cells for each day of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.className = 'day';
        dayCell.innerText = day;
        dayCell.onclick = () => selectDay(day, month, year);
        calendar.appendChild(dayCell);
    }
}

function selectDay(day, month, year) {
    // Hide the calendar and show the selected day content
    document.getElementById('calendar').style.display = 'none';
    document.querySelector('.calendar-header').style.display = 'none';

    // Update the day content with selected day details
    const dayContent = document.createElement('div');
    dayContent.className = 'day-content';
    dayContent.innerHTML = `
        <div class="selected-leftSide">
            <div class="selected-header">
                <button class="selectedDay-button" onclick="backToCalendar()"></button>
                <h2 class="selected-date">${months[month]} ${day}, ${year}</h2>
            </div>
            <div class="selectedData">
                Add Contents Here
            </div>
        </div>
        <div class="selected-rightSide">
            <h3>Add Post</h3>
            <form class="scheduleForm">
                <input placeholder="Post ID"/>
                <input placeholder="Time of Day"/>
                <input placeholder="Alert"/>
                <input placeholder="Platform"/>
                <button>Submit</button>
            </form>
        </div>
    `;

    // Append day content to the container
    document.querySelector('.calendar-container').appendChild(dayContent);
}

function backToCalendar() {
    // Remove the selected day content and show the calendar again
    document.querySelector('.day-content').remove();
    document.getElementById('calendar').style.display = 'grid';
    document.querySelector('.calendar-header').style.display = 'flex';
}
