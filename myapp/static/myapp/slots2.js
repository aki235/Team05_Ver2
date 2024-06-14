// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"


document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        // initialView: 'dayGridMonth',

        selectable: true,
        select: function(info) {
            // 重複チェック関数
            function isOverlapping(start, end) {
                let events = calendar.getEvents();
                for (let i = 0; i < events.length; i++) {
                    if ((start < events[i].end && end > events[i].start)) {
                        return true;
                    }
                }
                return false;
            }

            if (isOverlapping(info.start, info.end)) {
                alert("この時間帯には既に予定があります。");
                return;
            }


            const isConfirmed = confirm("この時間帯にスロットを追加しますか？");

            if (isConfirmed) {
                axios
                    .post("/add-slot/", {
                        start_time: info.start.valueOf(),
                        end_time: info.end.valueOf(),
                    })
                    .then((response) => {
                        // イベントの追加
                        calendar.addEvent({
                            id: response.data.id,  // 返されたIDを設定
                            title: "slot",
                            start: info.start,
                            end: info.end,
                            allDay: false,
                        });
                    })
                    .catch(() => {
                        // バリデーションエラーなど
                        alert("登録に失敗しました");
                    });
            }
        },
        eventDidMount: function(info) {
            console.log("Event ID:", info.event.id);  // IDをログに出力
            info.el.addEventListener('contextmenu', function(ev) {
                ev.preventDefault(); // 右クリックメニューを抑制
                const isConfirmed = confirm("このスロットを削除しますか？");
                if (isConfirmed) {
                    axios
                        .post("/delete-slot/", {
                            id: info.event.id
                        })
                        .then(() => {
                            // イベントの削除
                            info.event.remove();
                        })
                        .catch(() => {
                            // バリデーションエラーなど
                            alert("削除に失敗しました");
                        });
                }
            });
        },
        events: function (info, successCallback, failureCallback) {
            axios
                .post("/get-slot/", {
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
