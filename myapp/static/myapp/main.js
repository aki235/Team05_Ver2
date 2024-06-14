// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            // initialView: 'timeGridWeek',
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: function (info, successCallback, failureCallback) {
                axios.get('/get-schedules/')
                    .then(response => {
                        // ログイン中のユーザーが関与するスケジュールのみをフィルタリング
                        var events = response.data.map(schedule => {
                            return {
                                id: schedule.id,
                                title: `${schedule.teacher} teaches ${schedule.learner}`,
                                start: schedule.start_time,
                                end: schedule.end_time,
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
