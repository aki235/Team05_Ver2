// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let selectedSubject = null;

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
                    subject: selectedSubject ? selectedSubject.name : ""
                })
                .then((response) => {
                    calendar.removeAllEvents(); // 一度すべての予定を削除
                    successCallback(response.data); // response.dataをもとにイベントを追加
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
        eventClick: function(info) {
            // スロットをクリックしたときの処理
            if (confirm("予約を行いますか？(1ポイントを消費します)")) {
                var slotId = info.event.id;
                axios
                    .post("/reserve-slot/", { slot_id: slotId, subject_id: selectedSubject.id })
                    .then(response => {
                        alert("予約が成立しました");
                        calendar.refetchEvents(); // 予約後にカレンダーをリフレッシュ
                    })
                    .catch(() => {
                        alert("予約に失敗しました");
                    });
            }
        }
    });

    calendar.render();

    document.getElementById("search-button").addEventListener("click", function() {
        var query = document.getElementById("subject-search").value;
        axios
            .post("/search-subjects/", { query: query })
            .then(response => {
                var resultsDiv = document.getElementById("search-results");
                resultsDiv.innerHTML = "";
                response.data.forEach(subject => {
                    var div = document.createElement("div");
                    div.textContent = `${subject.name} (${subject.subject_number})`;
                    div.dataset.subjectId = subject.id;
                    div.addEventListener("click", function() {
                        selectedSubject = subject; // 選択した科目をグローバル変数に保存
                        document.getElementById("subject-search").dataset.selectedSubject = subject.name;
                        // alert(subject.name);
                        calendar.removeAllEvents(); // 一度すべての予定を削除
                        axios
                            .post("/get-slot2/", {
                                start_time: calendar.view.activeStart.valueOf(),
                                end_time: calendar.view.activeEnd.valueOf(),
                                subject: subject.name
                            })
                            .then((response) => {
                                // alert(`Slots: ${JSON.stringify(response.data)}`); // スロットをアラート表示
                                response.data.forEach(event => {
                                    calendar.addEvent(event);
                                });
                            })
                            .catch(() => {
                                alert("スロットの読み込みに失敗しました");
                            });
                    });
                    resultsDiv.appendChild(div);
                });
            })
            .catch(() => {
                alert("検索に失敗しました");
            });
    });
});
