// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridWeek',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: function (info, successCallback, failureCallback) {
                axios.post('/get-schedules/', {
                    start_time: info.start.valueOf(),
                    end_time: info.end.valueOf()
                })
                    .then(response => {
                        var events = response.data.map(schedule => {
                            return {
                                id: schedule.id,
                                title: schedule.title,
                                start: schedule.start,
                                end: schedule.end,
                                backgroundColor: 'orange', // スケジュールをオレンジ色で表示
                                borderColor: 'orange'
                            };
                        });
                        successCallback(events);
                    })
                    .catch(error => {
                        console.error('スケジュールの取得に失敗しました', error);
                        failureCallback(error);
                    });
            }
        });

        calendar.render();
    } else {
        console.error("カレンダーの要素が見つかりませんでした");
    }
});
