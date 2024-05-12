const timer = (deadline) => {
    const timerDays = document.querySelectorAll(".count_1>span");
    const timerHours = document.querySelectorAll(".count_2>span");
    const timerMinutes = document.querySelectorAll(".count_3>span");
    const timerSeconds = document.querySelectorAll(".count_4>span");

    const getTimeRemaining = () => {
        let dateStop = new Date(deadline).getTime();
        let dateNow = new Date().getTime();
        let timeRemaining = (dateStop - dateNow) / 1000;
        let days = Math.floor(timeRemaining / 60 / 60 / 24);
        let hours = Math.floor((timeRemaining / 60 / 60) % 24);
        let minutes = Math.floor((timeRemaining / 60) % 60);
        let seconds = Math.floor(timeRemaining % 60);

        return { timeRemaining, days, hours, minutes, seconds };
    };

    const updateClock = () => {
        let getTime = getTimeRemaining();
        timerDays.forEach((days) => {
            days.textContent = ("0" + getTime.days).slice(-2);
        });
        timerHours.forEach((hours) => {
            hours.textContent = ("0" + getTime.hours).slice(-2);
        });
        timerMinutes.forEach((minutes) => {
            minutes.textContent = ("0" + getTime.minutes).slice(-2);
        });
        timerSeconds.forEach((seconds) => {
            seconds.textContent = ("0" + getTime.seconds).slice(-2);
        });
    };

    setTimeout(() => {
        let getTime = getTimeRemaining();
        if (getTime.timeRemaining > 0) {
            updateClock();
        } else if (getTime.timeRemaining === 0) {
            clearTimeout(updateClock);
        }
    });

    setInterval(() => {
        let getTime = getTimeRemaining();
        if (getTime.timeRemaining > 0) {
            updateClock();
        } else if (getTime.timeRemaining === 0) {
            clearInterval(updateClock);
        }
    }, 1000);
};

timer(`31 may 2025`);