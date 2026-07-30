$(function() {
    var common = document.getElementById("common-timezones").textContent.split(",");
    var all = document.getElementById("all-timezones").textContent.split(",");

    function toOption(tz) {
        return {value: tz, group: common.includes(tz) ? ["c", "a"] : "a"}
    }

    document.querySelectorAll("select[name=tz]").forEach((el) => {
        new TomSelect(el, {
            diacritics: false,
            labelField: "value",
            lockOptgroupOrder: true,
            maxOptions: null,
            optgroupField: "group",
            options: all.map(toOption),
            optgroups: [
                {value: "c", label: "常用时区"},
                {value: "a", label: "所有时区"}
            ],
            placeholder: "输入搜索",
            plugins: ["dropdown_input", "no_backspace_delete"],
            refreshThrottle: 0,
            searchField: ["value"],
        });
    });
});