// document.addEventListener('DOMContentLoaded', function () {

//     var calendarEl = document.getElementById('calendar');

//     var calendar = new FullCalendar.Calendar(calendarEl, {
//         initialView: 'timeGridWeek',

//         selectable: true,
//         select: function(info) {
//             const eventName = prompt("スロットを入力してください");

//             if (eventName) {
//                 calendar.addEvent({
//                     title: eventName,
//                     start: info.start,
//                     end: info.end,
//                     allDay: false,
//                 });
//             }
//         },
//         // slotDuration: '00:15:00',
//     });

//     calendar.render();
// });

// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"


document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        // initialView: 'dayGridMonth',

        selectable: true,

        events: function (info, successCallback, failureCallback) {
            axios
                .post("/get-slot2/", {
                    start_time: info.start.valueOf(),
                    end_time: info.end.valueOf(),
                })
                .then((response) => {
                    calendar.removeAllEvents();
                    successCallback(response.data);
                })
                .catch(() => {
                    // バリデーションエラーなど
                    alert("読み込みに失敗しました");
                });
        },
        // 15分刻みのスロットを表示
        slotDuration: '00:15:00',
        // 1時間ごとに時間ラベルを表示
        slotLabelInterval: '01:00:00',
    });

    calendar.render();
});
