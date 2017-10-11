$(() => {
    $('.progress-bar').tooltip({});
    $('.job-title').on('click', (e) => {
        console.log(e.target);
        $(e.target).closest('label').siblings('table.summary-data').toggle();
    });
});
